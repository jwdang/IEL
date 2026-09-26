"""The six-step pipeline that runs at the end of an episode.

Order: instance reconstruction -> outcome judging -> candidate bookkeeping -> admission
adjudication -> contrastive distillation -> periodic merge scan.
Ground-truth labels are never read anywhere: judging relies only on signals observable
within the trajectory. Execution is serial, with no concurrency protection.
"""

from __future__ import annotations

import json
from typing import Any

from llm_retry import invoke_with_retry
from intent.adjudicator import (
    adjudicate_intent,
    adjudicate_slot,
    apply_intent_decision,
    apply_slot_decision,
    merge_scan,
)
from intent.config import (
    IntentPaths,
    MERGE_SCAN_EVERY_N_EPISODES,
    MIN_TERMINAL_SUPPORT,
)
from intent.distiller import distill_and_write
from intent.instances import TurnDecomposition, build_instances
from intent.ledger import Ledger
from intent.outcome import classify_outcome, is_terminal_call
from intent.store import EvolutionLog, ExperienceStore, Instance, InstanceStore
from intent.taxonomy import Taxonomy


def _has_clean_terminal_call(instance: Instance) -> bool:
    """Whether this instance carries a successful terminal call "usable as terminality
    evidence".

    Two-fold exclusion: failed calls, and instances with doubtful attribution (which do not
    even qualify for a success verdict, see classify_outcome).
    """
    if instance.ambiguous_attribution:
        return False
    return any(
        is_terminal_call(call.name, call.action) and call.ok
        for call in instance.tools
    )


def _match_desc(llm: Any):
    """Build the ledger's semantic-merge function."""

    def matcher(desc: str, existing: list[str]) -> int | None:
        if not existing:
            return None
        if desc in existing:
            # The descriptions are exactly equal: identity can be decided without semantic
            # adjudication, so skip the LLM call. This does not violate the Ledger docstring's
            # warning against "using string equality" -- that constraint targets synonymous
            # descriptions after drift, and the trivial case of exact equality needs no LLM.
            return existing.index(desc)
        prompt = (
            "Determine whether the new candidate and one of the existing Candidate "
            "Ledger descriptions denote the same business intent.\n"
            f"New candidate: {desc}\n"
            f"Existing candidate descriptions: {json.dumps(existing, ensure_ascii=False)}\n"
            'Output JSON only: {"match_index": integer index or null}'
        )
        try:
            response = invoke_with_retry(
                llm, [{"role": "user", "content": prompt}], description="intent.match_desc"
            )
            raw = getattr(response, "content", response)
            payload = json.loads(raw if isinstance(raw, str) else str(raw))
            index = payload.get("match_index")
        except Exception:  # noqa: BLE001
            return None
        if isinstance(index, int) and 0 <= index < len(existing):
            return index
        return None

    return matcher


