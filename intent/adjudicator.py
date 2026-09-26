"""Admission adjudication.

A candidate intent has three choices (merge / slot / new, defaulting to slot), a candidate
slot has two (accept / reject). The default outlet is slot rather than new -- the root cause
of the old skill library exploding was precisely defaulting to creating new ones.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from typing import Any

from llm_retry import invoke_with_retry
from intent.config import DISCRIMINATION_ACCURACY_THRESHOLD, NEIGHBOR_TOP_K
from intent.jsonio import coerce_bool, extract_json
from intent.prompts import ADJUDICATE_INTENT_RULES, ADJUDICATE_SLOT_RULES
from intent.taxonomy import Intent, Taxonomy


@dataclass
class IntentDecision:
    outlet: str
    target_id: str = ""
    new_id: str = ""
    description: str = ""
    discriminators: dict[str, str] = field(default_factory=dict)
    slot_key: str = ""
    slot_value: str = ""
    aliases: list[str] = field(default_factory=list)
    reason: str = ""
    # Set on a double fallback (the neighbour set is a fallback + the adjudication output is
    # unparseable): no link of this adjudication was ever really determined, so the caller
    # must set the candidate aside as-is.
    deferred: bool = False
    # Whether this intent must produce one state change to be complete. None means the LLM
    # did not give it or it could not be parsed, leaving it to the section 4.3 one-way
    # correction to tighten in later episodes -- never guess here.
    requires_terminal_action: bool | None = None


def _invoke(llm: Any, prompt: str) -> str:
    response = invoke_with_retry(
        llm, [{"role": "user", "content": prompt}], description="intent.adjudicate"
    )
    raw = getattr(response, "content", response)
    return raw if isinstance(raw, str) else str(raw)


def select_neighbors(desc: str, taxonomy: Taxonomy, llm: Any) -> list[str]:
    """Select the intents most similar to the candidate from the whole table.

    The taxonomy is small at this stage (expected < 50 entries), so we introduce no vector
    retrieval and simply hand the whole table to the LLM to pick from.
    """
    intents = taxonomy.active()
    if not intents:
        return []
    if len(intents) <= NEIGHBOR_TOP_K:
        return [intent.id for intent in intents]

    catalog = json.dumps(
        [{"id": i.id, "description": i.description} for i in intents], ensure_ascii=False
    )
    prompt = (
        f"Select the {NEIGHBOR_TOP_K} intents below whose semantics are closest to the "
        "candidate description.\n"
        f"Candidate description: {desc}\n"
        f"Intent catalog: {catalog}\n"
        'Output JSON only: {"neighbors": ["id1", "id2"]}'
    )
    try:
        payload = extract_json(_invoke(llm, prompt))
    except Exception:  # noqa: BLE001
        payload = None
    if not payload:
        return [intent.id for intent in intents[:NEIGHBOR_TOP_K]]

    valid = {intent.id for intent in intents}
    picked = [str(item) for item in (payload.get("neighbors") or []) if str(item) in valid]
    return picked[:NEIGHBOR_TOP_K]


def parse_intent_decision(raw: str) -> IntentDecision | None:
    payload = extract_json(raw)
    if payload is None:
        return None
    outlet = str(payload.get("outlet", "")).strip()
    if outlet not in {"merge", "slot", "new"}:
        return None
    return IntentDecision(
        outlet=outlet,
        target_id=str(payload.get("target_id", "")).strip(),
        new_id=str(payload.get("new_id", "")).strip(),
        description=str(payload.get("description", "")).strip(),
        discriminators={
            str(k): str(v) for k, v in (payload.get("discriminators") or {}).items()
        },
        slot_key=str(payload.get("slot_key", "")).strip(),
        slot_value=str(payload.get("slot_value", "")).strip(),
        reason=str(payload.get("reason", "")).strip(),
        requires_terminal_action=(
            None
            if payload.get("requires_terminal_action") is None
            # coerce_bool rather than bare bool(): when the model outputs the string
            # "false", bool("false") == True, which would mislabel a query-class intent as
            # requiring a terminal action and from then on permanently judge every instance
            # of that intent without a terminal call as failure.
            else coerce_bool(payload["requires_terminal_action"])
        ),
    )


def adjudicate_intent(
    desc: str, aliases: list[str], taxonomy: Taxonomy, llm: Any
) -> IntentDecision:
    """Adjudicate a candidate intent that has met the threshold.

    Admission constraint: `new` can only be reached by an adjudication result the LLM gave
    explicitly -- any fallback, parse failure or downgrade path always lands on `slot`, never
    on `new`.
    """
    fallback_id = aliases[0] if aliases else "unnamed.intent"

    if taxonomy.is_empty():
        # Cold start: the taxonomy is empty, there are no neighbours to compare against, so
        # add directly and fire no LLM call at all. Note the distinction from "neighbour
        # selection returned empty" -- there the taxonomy is not empty and this path must not
        # be taken.
        return IntentDecision(
            outlet="new",
            new_id=fallback_id,
            description=desc,
            aliases=list(aliases),
            reason="the taxonomy is empty, so there are no neighbours to compare against",
        )

    neighbors = select_neighbors(desc, taxonomy, llm)
    neighbor_fallback_note = ""
    if not neighbors:
        # The taxonomy is not empty, yet neighbour selection returned empty -- the LLM judged
        # that none are close, or every id it picked was a hallucination and got filtered out.
        # This is not a cold start and must never lead to adding: fall back to the first
        # NEIGHBOR_TOP_K active intents as the neighbour set and continue through the normal
        # adjudication flow.
        neighbors = [intent.id for intent in taxonomy.active()[:NEIGHBOR_TOP_K]]
        neighbor_fallback_note = "neighbour selection came back empty, fell back to the first N active intents; "

    neighbor_records = json.dumps(
        [
            {
                "id": intent_id,
                "description": (taxonomy.get(intent_id).description if taxonomy.get(intent_id) else ""),
                "slots": (taxonomy.get(intent_id).slots if taxonomy.get(intent_id) else {}),
            }
            for intent_id in neighbors
        ],
        ensure_ascii=False,
    )
    prompt = (
        f"{ADJUDICATE_INTENT_RULES}\n"
        f"Candidate description: {desc}\n"
        f"Ids this candidate has previously used: {', '.join(aliases) or '(none)'}\n"
        f"Nearest intents: {neighbor_records}\n\n"
        "Output JSON only:\n"
        '{"outlet": "merge|slot|new", "target_id": "neighbour id (required for merge/slot)", '
        '"new_id": "object.action (required for new)", "description": "new intent description '
        '(required for new)", '
        '"discriminators": {"neighbour id": "discriminating question"}, '
        '"slot_key": "slot name (required for slot)", "slot_value": "slot value (required for '
        'slot)", '
        '"requires_terminal_action": true/false (must this intent change system state?), '
        '"reason": "rationale"}'
    )

    try:
        decision = parse_intent_decision(_invoke(llm, prompt))
    except Exception:  # noqa: BLE001
        decision = None

    if decision is None and neighbor_fallback_note:
        # Two fallbacks stacked: the neighbour set was not selected, and the adjudication
        # conclusion did not parse, so target was never really determined from start to
        # finish. Here, following the old approach and dumping the candidate's instances onto
        # neighbors[0] would amount to writing an unfamiliar candidate's trajectory into
        # another intent's SKILL.md and injecting it into all later experiments -- an error
        # both hidden and self-amplifying. The right thing is to do nothing this round and
        # leave the candidate in the ledger to be retried in the next episode.
        return IntentDecision(
            outlet="defer",
            deferred=True,
            aliases=list(aliases),
            reason=(
                f"{neighbor_fallback_note}the resolution output was also unparseable. "
                "Both fallbacks stacked and the target was never truly determined, so nothing is done this episode; the candidate stays in the ledger for the next one"
            ),
        )

    if decision is None:
        # on a parse failure take the default outlet slot, never default to creating new
        return IntentDecision(
            outlet="slot",
            target_id=neighbors[0],
            slot_key="variant",
            slot_value=fallback_id,
            aliases=list(aliases),
            reason=f"{neighbor_fallback_note}the resolution output was unparseable, so the default outlet slot is used",
        )

    if decision.outlet == "new" and not decision.new_id:
        # If the new outlet lacks a new_id, we must never fall back to creating a new entry
        # from the candidate's own alias -- that is precisely the explosion pattern of "every
        # new alias becomes its own entry". Downgrade to slot.
        decision.outlet = "slot"
        decision.target_id = neighbors[0]
        decision.reason = f"the new outlet is missing new_id, downgraded to slot; {decision.reason}"

    if decision.outlet in {"merge", "slot"} and decision.target_id not in neighbors:
        # target_id is missing or not in the neighbour set: merge is destructive (it marks
        # the source intent as merged and forwards it), so it must not be backstopped by
        # guessing a neighbour -- always force a downgrade to slot.
        original_outlet = decision.outlet
        decision.outlet = "slot"
        decision.target_id = neighbors[0]
        decision.reason = (
            f"the {original_outlet} outlet's target_id is missing or not among the neighbours, "
            f"forced down to slot; {decision.reason}"
        )

    if decision.outlet == "slot" and not decision.slot_key:
        decision.slot_key = "variant"
        decision.slot_value = fallback_id

    if neighbor_fallback_note:
        decision.reason = f"{neighbor_fallback_note}{decision.reason}"

    # every id the candidate has used is carried out, so the merge outlet can register alias
    # forwarding from it
    decision.aliases = list(aliases)
    return decision


def apply_intent_decision(decision: IntentDecision, taxonomy: Taxonomy) -> str:
    """Write the adjudication into the taxonomy and return the intent id the instances
    should belong to.

    Before writing, the `new` outlet must confirm that new_id does not yet exist: a name
    collision is not a creation but the erasure of an existing entry along with its
    description, discriminating questions, slot schema and aliases -- the discriminating
    questions are exactly the field the decomposer uses to disambiguate, and once lost they
    never grow back. A collision always downgrades to slot (this module's established
    invariant that "the default outlet is slot, never new by default"), the instances still
    go under the existing entry's name, and the reason for the downgrade is written into
    decision.reason so evolution_log keeps a trace.
    """
    if decision.deferred:
        # deferred: touch nothing in the taxonomy, return an empty id to tell the caller
        # "no attribution this round"
        return ""

    if decision.outlet == "new" and taxonomy.get(decision.new_id) is not None:
        survivor = taxonomy.resolve(decision.new_id) or decision.new_id
        fallback_value = decision.aliases[0] if decision.aliases else decision.new_id
        original_id = decision.new_id
        decision.outlet = "slot"
        decision.target_id = survivor
        decision.new_id = ""
        if not decision.slot_key:
            decision.slot_key = "variant"
            decision.slot_value = fallback_value
        decision.reason = (
            f"the new outlet's new_id `{original_id}` already exists in the taxonomy and must not be overwritten, "
            f"downgraded to a slot on {survivor}; {decision.reason}"
        )

    if decision.outlet == "new":
        taxonomy.add(
            Intent(
                id=decision.new_id,
                description=decision.description or decision.new_id,
                discriminators=decision.discriminators,
                aliases=[a for a in decision.aliases if a != decision.new_id],
                requires_terminal_action=decision.requires_terminal_action,
            )
        )
        return decision.new_id

    target = decision.target_id
    if decision.outlet == "slot":
        taxonomy.add_slot_value(target, decision.slot_key, decision.slot_value)
        return target

    # merge: the candidate may never have been admitted to the taxonomy, in which case we
    # only register alias forwarding on the target
    intent = taxonomy.get(target)
    if intent is not None:
        for alias in decision.aliases:
            if alias and alias != target and alias not in intent.aliases:
                intent.aliases.append(alias)
            existing = taxonomy.get(alias)
            if existing is not None and existing.is_active and alias != target:
                taxonomy.merge(alias, target)
    return target


@dataclass
class SlotDecision:
    outlet: str
    map_to: str = ""
    reason: str = ""


def adjudicate_slot(
    intent_id: str, key: str, value: str, taxonomy: Taxonomy, llm: Any
) -> SlotDecision:
    """Adjudicate a candidate slot that has met the threshold. The target intent is already
    fixed, so no neighbour comparison is needed."""
    intent = taxonomy.get(intent_id)
    existing = json.dumps(intent.slots if intent else {}, ensure_ascii=False)
    prompt = (
        f"{ADJUDICATE_SLOT_RULES}\n"
        f"Target intent: {intent_id}\n"
        f"Existing slot schema of that intent: {existing}\n"
        f"Candidate slot: key={key}, value={value}\n\n"
        "Output JSON only:\n"
        '{"outlet": "accept|reject", "map_to": "synonymous existing key (optional)", '
        '"reason": "rationale"}'
    )
    try:
        payload = extract_json(_invoke(llm, prompt))
    except Exception:  # noqa: BLE001
        payload = None

    if not payload or str(payload.get("outlet", "")) not in {"accept", "reject"}:
        # unparseable or an invalid outlet: always land on reject -- the conservative
        # direction, never accept by default
        return SlotDecision(outlet="reject", reason="the resolution output was unparseable, treated as reject")
    return SlotDecision(
        outlet=str(payload["outlet"]),
        map_to=str(payload.get("map_to", "")).strip(),
        reason=str(payload.get("reason", "")).strip(),
    )


def apply_slot_decision(
    intent_id: str, key: str, value: str, decision: SlotDecision, taxonomy: Taxonomy
) -> bool:
    """Write the slot adjudication into the schema and return whether the schema changed."""
    if decision.outlet == "accept":
        return taxonomy.add_slot_value(intent_id, key, value)
    if decision.outlet == "reject" and decision.map_to:
        # reject but with a map_to: write it under the synonymous existing key, which still
        # counts as a change
        return taxonomy.add_slot_value(intent_id, decision.map_to, value)
    return False


def merge_scan(
    taxonomy: Taxonomy,
    sample_texts: dict[str, list[str]],
    llm: Any,
    refusals: list[dict[str, str]] | None = None,
) -> list[tuple[str, str, float, str]]:
    """Periodically scan highly similar intent pairs and force-merge those whose
    discrimination accuracy is too low.

    Growing without merging inevitably inflates the taxonomy, so this puts an upper bound on
    its entropy.

    refusals is an optional output parameter: intent pairs blocked by the terminality hard
    constraint are appended to it for the caller to write into the evolution log. The merge
    scan is the only destructive write operation in the taxonomy, and "considered and
    refused" must be distinguishable in the log from "never considered at all" -- the former
    means the design is working, the latter that similar-pair detection failed to find it,
    and the two are handled completely differently.
    """
    intents = taxonomy.active()
    if len(intents) < 2:
        return []

    catalog = json.dumps(
        [{"id": i.id, "description": i.description} for i in intents], ensure_ascii=False
    )
    pair_prompt = (
        "Find the pairs of intents below that are semantically highly similar and "
        "therefore likely to be confused with each other.\n"
        f"Intent catalog: {catalog}\n"
        'Output JSON only: {"pairs": [["id1", "id2"]]}. Return an empty list when there '
        "are no similar pairs."
    )
    try:
        payload = extract_json(_invoke(llm, pair_prompt))
    except Exception:  # noqa: BLE001
        payload = None
    if not payload:
        return []

    valid = {intent.id for intent in intents}
    merged: list[tuple[str, str, float, str]] = []

    for pair in payload.get("pairs") or []:
        if not isinstance(pair, list) or len(pair) != 2:
            continue
        first, second = str(pair[0]), str(pair[1])
        if first not in valid or second not in valid or first == second:
            continue
        first_entry = taxonomy.get(first)
        second_entry = taxonomy.get(second)
        if (
            first_entry is None
            or not first_entry.is_active
            or second_entry is None
            or not second_entry.is_active
        ):
            # Check the active status directly rather than using resolve() -- resolve walks
            # the merged_into chain to the final active id and would still succeed for an id
            # merged away in this round, making this check a formality. Checking is_active
            # directly is what actually blocks both cases: inactive before the scan, and
            # merged away midway through this round's scan.
            continue

        # Terminality hard constraint: intents that need a state change are never merged with
        # pure-query intents, however similar their user expressions are. This is not a
        # threshold problem; adjusting the acc cut-off cannot save it.
        #
        # After a merge, all of source's instances are judged by target's
        # requires_terminal_action, and both directions are harmful: if a query is merged into
        # a state change, every instance of that query intent is judged incomplete for "no
        # terminal call" (measured: results/e1's discount.query_info and logistics.track thus
        # made the guard raise 11 false alarms in a row, 11/13 of all incomplete_claimed); if
        # a state change is merged into a query, the guard goes completely blind to that
        # intent. Experience routing is likewise misaligned -- a logistics query would
        # retrieve the SKILL.md for placing an order.
        #
        # Measured: 5 of 9 historical merges fell foul of this constraint, all of them
        # "query merged into state change": logistics.query->order.query,
        # product.check_purchase_feasibility->order.create,
        # logistics.query_progress->order.query_info, gift.query_policy->trade_in.query_rule,
        # promotion.query_rule->trade_in.query_rule.
        #
        # The test uses `is True` rather than equality: None (unlabelled) and False behave
        # identically on both the judging and the tightening paths (classify_outcome routes
        # None as False, and pipeline's one-way tightening is equally open to both), so
        # treating them as one class is what prevents blocking intents of the same kind that
        # could be merged simply because of the order in which they were labelled.
        if (first_entry.requires_terminal_action is True) != (
            second_entry.requires_terminal_action is True
        ):
            if refusals is not None:
                refusals.append({
                    "source": second,
                    "target": first,
                    "reason": (
                        f"terminality disagrees, refusing to merge: "
                        f"{second}(rta={second_entry.requires_terminal_action}) / "
                        f"{first}(rta={first_entry.requires_terminal_action})"
                    ),
                })
            # blocked before the discrimination call, which also saves this pair's LLM cost
            continue

        samples = json.dumps(
            {
                first: sample_texts.get(first, []),
                second: sample_texts.get(second, []),
            },
            ensure_ascii=False,
        )
        test_prompt = (
            "Assess whether two intents can be reliably told apart. Give an estimate of "
            "the discrimination accuracy between 0 and 1.\n"
            f"Intent A: {first}\nIntent B: {second}\n"
            f"Real user-expression samples of each: {samples}\n"
            'Output JSON only: {"accuracy": 0.0, "reason": "rationale"}'
        )
        try:
            verdict = extract_json(_invoke(llm, test_prompt))
        except Exception:  # noqa: BLE001
            verdict = None
        if not verdict:
            # A missing or unparseable estimate must not trigger a merge -- merging is
            # destructive, so the safe default is to let this pair through and leave it for
            # the next scan
            continue
        try:
            accuracy = float(verdict.get("accuracy", 1.0))
        except Exception:  # noqa: BLE001
            accuracy = 1.0
        # NaN is one of the few paths where float() does not raise, and nan >= 0.8 is always
        # False, which would defeat the "do not merge" judgement and trigger a destructive
        # merge directly. Any non-finite value is treated as 1.0 (do not merge); format-class
        # errors already fall on this safe side.
        if not math.isfinite(accuracy):
            accuracy = 1.0
        if accuracy >= DISCRIMINATION_ACCURACY_THRESHOLD:
            continue

        reason = str(verdict.get("reason", "")).strip()
        taxonomy.merge(second, first)
        merged.append((second, first, accuracy, reason))

    return merged
