"""Contrastive experience distillation.

The input is several instances of the same intent, not a single trajectory: several successes
generalize the common path, and one success plus one failure locates the failure point. With
only failed instances we do not distill -- invented experience is worse than none.
"""

from __future__ import annotations

import json
from typing import Any

from llm_retry import invoke_with_retry
from intent.prompts import DISTILL_RULES
from intent.store import ExperienceStore, Instance, InstanceStore


def common_tool_subsequence(sequences: list[list[str]]) -> list[str]:
    """Compute the longest common subsequence of several tool sequences, as the backbone of
    the experience."""
    if not sequences:
        return []
    common = sequences[0]
    for sequence in sequences[1:]:
        common = _lcs(common, sequence)
    return common


def _lcs(left: list[str], right: list[str]) -> list[str]:
    rows, cols = len(left), len(right)
    table = [[0] * (cols + 1) for _ in range(rows + 1)]
    for i in range(rows - 1, -1, -1):
        for j in range(cols - 1, -1, -1):
            if left[i] == right[j]:
                table[i][j] = table[i + 1][j + 1] + 1
            else:
                table[i][j] = max(table[i + 1][j], table[i][j + 1])
    result: list[str] = []
    i = j = 0
    while i < rows and j < cols:
        if left[i] == right[j]:
            result.append(left[i])
            i += 1
            j += 1
        elif table[i + 1][j] >= table[i][j + 1]:
            i += 1
        else:
            j += 1
    return result


def _instance_view(instance: Instance) -> dict[str, Any]:
    """The instance view handed to the LLM.

    outcome and outcome_reason must be exposed for every instance: failed instances are the
    only source of evidence for the "Common errors" section, and without marking why they count
    as failures the LLM has no way to locate the divergence point.
    """
    return {
        "outcome": instance.outcome,
        "outcome_reason": instance.outcome_reason,
        "slots": instance.slots,
        "user_text": instance.text,
        "tools": [
            {
                "name": call.name,
                "action": call.action,
                "status": call.status,
            }
            for call in instance.tools
        ],
    }


def build_distill_prompt(intent_id: str, instances: list[Instance]) -> str:
    successes = [i for i in instances if i.outcome == "success"]
    backbone = common_tool_subsequence(
        [[call.name for call in i.tools] for i in successes]
    )
    return (
        f"{DISTILL_RULES}\n"
        f"Intent id: {intent_id}\n"
        f"Common tool subsequence across successful instances (reference only): "
        f"{' -> '.join(backbone) or '(empty)'}\n"
        "All instances:\n"
        f"{json.dumps([_instance_view(i) for i in instances], ensure_ascii=False, indent=2)}\n"
    )


def distill(intent_id: str, instances: list[Instance], llm: Any) -> str | None:
    """Distill the raw experience text from several instances (the description line + body,
    not yet split). Returns None when there is no successful instance."""
    if not any(i.outcome == "success" for i in instances):
        return None
    prompt = build_distill_prompt(intent_id, instances)
    try:
        response = invoke_with_retry(
            llm, [{"role": "user", "content": prompt}], description="intent.distill"
        )
        raw = getattr(response, "content", response)
        if not isinstance(raw, str):
            return None
        body = raw
    except Exception:  # noqa: BLE001
        return None
    return body.strip() or None


def split_description(raw: str) -> tuple[str, str]:
    """Split the description line and the body out of the distilled raw text.

    Tolerant of the LLM not starting with the `description: ...` format: the whole text is
    taken as the body, description is left empty, and the write is not blocked -- format drift
    should not throw away experience that has already been distilled.
    """
    lines = raw.splitlines()
    if lines and lines[0].strip().lower().startswith("description:"):
        description = lines[0].split(":", 1)[1].strip()
        rest = "\n".join(lines[1:]).lstrip("\n")
        return description, rest
    return "", raw


def distill_and_write(
    intent_id: str,
    refs: list[str],
    instance_store: InstanceStore,
    experience_store: ExperienceStore,
    llm: Any,
) -> bool:
    """Distill and persist, returning whether anything was written.

    Instances with ambiguous_attribution true are filtered out first and enter neither the
    LLM's input nor the Evidence list: such an instance's tool calls were hard-assigned to it
    by the "excess turn" heuristic and may in fact be another intent's calls (see
    instances._assign_positional). Keeping them would let misattributed calls count as
    evidence for this intent -- whether as a successful path to imitate or written into
    "Common errors", either way teaching a causal relation unrelated to this intent. When every
    instance is doubtful there is no trustworthy evidence, and, exactly as with "only failed
    instances", no experience is produced.
    """
    instances = instance_store.load_many(refs)
    trustworthy = [
        (ref, instance)
        for ref, instance in zip(refs, instances)
        if not instance.ambiguous_attribution
    ]
    if not trustworthy:
        return False
    trusted_refs = [ref for ref, _ in trustworthy]
    trusted_instances = [instance for _, instance in trustworthy]
    raw = distill(intent_id, trusted_instances, llm)
    if raw is None:
        return False
    description, body = split_description(raw)
    experience_store.write(intent_id, description, body, trusted_refs)
    return True