def run_episode_pipeline(
    episode_id: str,
    turns: list[TurnDecomposition],
    tool_calls: list[dict[str, Any]],
    paths: IntentPaths,
    llm: Any,
    episode_counter: int,
    signals: dict[str, dict[str, bool]] | None = None,
    evolve: bool = True,
    instance_sink: IntentPaths | None = None,
) -> dict[str, Any]:
    """instance_sink: where instances are persisted, defaulting to the same place as paths.

    The frozen evaluation stage (evolve=False) must write instances to a metrics directory
    outside the library: all of the paper's mechanism metrics come from instances, so
    nothing can be collected if they are not persisted; and the frozen library is the shared
    read-only measuring instrument of every evaluation arm, while the evaluation stage runs
    concurrently, so writing into the library would let the arms pollute each other. The
    taxonomy is still read from paths -- steps one/two need requires_terminal_action to
    judge outcome.

    signals: the per-instance negative_signal / repeated_query judged by verifier, looked up
    by intent id; when absent, or when the entry cannot be found, it is always treated as
    False -- better to miss a judgment than to manufacture a failure out of a missing value.
    """
    paths.ensure()
    taxonomy = Taxonomy(paths.taxonomy)
    taxonomy.load()
    ledger = Ledger(paths.ledger)
    ledger.load()
    if instance_sink is not None:
        instance_sink.ensure()
    instance_store = InstanceStore(instance_sink or paths)
    experience_store = ExperienceStore(paths)
    evolution_log = EvolutionLog(paths)

    # Step one + two: instance reconstruction and outcome judging
    instances = build_instances(turns, tool_calls)
    signals = signals or {}
    refs: list[tuple[str, Instance]] = []
    # For instances of ledger candidates (whose canonical does not yet exist in the
    # taxonomy), requires_terminal_action is necessarily None when judged here -- their
    # target intent is only determined after admission in step four.
    # negative_signal/repeated_query are not persisted (Instance has no such fields), so a
    # copy must be kept here, for step four to re-judge these "created within this episode"
    # instances once it has the authoritative requires_terminal_action; see the
    # pending_signals consumption point below. Candidate instances from across episodes
    # (produced by a previous pipeline call, only now reaching the threshold) are not in
    # this dict and are not re-judged this round -- that is the scope Track B explicitly
    # draws, and we do not pretend here to be able to fix historical evidence off disk.
    pending_signals: dict[str, tuple[bool, bool]] = {}
    for index, instance in enumerate(instances):
        canonical = taxonomy.resolve(instance.intent) or instance.intent
        entry = taxonomy.get(canonical)
        judged = signals.get(instance.intent) or {}
        negative_signal = bool(judged.get("negative_signal", False))
        repeated_query = bool(judged.get("repeated_query", False))
        instance.outcome, instance.outcome_reason = classify_outcome(
            instance.tools,
            negative_signal=negative_signal,
            repeated_query=repeated_query,
            ambiguous_attribution=instance.ambiguous_attribution,
            requires_terminal_action=(
                entry.requires_terminal_action if entry is not None else None
            ),
        )
        # Section 4.3 one-way correction: observing a successful terminal call is conclusive
        # evidence that "this intent really does change state", and it only upgrades, never
        # downgrades. Conversely, "several instances have no terminal call" does not imply
        # "no terminal call is required" -- that is exactly the hole this design closes.
        #
        # Instances with doubtful attribution do not count: the calls under their name may
        # come from another intent in the same turn, which is why classify_outcome above
        # refuses to judge them success (this instance's outcome is unknown). Evidence that
        # does not even qualify for a success verdict should not permanently rewrite the
        # taxonomy. Measured: discount.query_info (described as "query the 618 promotion
        # policy") and logistics.track ("query the current logistics position of the parcel
        # in the user's order") were each tightened to true by **one** ambiguous_attribution
        # instance, after which every instance of those two pure-query intents was judged
        # failure.
        #
        # And one is not enough; it takes MIN_TERMINAL_SUPPORT of them: the typical shape of
        # a misattribution is "one out of a large N", so flipping on a single instance would
        # make the threshold a formality.
        #
        # Measured: of discount.query's ("query current promotion information") 15 instances
        # only 1 carried a clean terminal call, and that user's actual words were "are there
        # any discounts or promotions?" yet it carried a manage_ecard/refund; of
        # logistics.query's ("query logistics progress") 12 instances only 1 did, carrying
        # manage_order/modify. Both pure-query intents therefore became
        # requires_terminal_action=true.
        if (
            evolve
            and entry is not None
            and entry.requires_terminal_action is not True
            and not instance.ambiguous_attribution
            and _has_clean_terminal_call(instance)
        ):
            # The historical support count (this instance is not yet persisted, hence the
            # +1). This likewise counts only unambiguously attributed instances, keeping the
            # same standard as the condition above.
            support = 1 + sum(
                1
                for ref in instance_store.refs_for_intent(canonical, resolve=taxonomy.resolve)
                if _has_clean_terminal_call(instance_store.load(ref))
            )
            if support >= MIN_TERMINAL_SUPPORT:
                entry.requires_terminal_action = True
                evolution_log.append({
                    "episode": episode_id,
                    "type": "terminality",
                    "outlet": "tighten",
                    "intent": canonical,
                    "reason": f"observed a successful terminal call, supported by {support} instances",
                })
        ref = instance_store.save(episode_id, index, instance)
        refs.append((ref, instance))
        if entry is None:
            pending_signals[ref] = (negative_signal, repeated_query)

    # The frozen evaluation stage stops here: steps one/two are pure measurement
    # (reconstruct instances, judge outcome), while steps three to six are the "growth" --
    # bookkeeping, adjudication, distillation and the merge scan all modify the
    # taxonomy/ledger/experiences. evolve=False means exactly "does not grow", so we return
    # here directly rather than letting the later steps run and relying on the trailing
    # `if evolve: save()` as a backstop: by then step five's distill_and_write would already
    # have written SKILL.md into the library (ExperienceStore does not go through
    # taxonomy.save), and the frozen library would be scribbled over by concurrent
    # evaluation arms.
    if not evolve:
        return {
            "instances": len(instances),
            "refs": [ref for ref, _ in refs],
            "admitted": [],
            "distilled": [],
            "merged": [],
        }

    # Step three: candidate bookkeeping
    matcher = _match_desc(llm)
    desc_by_id = {}
    for turn in turns:
        for item in turn.candidates:
            desc_by_id[str(item.get("proposed_id", ""))] = str(item.get("desc", ""))

    # If an intent already in the taxonomy (the matched branch) gained a successful instance
    # this round, its set of successful instances changed and it needs re-distilling; adding
    # only failed instances does not trigger it, avoiding pointless reruns.
    touched: set[str] = set()

    for ref, instance in refs:
        canonical = taxonomy.resolve(instance.intent)
        if canonical is None:
            ledger.add_intent_candidate(
                desc=desc_by_id.get(instance.intent) or instance.text or instance.intent,
                proposed_id=instance.intent,
                instance_ref=ref,
                matcher=matcher,
            )
            continue
        if instance.outcome == "success":
            touched.add(canonical)
        for key, value in taxonomy.unknown_slots(canonical, instance.slots):
            ledger.add_slot_candidate(canonical, key, value, ref)

    # Step four: admission adjudication
    outcome_of = {ref: instance.outcome for ref, instance in refs}

    def lookup_outcome(ref: str) -> str:
        if ref in outcome_of:
            return outcome_of[ref]
        return instance_store.load(ref).outcome

    ready_intents, ready_slots = ledger.ready(lookup_outcome)
    admitted: list[str] = []

    for candidate in ready_intents:
        decision = adjudicate_intent(candidate.desc, candidate.aliases, taxonomy, llm)
        target = apply_intent_decision(decision, taxonomy)
        if decision.deferred:
            # Double fallback: neither the neighbours nor the conclusion were ever really
            # determined. We change neither instance attribution nor distillation, and leave
            # the candidate in the ledger as-is for the next episode -- casually hanging it on
            # some neighbour would let an unfamiliar trajectory pollute that intent's
            # experience document and inject it into all later experiments.
            evolution_log.append(
                {
                    "episode": episode_id,
                    "type": "intent",
                    "outlet": "defer",
                    "desc": candidate.desc,
                    "aliases": candidate.aliases,
                    "target": None,
                    "reason": decision.reason,
                    "evidence": candidate.instances,
                }
            )
            continue
        evolution_log.append(
            {
                "episode": episode_id,
                "type": "intent",
                "outlet": decision.outlet,
                "desc": candidate.desc,
                "aliases": candidate.aliases,
                "target": target,
                "reason": decision.reason,
                "evidence": candidate.instances,
            }
        )
        # Instance attribution: all three outlets attribute the instances to the target intent
        target_entry = taxonomy.get(target)
        for ref in candidate.instances:
            instance = instance_store.load(ref)
            instance.intent = target
            if decision.outlet == "slot" and decision.slot_key:
                # When downgraded to a slot value, the instance must be re-hung *together
                # with* that slot value: if only the intent were changed, the instance would
                # lack this key/value, and stats.slot_distribution (which requires key and
                # value to both be on the instance) would always report 0 for that value, with
                # no evidence for re-distillation either.
                instance.slots[decision.slot_key] = decision.slot_value
            if target_entry is not None and ref in pending_signals:
                # When this instance's outcome was judged, target had not yet been admitted,
                # so requires_terminal_action could only be passed as None and it fell into
                # the lenient query-class branch -- even if target actually requires a
                # terminal action. Target now has an authoritative answer (whether freshly
                # written by the new outlet, or an existing intent pointed to by the
                # merge/slot outlet), so it must be re-judged: otherwise a trajectory that
                # never actually placed an order / cancelled / refunded would be treated as
                # success evidence and written into SKILL.md by step five.
                negative_signal, repeated_query = pending_signals[ref]
                instance.outcome, instance.outcome_reason = classify_outcome(
                    instance.tools,
                    negative_signal=negative_signal,
                    repeated_query=repeated_query,
                    ambiguous_attribution=instance.ambiguous_attribution,
                    requires_terminal_action=target_entry.requires_terminal_action,
                )
            episode, name = ref.split("/")[1], ref.split("/")[2]
            instance_store.save(episode, int(name.replace(".json", "")), instance)
            # After admission, the candidate's own slots must also go through the unknown-
            # slot path to become slot candidates on this intent that "now exists" -- the
            # candidate branch was continued past before admission, and without catching up
            # here they would never enter the schema.
            for key, value in taxonomy.unknown_slots(target, instance.slots):
                ledger.add_slot_candidate(target, key, value, ref)
        if decision.outlet == "new":
            admitted.append(target)
        touched.add(target)
        ledger.remove_intent(candidate)

    for candidate in ready_slots:
        decision = adjudicate_slot(
            candidate.intent, candidate.key, candidate.value, taxonomy, llm
        )
        changed = apply_slot_decision(
            candidate.intent, candidate.key, candidate.value, decision, taxonomy
        )
        evolution_log.append(
            {
                "episode": episode_id,
                "type": "slot",
                "outlet": decision.outlet,
                "intent": candidate.intent,
                "key": candidate.key,
                "value": candidate.value,
                "changed": changed,
                "reason": decision.reason,
                "evidence": candidate.instances,
            }
        )
        ledger.remove_slot(candidate)

    # Step five: contrastive distillation
    distilled: list[str] = []

    def distill_ids(intent_ids: set[str], *, force: bool = False) -> None:
        # refs always carry taxonomy.resolve: the historical instances of merged-away intents
        # must count into the surviving target's evidence set, or a merge would amount to
        # discarding everything learned on that side.
        #
        # force distinguishes "skip" from "rerun" semantics: step five still dedupes by
        # distilled (the same id is not distilled twice in one call); but the targets of step
        # six's merge scan must be unconditionally re-distilled once, even if they were
        # already distilled in this episode's step five -- merge targets are by construction
        # frequently reached intents, so "already distilled" colliding with "just merged" in
        # the same episode is the norm rather than a rare case, and without re-distilling the
        # merge scan would be wasted, with the merged-away intents' evidence never reaching
        # the surviving target's experience document.
        for intent_id in sorted(intent_ids):
            if intent_id in distilled and not force:
                continue
            intent_refs = instance_store.refs_for_intent(
                intent_id, resolve=taxonomy.resolve
            )
            if distill_and_write(
                intent_id, intent_refs, instance_store, experience_store, llm
            ):
                if intent_id not in distilled:
                    distilled.append(intent_id)

    distill_ids(touched)

    # Step six: periodic merge scan
    merged: list[Any] = []
    if episode_counter % MERGE_SCAN_EVERY_N_EPISODES == 0:
        samples = {
            intent.id: [
                instance_store.load(ref).text
                for ref in instance_store.refs_for_intent(
                    intent.id, resolve=taxonomy.resolve
                )[:5]
            ]
            for intent in taxonomy.active()
        }
        merge_refusals: list[dict[str, str]] = []
        merged = merge_scan(taxonomy, samples, llm, refusals=merge_refusals)
        for source, target, accuracy, reason in merged:
            evolution_log.append(
                {
                    "episode": episode_id,
                    "type": "merge_scan",
                    "outlet": "merge",
                    "source": source,
                    "target": target,
                    "accuracy": accuracy,
                    "reason": reason,
                }
            )
        # Pairs blocked by hard constraints must also leave a trace: the merge scan is the
        # taxonomy's only destructive write operation, and "considered but refused" is a
        # different thing from "the similar-pair detection never found it", handled differently.
        for refusal in merge_refusals:
            evolution_log.append(
                {
                    "episode": episode_id,
                    "type": "merge_scan",
                    "outlet": "refuse",
                    "source": refusal["source"],
                    "target": refusal["target"],
                    "accuracy": None,
                    "reason": refusal["reason"],
                }
            )
        # A merge transfers the source intent's instances to the target's name, so the
        # target's experience document must be re-distilled immediately, or the merged-in
        # evidence would never reach SKILL.md and could not be retrieved at runtime.
        # force=True: the target has very likely already been distilled in this episode's
        # step five.
        distill_ids({target for _, target, _, _ in merged}, force=True)

    if evolve:
        taxonomy.save()
        ledger.save()

    return {
        "instances": len(instances),
        "refs": [ref for ref, _ in refs],
        "admitted": admitted,
        "distilled": distilled,
        "merged": merged,
    }
