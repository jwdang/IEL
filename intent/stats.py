"""Structured statistics over scenarios.

The statistics aggregate only slot keys and values already admitted into the taxonomy schema
-- unadmitted candidate slots suffer from synonyms splitting keys and values, and counting them
would distort the figures.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from intent.outcome import is_terminal_call
from intent.store import Instance, InstanceStore
from intent.taxonomy import Taxonomy


def intent_distribution(instance_store: InstanceStore) -> dict[str, int]:
    """The distribution of instance counts across intents."""
    counter: Counter[str] = Counter()
    for ref in instance_store.all_refs():
        counter[instance_store.load(ref).intent] += 1
    return dict(counter)


def slot_distribution(
    instance_store: InstanceStore, taxonomy: Taxonomy, intent_id: str
) -> dict[str, dict[str, int]]:
    """The value distribution of each slot within a single intent."""
    intent = taxonomy.get(intent_id)
    if not intent:
        return {}
    result: dict[str, Counter[str]] = defaultdict(Counter)

    # pass resolve: the instances of merged-away intents now sit under the surviving target's
    # name, and the counting standard must be consistent
    for ref in instance_store.refs_for_intent(intent_id, resolve=taxonomy.resolve):
        instance = instance_store.load(ref)
        for key, value in instance.slots.items():
            if key in intent.slots and value in intent.slots[key]:
                result[key][value] += 1
    return {key: dict(counter) for key, counter in result.items()}


def slot_outcome_crosstab(
    instance_store: InstanceStore, taxonomy: Taxonomy, intent_id: str, key: str
) -> dict[str, dict[str, int]]:
    """A slot-value x outcome cross-tab, used to locate which kinds of scenario fail more
    often."""
    intent = taxonomy.get(intent_id)
    if intent is None or key not in intent.slots:
        return {}

    admitted_values = set(intent.slots[key])
    table: dict[str, Counter[str]] = defaultdict(Counter)
    for ref in instance_store.refs_for_intent(intent_id, resolve=taxonomy.resolve):
        instance = instance_store.load(ref)
        value = instance.slots.get(key)
        if value is not None and value in admitted_values:
            table[value][instance.outcome] += 1
    return {value: dict(counter) for value, counter in table.items()}


def intents_per_message(turns_per_episode: dict[str, list[int]]) -> dict[int, int]:
    """The distribution of intent counts per user message, directly quantifying how large
    multi-intent messages are."""
    counter: Counter[int] = Counter()
    for counts in turns_per_episode.values():
        for count in counts:
            counter[count] += 1
    return dict(counter)


def terminality_coverage_by_episode(
    refs: list[str], instances_by_ref: dict[str, Instance], taxonomy: Taxonomy
) -> dict[str, float]:
    """Terminality coverage grouped by episode (the share of instances whose intent has a
    terminality label).

    The taxonomy grows as the run proceeds and coverage rises with it; without reporting
    grouped by episode, a cross-episode comparison would mix in coverage differences rather
    than method differences.
    """
    totals: dict[str, int] = {}
    covered: dict[str, int] = {}
    for ref in refs:
        instance = instances_by_ref.get(ref)
        if instance is None:
            continue
        episode = ref.split("/")[1]
        totals[episode] = totals.get(episode, 0) + 1
        canonical = taxonomy.resolve(instance.intent) or instance.intent
        entry = taxonomy.get(canonical)
        if entry is not None and entry.requires_terminal_action is not None:
            covered[episode] = covered.get(episode, 0) + 1
    return {ep: covered.get(ep, 0) / count for ep, count in totals.items()}


def suspect_terminality_labels(
    taxonomy: Taxonomy, instances_by_intent: dict[str, list[Instance]]
) -> list[str]:
    """Intents labelled true for which no successful terminal call was ever observed, for
    manual review.

    The section 4.3 one-way correction can only tighten false/null to true; it cannot correct a
    pure-query intent that was wrongly labelled true -- that would make every instance of the
    intent permanently judged failure.
    """
    suspects: list[str] = []
    for intent in taxonomy.active():
        if intent.requires_terminal_action is not True:
            continue
        # Doubtfully attributed instances must be excluded: that is exactly how the wrong
        # labelling arose. Measured: discount.query_info and logistics.track were each tightened
        # to true by one ambiguous_attribution instance, and the terminal call under that
        # instance then in turn became evidence that "the label is right" -- this list is the
        # only outlet for a mislabel, and endorsing it with the very evidence that created the
        # mislabel would close that outlet for good.
        observed = any(
            is_terminal_call(call.name, call.action) and call.ok
            for instance in instances_by_intent.get(intent.id, [])
            if not instance.ambiguous_attribution
            for call in instance.tools
        )
        if not observed:
            suspects.append(intent.id)
    return sorted(suspects)


def render_report(instance_store: InstanceStore, taxonomy: Taxonomy) -> str:
    lines = ["# Intent library statistics", "", "## Instances per intent"]
    distribution = intent_distribution(instance_store)
    for intent_id, count in sorted(distribution.items(), key=lambda kv: -kv[1]):
        lines.append(f"- {intent_id}: {count}")

    lines.extend(["", "## Slot distribution per intent"])
    for intent in taxonomy.active():
        slots = slot_distribution(instance_store, taxonomy, intent.id)
        if not slots:
            continue
        lines.append(f"### {intent.id}")
        for key, values in slots.items():
            rendered = ", ".join(f"{v}={c}" for v, c in sorted(values.items()))
            lines.append(f"- {key}: {rendered}")

    all_refs = instance_store.all_refs()
    instances_by_ref = {ref: instance_store.load(ref) for ref in all_refs}
    all_instances = list(instances_by_ref.values())

    lines.extend(["", "## Terminality coverage (by episode)"])
    for episode, coverage in sorted(
        terminality_coverage_by_episode(all_refs, instances_by_ref, taxonomy).items()
    ):
        lines.append(f"- {episode}: {coverage:.2%}")

    by_intent: dict[str, list[Instance]] = {}
    for instance in all_instances:
        canonical = taxonomy.resolve(instance.intent) or instance.intent
        by_intent.setdefault(canonical, []).append(instance)
    suspects = suspect_terminality_labels(taxonomy, by_intent)
    if suspects:
        lines.extend(["", "## Intents suspected of being mislabelled as requiring a terminal action (pending manual review)"])
        lines.extend(f"- {intent_id}" for intent_id in suspects)

    return "\n".join(lines) + "\n"
