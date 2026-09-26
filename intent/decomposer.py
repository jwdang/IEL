"""Runtime intent decomposition and taxonomy matching.

Prompt construction and output parsing are split into pure functions, so they can be unit
tested without an LLM; decompose() only wires the two together with one LLM call.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from llm_retry import invoke_with_retry
from intent.jsonio import extract_json
from intent.prompts import (
    DECOMPOSE_EXAMPLES,
    DECOMPOSE_OUTPUT_SCHEMA,
    DECOMPOSE_RULES,
)
from intent.taxonomy import Taxonomy


@dataclass
class Matched:
    id: str
    slots: dict[str, str] = field(default_factory=dict)
    span: str = ""


@dataclass
class Candidate:
    """A candidate intent. Two sources: the candidates the LLM gives directly, and items in
    matched that carry an id the taxonomy does not have (most likely a format error, or the
    model wanted to propose a new intent but used the wrong field).

    Being in matched itself requires a "certain match" (see DECOMPOSE_RULES), so there is no
    "matched but not certain enough" tier -- when the LLM is unsure it should emit nothing
    rather than downgrade.
    """

    proposed_id: str
    desc: str = ""
    slots: dict[str, str] = field(default_factory=dict)
    span: str = ""
    # Whether this came from an item in matched whose id the taxonomy does not have, used to
    # distinguish it from a candidate the LLM gave directly.
    from_matched: bool = False


@dataclass
class DecomposeResult:
    matched: list[Matched] = field(default_factory=list)
    candidates: list[Candidate] = field(default_factory=list)
    non_transactional: list[str] = field(default_factory=list)


def _taxonomy_view(taxonomy: Taxonomy) -> str:
    intents = taxonomy.active()
    if not intents:
        return "(the taxonomy is empty)"
    records = [
        {
            "id": intent.id,
            "description": intent.description,
            "discriminators": intent.discriminators,
            "negative_triggers": intent.negative_triggers,
            "slots": intent.slots,
        }
        for intent in intents
    ]
    return json.dumps(records, ensure_ascii=False)


def build_decompose_prompt(
    user_message: str,
    recent_context: str,
    taxonomy: Taxonomy,
    tool_names: list[str],
) -> str:
    return (
        f"{DECOMPOSE_RULES}\n"
        f"{DECOMPOSE_EXAMPLES}\n"
        f"{DECOMPOSE_OUTPUT_SCHEMA}\n"
        "Current intent taxonomy:\n"
        f"<taxonomy>{_taxonomy_view(taxonomy)}</taxonomy>\n\n"
        "Available tools in the current environment:\n"
        f"<tools>{', '.join(tool_names) or '(none)'}</tools>\n\n"
        "Recent dialogue context:\n"
        f"<context>{recent_context or '(none)'}</context>\n\n"
        "Current user message:\n"
        f"<message>{user_message}</message>\n"
    )


def _coerce_slots(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {str(k): str(v) for k, v in value.items()}


def parse_decompose_output(raw: str, taxonomy: Taxonomy) -> DecomposeResult:
    payload = extract_json(raw)
    if payload is None:
        return DecomposeResult()

    result = DecomposeResult()

    # guard the matched field: only iterate once it is confirmed to be a list
    matched_items = payload.get("matched")
    if not isinstance(matched_items, list):
        matched_items = []

    for item in matched_items:
        if not isinstance(item, dict):
            continue
        raw_id = str(item.get("id", "")).strip()
        span = str(item.get("span", ""))
        slots = _coerce_slots(item.get("slots"))

        canonical = taxonomy.resolve(raw_id) if raw_id else None
        if canonical is None:
            # any id absent from the taxonomy is turned into a candidate, never let into matched
            result.candidates.append(
                Candidate(
                    proposed_id=raw_id, desc="", slots=slots, span=span,
                    from_matched=True,
                )
            )
            continue
        result.matched.append(Matched(id=canonical, slots=slots, span=span))

    # guard the candidates field: only iterate once it is confirmed to be a list
    candidates_items = payload.get("candidates")
    if not isinstance(candidates_items, list):
        candidates_items = []

    for item in candidates_items:
        if not isinstance(item, dict):
            continue
        result.candidates.append(
            Candidate(
                proposed_id=str(item.get("proposed_id", "")).strip(),
                desc=str(item.get("desc", "")).strip(),
                slots=_coerce_slots(item.get("slots")),
                span=str(item.get("span", "")),
            )
        )

    # guard the non_transactional field: only iterate once it is confirmed to be a list
    nontrans_items = payload.get("non_transactional")
    if not isinstance(nontrans_items, list):
        nontrans_items = []

    for item in nontrans_items:
        result.non_transactional.append(str(item))

    return result


def decompose(
    llm: Any,
    user_message: str,
    recent_context: str,
    taxonomy: Taxonomy,
    tool_names: list[str],
) -> DecomposeResult:
    """One LLM call does both decomposition and matching. On failure it returns an empty
    result without affecting the main flow."""
    prompt = build_decompose_prompt(user_message, recent_context, taxonomy, tool_names)
    try:
        response = invoke_with_retry(
            llm, [{"role": "user", "content": prompt}], description="intent.decompose"
        )
        raw = getattr(response, "content", response)
        if not isinstance(raw, str):
            raw = str(raw)
        return parse_decompose_output(raw, taxonomy)
    except Exception:  # noqa: BLE001
        return DecomposeResult()
