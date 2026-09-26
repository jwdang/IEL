"""Parsing of LLM structured output.

Decomposition, admission adjudication and signal judging all ask the model to "output JSON
only", and all face the same thing: the model sometimes ignores that instruction and wraps
its result in a ```json fence. Keeping a word-for-word identical implementation in each of the
three modules would amount to duplicating the judgement of "which malformed outputs do we
tolerate" three times -- changing only one of them later would silently make the other two
stricter or looser, and that difference would show up only as "some module occasionally fails
to parse", which is extremely hard to attribute.
"""

from __future__ import annotations

import json
from typing import Any


def coerce_bool(value: Any, default: bool = False) -> bool:
    """Normalize booleans in LLM output.

    The model's JSON output occasionally writes true/false as strings ("false", "no", etc.).
    bool("false") == True, so loose type coercion would invert the signal in the wrong
    direction -- inverting verifier's negative_signal would turn a successful instance into a
    failure; inverting requires_terminal_action would make every instance of a query-class
    intent permanently judged failure, and the one-way tightening cannot be undone. Here we
    converge uniformly on the truth table, and unrecognized values fall back to default (the
    conservative direction).
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "1", "yes", "y", "on"}:
            return True
        if text in {"false", "0", "no", "n", "off", ""}:
            return False
    return default


def extract_json(raw: str) -> dict[str, Any] | None:
    """Extract a JSON object from the LLM's raw output, tolerating a ```json code-block wrapper.

    Try parsing as-is first, and on failure fall back to stripping the fence and retrying; if
    both fail, return None -- on which the caller treats this round's judgement as an empty
    result (decomposition falls back to empty, adjudication takes the default outlet slot,
    the verifier does not intervene), rather than letting one format drift interrupt the whole
    episode.
    """
    texts = [raw]
    if "```" in raw:
        start = raw.find("```")
        end = raw.rfind("```")
        if end > start:
            block = raw[start + 3 : end].strip()
            if block.startswith("json"):
                block = block[4:].strip()
            texts.append(block)
    for text in texts:
        try:
            parsed = json.loads(text)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(parsed, dict):
            return parsed
    return None
