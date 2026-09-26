"""The shared adjudicator: per-instance judging of negative signals and repeated queries.

Paper section B.3: negative labels have three sources -- a failed tool call, a missing
required state change, and an **unresolved negative signal**. This module handles only the
third: one LLM call reads the whole dialogue and gives negative_signal / repeated_query for
each instance.

It deliberately does not do two things that the old "execution guard" used to do:

- **Completeness review** (an intent labelled requires_terminal_action with no terminal call)
  is judged deterministically by outcome._classify, needing no LLM and no knowledge of what
  the service agent said;
- **Completing / re-sending tool calls** has been removed from this repository.

Removing completion changes none of the numbers the paper reports. During development both
the growth stage and the evaluation stage ran in the two modes where "guard judging takes part
in neither outcome composition nor reward" (corresponding in the scripts to `--guard off` and
`--guard observe`, a switch that has since been deleted along with the guard), so those two
modes are behaviourally exactly equivalent to this module -- this module is what they did. See
the growth and evaluation stages in scripts/run_*_iel.sh.
"""

from __future__ import annotations

import json
from typing import Any

from llm_retry import invoke_with_retry
from intent.jsonio import coerce_bool, extract_json
from intent.store import Instance

# The judged fields are fixed, with no room for free discretion. Neither manufactures
# success; they only make judging stricter.
SIGNAL_FIELDS = ("negative_signal", "repeated_query")


def build_verify_prompt(
    instances: list[Instance], conversation: list[dict[str, str]]
) -> str:
    """Assemble the prompt for one adjudication.

    The whole dialogue (including the service agent's replies) must be shown to the LLM: user
    dissatisfaction and repeated questions may fall in turns outside this intent's tool calls,
    so looking only at the tool record would miss them.
    """
    dialogue = "\n".join(
        f"[{i}] User: {turn.get('user', '')}\n[{i}] Agent: {turn.get('assistant', '')}"
        for i, turn in enumerate(conversation)
    )
    records = [
        {
            "intent": instance.intent,
            "user_text": instance.text,
            "slots": instance.slots,
            "tools": [
                {"name": call.name, "action": call.action, "status": call.status}
                for call in instance.tools
            ],
        }
        for instance in instances
    ]
    return (
        "You are reviewing how an e-commerce customer-service dialogue was carried out. "
        "Below are the full dialogue and the tool calls split by intent.\n\n"
        "For **every** instance, judge two things (the checks are fixed; do not exercise "
        "your own discretion):\n"
        "1. negative_signal: within the dialogue span related to this intent, did the user "
        "repeat the same request, express clear dissatisfaction, or reject the conclusion "
        "the agent gave?\n"
        "2. repeated_query: did the user ask the same question again in a later turn?\n\n"
        f"Dialogue:\n{dialogue}\n\n"
        f"Instances:\n{json.dumps(records, ensure_ascii=False, indent=2)}\n\n"
        'Output JSON only: {"instances": [{"intent": "intent id", "negative_signal": '
        'true/false, "repeated_query": true/false}]}'
    )


def parse_verify_output(raw: str, intent_ids: list[str]) -> dict[str, dict[str, bool]]:
    """Parse the adjudication output. Intent ids outside the taxonomy are always dropped,
    never letting a hallucination through.

    When extract_json cannot parse, an empty table is returned and no instance gets a verdict
    this round, so negative_signal / repeated_query are all False -- the adjudication does not
    intervene. Format drift must not manufacture failure in the other direction.
    """
    payload = extract_json(raw)
    if not payload:
        return {}
    items = payload.get("instances")
    if not isinstance(items, list):
        return {}
    valid = set(intent_ids)
    parsed: dict[str, dict[str, bool]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        intent_id = str(item.get("intent", "")).strip()
        if intent_id not in valid:
            continue
        # Use coerce_bool rather than bare bool(): the model may output the string "false"
        # (legal JSON), and bool("false") == True would invert the negative signal.
        parsed[intent_id] = {
            field: coerce_bool(item.get(field, False)) for field in SIGNAL_FIELDS
        }
    return parsed


def verify_signals(
    llm: Any,
    instances: list[Instance],
    conversation: list[dict[str, str]],
) -> dict[str, dict[str, bool]]:
    """Adjudicate the whole episode with one LLM call, returning intent id -> signal dict.

    Returns an empty table when the LLM call fails: better to miss a verdict than to turn a
    normal instance into a failure on the strength of one failed call. The caller treats an
    empty table as all signals being False.

    Results are keyed by instance.intent, so it assumes the same intent id appears at most once
    in instances -- which holds at the call site because build_instances has already merged by
    intent id. On a duplicate the later entry overwrites the earlier one, matching the old
    guard's behaviour.
    """
    if not instances:
        return {}
    intent_ids = [instance.intent for instance in instances]
    try:
        response = invoke_with_retry(
            llm,
            [{"role": "user", "content": build_verify_prompt(instances, conversation)}],
            description="intent.verify_signals",
        )
        raw = getattr(response, "content", response)
        return parse_verify_output(raw if isinstance(raw, str) else str(raw), intent_ids)
    except Exception:  # noqa: BLE001
        return {}
