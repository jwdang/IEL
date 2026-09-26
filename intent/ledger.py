"""The candidate ledger.

It holds only unadjudicated candidates; once adjudication is done the entry is deleted
outright -- the result has been recorded in evolution_log and the taxonomy, so no status field
needs to be kept. Both kinds of entry share the same threshold and adjudication flow.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from intent.config import MIN_INSTANCES_FOR_ADJUDICATION, MIN_SUCCESS_FOR_ADJUDICATION

# Input: the new candidate description and the list of existing descriptions in the ledger;
# output: the matched index or None
DescMatcher = Callable[[str, list[str]], "int | None"]


@dataclass
class IntentCandidate:
    """A candidate intent not yet admitted to the taxonomy."""

    desc: str
    aliases: list[str] = field(default_factory=list)
    instances: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "intent",
            "desc": self.desc,
            "aliases": self.aliases,
            "instances": self.instances,
        }


@dataclass
class SlotCandidate:
    """A slot key or value newly appearing on an already-admitted intent."""

    intent: str
    key: str
    value: str
    instances: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "slot",
            "intent": self.intent,
            "key": self.key,
            "value": self.value,
            "instances": self.instances,
        }


class Ledger:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.intent_candidates: list[IntentCandidate] = []
        self.slot_candidates: list[SlotCandidate] = []

    def load(self) -> None:
        self.intent_candidates = []
        self.slot_candidates = []
        if not self.path.exists():
            return
        for item in json.loads(self.path.read_text(encoding="utf-8")):
            if item.get("type") == "slot":
                self.slot_candidates.append(
                    SlotCandidate(
                        intent=str(item["intent"]),
                        key=str(item["key"]),
                        value=str(item["value"]),
                        instances=list(item.get("instances") or []),
                    )
                )
            else:
                self.intent_candidates.append(
                    IntentCandidate(
                        desc=str(item["desc"]),
                        aliases=list(item.get("aliases") or []),
                        instances=list(item.get("instances") or []),
                    )
                )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [entry.to_dict() for entry in self.intent_candidates]
        payload.extend(entry.to_dict() for entry in self.slot_candidates)
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add_intent_candidate(
        self,
        desc: str,
        proposed_id: str,
        instance_ref: str,
        matcher: DescMatcher,
    ) -> IntentCandidate:
        """Book an entry in via semantic merging.

        String equality is not used: without a prior grid, naming necessarily drifts, and
        aggregating by string would make the count never reach the threshold, silently
        disabling the evolution mechanism.
        """
        index = matcher(desc, [entry.desc for entry in self.intent_candidates])
        if index is None:
            entry = IntentCandidate(desc=desc)
            self.intent_candidates.append(entry)
        else:
            entry = self.intent_candidates[index]
        if proposed_id and proposed_id not in entry.aliases:
            entry.aliases.append(proposed_id)
        if instance_ref not in entry.instances:
            entry.instances.append(instance_ref)
        return entry

    def add_slot_candidate(
        self, intent: str, key: str, value: str, instance_ref: str
    ) -> SlotCandidate:
        """Slot candidates aggregate by exact (intent, key, value) match, needing no semantic
        merging."""
        for entry in self.slot_candidates:
            if entry.intent == intent and entry.key == key and entry.value == value:
                if instance_ref not in entry.instances:
                    entry.instances.append(instance_ref)
                return entry
        entry = SlotCandidate(intent=intent, key=key, value=value, instances=[instance_ref])
        self.slot_candidates.append(entry)
        return entry

    def ready(
        self, outcome_of: Callable[[str], str]
    ) -> tuple[list[IntentCandidate], list[SlotCandidate]]:
        """Filter out the entries that meet the admission threshold: instance count >= 2 and
        successful instances >= 1."""

        def qualifies(refs: list[str]) -> bool:
            if len(refs) < MIN_INSTANCES_FOR_ADJUDICATION:
                return False
            successes = sum(1 for ref in refs if outcome_of(ref) == "success")
            return successes >= MIN_SUCCESS_FOR_ADJUDICATION

        return (
            [entry for entry in self.intent_candidates if qualifies(entry.instances)],
            [entry for entry in self.slot_candidates if qualifies(entry.instances)],
        )

    def remove_intent(self, candidate: IntentCandidate) -> None:
        self.intent_candidates = [e for e in self.intent_candidates if e is not candidate]

    def remove_slot(self, candidate: SlotCandidate) -> None:
        self.slot_candidates = [e for e in self.slot_candidates if e is not candidate]
