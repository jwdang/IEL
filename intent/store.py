"""Reading and writing of intent instances, experience documents and the evolution log."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable

from intent.config import IntentPaths
from intent.outcome import ToolCall


@dataclass
class Instance:
    """A concrete occurrence of some intent in one dialogue.

    We deliberately do not store is_candidate (derivable from the taxonomy and it changes
    after adjudication), turns (no consumer once persisted), or the tools' is_terminal
    (derivable from outcome.TERMINAL_ACTIONS).

    ambiguous_attribution is set by instances.py on excess turns and means the tool calls
    under this instance's name may have mixed in calls from other intents in the same turn,
    so it must not be judged success. It must be persisted: outcome is computed in the
    pipeline and then frozen, but re-running statistics/evaluation still needs to know why
    this piece of evidence does not count as success.
    """

    intent: str
    slots: dict[str, str] = field(default_factory=dict)
    text: str = ""
    tools: list[ToolCall] = field(default_factory=list)
    outcome: str = "unknown"
    outcome_reason: str = ""
    ambiguous_attribution: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent,
            "slots": self.slots,
            "text": self.text,
            "tools": [
                {
                    "name": call.name,
                    "action": call.action,
                    "status": call.status,
                }
                for call in self.tools
            ],
            "outcome": self.outcome,
            "outcome_reason": self.outcome_reason,
            "ambiguous_attribution": self.ambiguous_attribution,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Instance":
        return cls(
            intent=str(payload.get("intent", "")),
            slots={str(k): str(v) for k, v in (payload.get("slots") or {}).items()},
            text=str(payload.get("text", "")),
            tools=[
                ToolCall(
                    name=str(item.get("name", "")),
                    action=item.get("action"),
                    status=str(item.get("status", "")),
                )
                for item in (payload.get("tools") or [])
            ],
            outcome=str(payload.get("outcome", "unknown")),
            outcome_reason=str(payload.get("outcome_reason", "")),
            ambiguous_attribution=bool(payload.get("ambiguous_attribution", False)),
        )


class InstanceStore:
    """Reading and writing of instance files. ref always uses a path relative to the intent
    library root."""

    def __init__(self, paths: IntentPaths) -> None:
        self.paths = paths

    def save(self, episode_id: str, index: int, instance: Instance) -> str:
        episode_dir = self.paths.instances / episode_id
        episode_dir.mkdir(parents=True, exist_ok=True)
        target = episode_dir / f"{index}.json"
        target.write_text(
            json.dumps(instance.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return f"instances/{episode_id}/{index}.json"

    def load(self, ref: str) -> Instance:
        payload = json.loads((self.paths.root / ref).read_text(encoding="utf-8"))
        return Instance.from_dict(payload)

    def load_many(self, refs: list[str]) -> list[Instance]:
        return [self.load(ref) for ref in refs]

    def all_refs(self) -> list[str]:
        if not self.paths.instances.exists():
            return []
        files = sorted(self.paths.instances.glob("*/*.json"))
        return [f"instances/{f.parent.name}/{f.name}" for f in files]

    def refs_for_intent(
        self, intent_id: str, resolve: "Callable[[str], str | None] | None" = None
    ) -> list[str]:
        """Return the instance refs belonging to this intent.

        When resolve is passed Taxonomy.resolve, each instance record's intent is first
        resolved to the currently surviving canonical id before comparison: the historical
        instances of a merged-away intent thus automatically hang under the surviving target's
        name instead of going missing along with the merge (losing evidence on every merge
        would amount to deleting a batch of data each time).

        We chose "resolve at read time" over "rewrite the instance files": instances are this
        system's only raw evidence, and rewriting is destructive and irreversible -- one wrong
        merge would permanently tamper with historical instances and there would be no way
        back afterwards; read-time resolution is fully reversible, takes effect the moment the
        merge chain changes, and costs only one extra dict lookup each time (taxonomy size
        < 50, negligible).

        The queried id itself is deliberately not resolved: passing in an already merged-away
        dead id simply yields an empty list, keeping dead ids from continuing to serve as valid
        lookup keys. Without resolve, behaviour is exactly as before, and candidate ids not yet
        admitted to the taxonomy still match literally.
        """
        matched: list[str] = []
        for ref in self.all_refs():
            stored = self.load(ref).intent
            canonical = (resolve(stored) if resolve is not None else None) or stored
            if canonical == intent_id:
                matched.append(ref)
        return matched


class ExperienceStore:
    """Experience documents organized by intent id."""

    def __init__(self, paths: IntentPaths) -> None:
        self.paths = paths

    def _path(self, intent_id: str):
        return self.paths.experiences / intent_id / "SKILL.md"

    def exists(self, intent_id: str) -> bool:
        return self._path(intent_id).exists()

    def read(self, intent_id: str) -> str | None:
        path = self._path(intent_id)
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8")

    def write(
        self, intent_id: str, description: str, body: str, evidence: list[str]
    ) -> None:
        """Persist as the unified skill structure: frontmatter (name/description) + body.

        description is the "light" layer of progressive disclosure -- what is shown to the
        LLM during decomposition is actually Intent.description in taxonomy.yaml, not this
        one; this description only makes SKILL.md self-describing and keeps it consistent with
        the shape of a standard skill file.
        """
        path = self._path(intent_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        evidence_block = "\n".join(f"- {ref}" for ref in evidence)
        document = (
            f"---\nname: {intent_id}\ndescription: {description}\n---\n\n"
            f"{body.strip()}\n\n## Evidence\n{evidence_block}\n"
        )
        path.write_text(document, encoding="utf-8")


class EvolutionLog:
    """The decision stream of taxonomy evolution, one JSON object per line."""

    def __init__(self, paths: IntentPaths) -> None:
        self.paths = paths

    def append(self, record: dict[str, Any]) -> None:
        self.paths.evolution_log.parent.mkdir(parents=True, exist_ok=True)
        with self.paths.evolution_log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def read_all(self) -> list[dict[str, Any]]:
        if not self.paths.evolution_log.exists():
            return []
        lines = self.paths.evolution_log.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines if line.strip()]
