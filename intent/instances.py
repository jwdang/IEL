"""Intent instance reconstruction.

At runtime everything is split turn by turn, but an intent often spans several turns, while
the unit experience is distilled from is the complete instance. This module merges the
per-turn decomposition results into instances and attributes tool calls to specific intents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from intent.outcome import ToolCall
from intent.store import Instance


@dataclass
class TurnDecomposition:
    """The decomposition result of one user message.

    user_message is that turn's raw user message, used only to reconstruct the true order in
    which multiple intents appear in the message (see _turn_intent_ids); when it is
    unavailable we fall back to the existing order.
    """

    turn_index: int
    matched: list[dict[str, Any]] = field(default_factory=list)
    candidates: list[dict[str, Any]] = field(default_factory=list)
    user_message: str = ""


def _turn_intent_ids(turn: TurnDecomposition) -> list[tuple[str, dict[str, str], str]]:
    """Return this turn's (intent id, slots, source span) in order of appearance.

    matched and candidates are two independent lists emitted by the decomposer, and simply
    concatenating them would order a message where "the candidate appears first and the match
    later" wrongly, which in turn aligns tool calls to the wrong intents. Here we reorder by
    each entry's span position in the raw user message to reconstruct the true order of
    appearance; entries whose span is empty or cannot be found in the message are always
    placed last, with a stable sort keeping their relative order -- better to fall back to the
    old order than to guess. Without a user_message we likewise fall back to the old order
    (matched first).
    """
    items: list[tuple[str, dict[str, str], str]] = []
    for item in turn.matched:
        intent_id = str(item.get("id", "")).strip()
        if intent_id:
            items.append((intent_id, dict(item.get("slots") or {}), str(item.get("span", ""))))
    for item in turn.candidates:
        intent_id = str(item.get("proposed_id", "")).strip()
        if intent_id:
            items.append((intent_id, dict(item.get("slots") or {}), str(item.get("span", ""))))

    message = turn.user_message or ""
    if not message or len(items) < 2:
        return items

    fallback_position = len(message) + 1

    def position(entry: tuple[str, dict[str, str], str]) -> int:
        span = entry[2]
        if not span:
            return fallback_position
        found = message.find(span)
        return found if found >= 0 else fallback_position

    return sorted(items, key=position)


def _assign_positional(
    intent_ids: list[str], calls: list[dict[str, Any]]
) -> tuple[dict[str, list[dict[str, Any]]], set[str]]:
    """Align one turn's tool calls to that turn's intents, in order.

    Returns (attribution table, set of intent ids with doubtful attribution). The
    attribution rules, in priority order:

    1. Single-intent turn: all calls go to it, attribution is certain.
    2. Multi-intent turn with call count <= intent count: align one-to-one in order of
       appearance; the later intents may get no calls (they may genuinely not have been
       handled yet this turn).
    3. Multi-intent turn with call count > intent count (an excess turn): the first n-1 calls
       align positionally to the first n-1 intents, and all the rest go to the **last**
       intent. The agent usually finishes one intent before starting the next, so a run of
       calls at the tail most likely belongs to the last intent.

    Rule 3 replaces the old implementation's "discard the extra calls". Discarding looks
    conservative but is actually the most dangerous option: an intent that genuinely triggered
    a terminal call would have its terminal call thrown away with the rest, thereby bypassing
    outcome.py's terminal-call requirement and falling into the lenient query-class branch to
    be judged success on someone else's query evidence -- and the terminal-call requirement is
    the main line of defence keeping wrong trajectories from being crystallized.

    Failure mode (which must be explicitly acknowledged): rule 3's tail merging is only a
    heuristic, and an excess call does not necessarily belong to the last intent. So the
    intent that absorbed the excess calls is flagged as having doubtful attribution, and
    classify_outcome always refuses to grant success to a doubtful instance -- better to have
    one fewer piece of success evidence than to manufacture evidence out of ambiguity. The
    first n-1 intents get exactly the same positional alignment as rule 2, with no extra doubt.
    """
    if not intent_ids:
        return {}, set()
    if len(intent_ids) == 1:
        return {intent_ids[0]: list(calls)}, set()

    assigned: dict[str, list[dict[str, Any]]] = {intent_id: [] for intent_id in intent_ids}
    ambiguous: set[str] = set()
    last_index = len(intent_ids) - 1

    if len(calls) <= len(intent_ids):
        for position, call in enumerate(calls):
            assigned[intent_ids[position]].append(call)
        return assigned, ambiguous

    for position, call in enumerate(calls):
        target = intent_ids[min(position, last_index)]
        assigned[target].append(call)
    ambiguous.add(intent_ids[last_index])
    return assigned, ambiguous


def _to_tool_call(call: dict[str, Any]) -> ToolCall:
    parameters = call.get("parameters") or {}
    action = parameters.get("action") if isinstance(parameters, dict) else None
    return ToolCall(
        name=str(call.get("tool_name", "")),
        action=str(action) if action else None,
        status=str(call.get("status", "")),
    )


def _assign_turns(
    turns: list[TurnDecomposition], tool_calls: list[dict[str, Any]]
) -> list[
    tuple[
        list[tuple[str, dict[str, str], str]],
        dict[str, list[dict[str, Any]]],
        set[str],
    ]
]:
    """Do one attribution pass per turn, returning a list of (this turn's intent entries,
    attribution table, ambiguity set)."""
    calls_by_turn: dict[int, list[dict[str, Any]]] = {}
    for call in tool_calls:
        calls_by_turn.setdefault(int(call.get("turn_index", -1)), []).append(call)

    assignments: list[
        tuple[
            list[tuple[str, dict[str, str], str]],
            dict[str, list[dict[str, Any]]],
            set[str],
        ]
    ] = []
    last_items: Optional[
        list[tuple[str, dict[str, str], str]]
    ] = None
    for turn in turns:
        items = _turn_intent_ids(turn)
        if not items:
            # No intent decomposition this turn (e.g. the user only replied with a
            # confirmation, and the LLM produced no intent). The tool calls really happened --
            # they may be the terminal execution of the previous turn's request. We must not
            # discard them just because this turn has no intents: what would be discarded is
            # exactly the terminal call outcome/guard judging needs, which would misjudge a
            # successful execution as incomplete/failure (measured: on the turn where the user
            # confirmed "Sunday home visit works", there was no intent, the agent's successful
            # schedule_service_tool was dropped, and the guard then misjudged it and failed to
            # complete it).
            # Inherit to the most recent turn that had intents, reusing the same positional
            # alignment rules; if the whole episode has no intents there is nothing to
            # attribute to, and they stay discarded.
            calls = calls_by_turn.get(turn.turn_index, [])
            if last_items is not None and calls:
                # Inherited calls all go to the **last** intent of the preceding turn: a turn
                # with no intents is usually an execution turn after a conversational
                # confirmation, and the agent's action belongs to the most recent active
                # intent. We cannot use _assign_calls' positional alignment -- when the call
                # count <= the intent count it would misattribute the terminal call to an
                # earlier intent, leaving the last intent without it (measured on task 15:
                # schedule_service_tool was attributed to a query-class intent, and the booking
                # intent was still judged incomplete).
                last_id = last_items[-1][0]
                assignments.append((last_items, {last_id: list(calls)}, set()))
            continue
        last_items = items
        intent_ids = [intent_id for intent_id, _, _ in items]
        assigned, ambiguous = _assign_positional(
            intent_ids, calls_by_turn.get(turn.turn_index, [])
        )
        assignments.append((items, assigned, ambiguous))
    return assignments


def build_instances(
    turns: list[TurnDecomposition], tool_calls: list[dict[str, Any]]
) -> list[Instance]:
    """Merge the per-turn decomposition results into intent instances. outcome is filled in
    later by the caller."""
    order: list[str] = []
    merged: dict[str, Instance] = {}

    for items, assigned, ambiguous in _assign_turns(turns, tool_calls):
        for intent_id, slots, span in items:
            if intent_id not in merged:
                merged[intent_id] = Instance(intent=intent_id)
                order.append(intent_id)
            instance = merged[intent_id]
            # ambiguity only accumulates: once one turn dumped excess calls on it, the whole
            # instance is no longer trustworthy
            if intent_id in ambiguous:
                instance.ambiguous_attribution = True
            instance.slots.update({str(k): str(v) for k, v in slots.items()})
            if span:
                instance.text = f"{instance.text}\n{span}".strip()
            instance.tools.extend(
                _to_tool_call(call) for call in assigned.get(intent_id, [])
            )

    return [merged[intent_id] for intent_id in order]
