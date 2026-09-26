"""The data structure and persistence of the intent taxonomy.

The taxonomy is stored as YAML and keyed by intent ids of the form `object.action`.
Which words are used for object/action is decided by the data; no domain constraint is imposed
here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

MERGED_PREFIX = "merged_into:"


@dataclass
class Intent:
    """An intent entry in the taxonomy."""

    id: str
    description: str
    discriminators: dict[str, str] = field(default_factory=dict)
    slots: dict[str, list[str]] = field(default_factory=dict)
    negative_triggers: list[str] = field(default_factory=list)
    status: str = "active"
    aliases: list[str] = field(default_factory=list)
    # None means not yet labelled (the default when migrating historical entries). Judging
    # routes it as False, but it must be recorded in outcome_reason -- silently treating it as
    # True would turn every historical query-class intent into a failure overnight. Tightening
    # can only be done by the section 4.3 one-way correction.
    requires_terminal_action: bool | None = None

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    @property
    def merged_into(self) -> str | None:
        if self.status.startswith(MERGED_PREFIX):
            return self.status[len(MERGED_PREFIX):]
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "discriminators": self.discriminators,
            "slots": self.slots,
            "negative_triggers": self.negative_triggers,
            "status": self.status,
            "aliases": self.aliases,
            "requires_terminal_action": self.requires_terminal_action,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Intent":
        return cls(
            id=str(payload["id"]),
            description=str(payload.get("description", "")),
            discriminators=dict(payload.get("discriminators") or {}),
            slots={k: list(v) for k, v in (payload.get("slots") or {}).items()},
            negative_triggers=list(payload.get("negative_triggers") or []),
            status=str(payload.get("status", "active")),
            aliases=list(payload.get("aliases") or []),
            requires_terminal_action=(
                None
                if payload.get("requires_terminal_action") is None
                else bool(payload["requires_terminal_action"])
            ),
        )


class Taxonomy:
    """The intent taxonomy: reading/writing, alias resolution and slot schema maintenance."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self._intents: dict[str, Intent] = {}

    def load(self) -> None:
        self._intents = {}
        if not self.path.exists():
            return
        raw = yaml.safe_load(self.path.read_text(encoding="utf-8")) or []
        for item in raw:
            intent = Intent.from_dict(item)
            self._intents[intent.id] = intent

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [intent.to_dict() for intent in self._intents.values()]
        self.path.write_text(
            yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

    def is_empty(self) -> bool:
        return not self.active()

    def active(self) -> list[Intent]:
        return [intent for intent in self._intents.values() if intent.is_active]

    def get(self, intent_id: str) -> Intent | None:
        return self._intents.get(intent_id)

    def resolve(self, intent_id: str) -> str | None:
        """Resolve any id or alias to the currently active canonical id."""
        intent = self._intents.get(intent_id)
        if intent is None:
            for candidate in self._intents.values():
                if intent_id in candidate.aliases:
                    intent = candidate
                    break
        if intent is None:
            return None
        # walk forward along the merged_into chain, at most 10 hops to guard against cycles
        for _ in range(10):
            if intent.is_active:
                return intent.id
            target = intent.merged_into
            if target is None or target not in self._intents:
                return None
            intent = self._intents[target]
        return None

    def add(self, intent: Intent) -> None:
        """Add an intent. Errors outright when the id already exists; never overwrites.

        A bare assignment would let any call site that mistypes an id silently erase a whole
        existing entry (description, discriminating questions, slot schema, aliases) leaving no
        trace. Pushing the invariant down into the data structure itself makes it impossible for
        call sites to bypass it. To modify an existing entry, directly modify the object
        returned by get(), or go through merge()/add_slot_value().
        """
        if intent.id in self._intents:
            raise ValueError(
                f"intent {intent.id} already exists, add() does not allow overwriting an existing entry"
            )
        self._intents[intent.id] = intent

    def merge(self, source_id: str, target_id: str) -> None:
        """Merge source into target, setting source to merged status while keeping forwarding."""
        if source_id not in self._intents:
            raise KeyError(f"unknown source intent: {source_id}")
        if target_id not in self._intents:
            raise KeyError(f"unknown target intent: {target_id}")
        source = self._intents[source_id]
        target = self._intents[target_id]
        source.status = f"{MERGED_PREFIX}{target_id}"
        for alias in [source_id, *source.aliases]:
            if alias not in target.aliases and alias != target_id:
                target.aliases.append(alias)

    def add_slot_value(self, intent_id: str, key: str, value: str) -> bool:
        """Write a slot value into the schema, returning False when it already exists."""
        intent = self._intents.get(intent_id)
        if intent is None:
            raise KeyError(f"unknown intent: {intent_id}")
        values = intent.slots.setdefault(key, [])
        if value in values:
            return False
        values.append(value)
        return True

    def unknown_slots(self, intent_id: str, slots: dict[str, Any]) -> list[tuple[str, str]]:
        """Return the list of (key, value) pairs not in this intent's schema."""
        intent = self._intents.get(intent_id)
        if intent is None:
            return [(str(k), str(v)) for k, v in slots.items()]
        unknown: list[tuple[str, str]] = []
        for key, value in slots.items():
            text_value = str(value)
            if key not in intent.slots or text_value not in intent.slots[key]:
                unknown.append((str(key), text_value))
        return unknown
