#!/usr/bin/env bash
# ============================================================================
# ECom-Bench-XCAT × IEL (this paper's method)
#
# One command runs this round of the experiment end to end. The whole pipeline
# lives in this script, so there is no need to drive its stages by hand:
#
#   1. grow      Cold-start from an empty directory, grow a memory library on the
#                other two folds, and freeze it into a snapshot
#   2. evaluate  Evaluate this method on the test fold against the frozen
#                snapshot, 3 trials per task
#   3. report    Per-fold and cross-fold pass^k (k=1,2,3), per-dimension failure
#                counts, and token cost
#
# The protocol is k-fold cross-validation: round i grows the memory library on the
# other k-1 folds (IEL only) and, once that library is frozen, evaluates only on
# fold i. Every task is therefore evaluated exactly once, and the library that
# evaluates it has never seen it. Evaluation always passes --evolve false: evolving
# on the test fold is data leakage, and run.py rejects it outright.
#
# Usage:
#   bash scripts/run_xcat_iel.sh
#
# Tunables (environment variables, all with defaults)
#   RUN_PYTHON         python interpreter          default python
#   RUN_FOLD_SPEC      fold specification          default folds/xcat_3fold_seed10.json
#   RUN_NUM_TRIALS     trials per task             default 3 (pass^3 needs 3)
#   RUN_CONCURRENCY    evaluation concurrency      default 10
#   RUN_RESULT_ROOT    results root                default results/xcat/iel
#   RUN_COLD_DIR       cold-start source (empty)   default intents-xcat-cold
#   RUN_SNAPSHOT_ROOT  per-round snapshot root     default intents-xcat-iel-cv
#   RUN_SEED           random seed                 default 10
#
# Scale: 3 folds × (40 episodes of serial growth + 20 tasks × 3 trials of evaluation): 120 episodes grown and 180 evaluations in total.
#   Growth is serial by design (the taxonomy is shared mutable state) and is the
#   main cost of the whole run; evaluation can run concurrently.
#
# ============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

ENV_NAME="xcat"
METHOD="iel"
AGENT_IMPL="intent"
INJECT="true"
GROW=1

PYTHON="${RUN_PYTHON:-python}"
FOLD_SPEC="${RUN_FOLD_SPEC:-folds/${ENV_NAME}_3fold_seed10.json}"
NUM_TRIALS="${RUN_NUM_TRIALS:-3}"
CONCURRENCY="${RUN_CONCURRENCY:-10}"
RESULT_ROOT="${RUN_RESULT_ROOT:-results/${ENV_NAME}/${METHOD}}"
COLD_DIR="${RUN_COLD_DIR:-intents-${ENV_NAME}-cold}"
SNAPSHOT_ROOT="${RUN_SNAPSHOT_ROOT:-intents-${ENV_NAME}-${METHOD}-cv}"
SEED="${RUN_SEED:-10}"

# --- Preflight checks -------------------------------------------------------
# Stop immediately when a dependency or a credential is missing: otherwise the
# failure only surfaces when the first episode makes an LLM call, by which point
# minutes of waiting have been wasted and the log holds nothing but one cryptic
# error line.
"$PYTHON" - <<'PY' || { echo "❌ missing dependencies; run pip install -r requirements.txt first" >&2; exit 1; }
import langgraph, langchain_openai, langchain_mcp_adapters, yaml, dotenv  # noqa: F401
PY

[ -f .env ] || { echo "❌ .env is missing (AGENT_LLM_* / USER_LLM_*, see Setup in the README)" >&2; exit 1; }
[ -f "$FOLD_SPEC" ] || { echo "❌ fold specification not found: $FOLD_SPEC" >&2; exit 1; }
if [ "$GROW" = "1" ]; then
  # The cold-start source is merely a starting point that must be empty, so create
  # it when it is absent; only complain when it already exists and is not empty --
  # in that case this round would no longer measure learning from scratch.
  mkdir -p "$COLD_DIR"
  [ -z "$(ls -A "$COLD_DIR" 2>/dev/null || true)" ] || {
    echo "❌ cold-start source $COLD_DIR is not an empty directory. The memory library has" >&2
    echo "   to grow out of a cold start, otherwise this round does not measure learning" >&2
    echo "   from scratch; point it at an empty directory and run again." >&2
    exit 1
  }
fi

# Keep logs next to the results, so post-hoc attribution never needs a second search.
mkdir -p "$RESULT_ROOT/logs"
MAIN_LOG="$RESULT_ROOT/logs/run-$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$MAIN_LOG") 2>&1

echo "▶ ECom-Bench-XCAT (60 tasks, apparel + food) × IEL (this paper's method)"
echo "  fold specification: $FOLD_SPEC"
echo "  results root: $RESULT_ROOT"
echo "  trials per task: $NUM_TRIALS    concurrency: $CONCURRENCY    seed: $SEED"
if [ "$GROW" = "1" ]; then
  echo "  memory library: cold start $COLD_DIR → per-round snapshot $SNAPSHOT_ROOT/<spec>/round<N>"
fi
echo "  full log: $MAIN_LOG"
echo

# --- Rounds -----------------------------------------------------------------
eval "$("$PYTHON" -m folds round --spec "$FOLD_SPEC")"   # → CV_ROUNDS="1 2 3"

for round in $CV_ROUNDS; do
  # Fetch these once per round, and clear the previous round's leftovers first:
  # otherwise a lookup that yields nothing would silently keep the old values.
  unset CV_GROW_FOLDS CV_TEST_FOLDS CV_LABEL CV_GROW_LABEL CV_SPEC_NAME
  eval "$("$PYTHON" -m folds round --spec "$FOLD_SPEC" --round "$round")"

  echo "────────────────────────────────────────────────────────────────────"
  if [ "$GROW" = "1" ]; then
    echo "Round ${round}: grow ${CV_GROW_FOLDS} → test ${CV_TEST_FOLDS}"
  else
    echo "Round ${round}: test ${CV_TEST_FOLDS} (this method has no growth stage)"
  fi
  echo "────────────────────────────────────────────────────────────────────"

  if [ "$GROW" = "1" ]; then
    snapshot="$SNAPSHOT_ROOT/${CV_SPEC_NAME}/round${round}"
    # Refuse to overwrite a snapshot that already exists: it is the sole basis for
    # this round's evaluation, and once it has been overwritten the numbers can no
    # longer be attributed to any particular library. (Use `if`, not a standalone
    # `[ ... ] && {...}`: the latter returns non-zero when its test fails, and
    # `set -e` would kill the script on the spot.)
    if [ -e "$snapshot" ]; then
      echo "❌ snapshot $snapshot already exists. It may be the library another batch of results rests on -- confirm it can be discarded before deleting it." >&2
      exit 1
    fi
    echo "▶ grow: $CV_GROW_FOLDS"
    # --num-trials 1: growth runs exactly once. Evolving further between trials
    # would leave the pass^k estimator undefined and amount to training on the test
    # set. Growth is a single serial pass; it is evaluation that repeats over trials.
    "$PYTHON" run.py --env "$ENV_NAME" \
      --fold-spec "$FOLD_SPEC" --grow-folds $CV_GROW_FOLDS \
      --inject true --evolve true \
      --intent-dir "$COLD_DIR" --snapshot-dir "$snapshot" \
      --num-trials 1 --max-concurrency 1 \
      --seed "$SEED" --shuffle 1 \
      --log-dir "$RESULT_ROOT/grow" --verbose false

    # Taxonomy audit: abort if it fails. Evaluating against a broken taxonomy skews
    # the mechanistic metrics of every arm in the same direction, so the gap between
    # the arms still looks plausible and the error never surfaces by itself.
    echo "▶ taxonomy audit: $snapshot"
    "$PYTHON" - "$snapshot" "$PYTHON" - "$snapshot" <<'PY'
import sys
from pathlib import Path

import yaml

sys.path.insert(0, ".")
from intent.config import intent_paths
from intent.taxonomy import Intent, Taxonomy

snapshot = Path(sys.argv[1])
tax_path = intent_paths(snapshot).taxonomy
if not tax_path.exists():
    print(f"\u274c audit failed: {tax_path} does not exist -- "
          f"the growth stage produced no taxonomy.")
    raise SystemExit(1)

entries = yaml.safe_load(tax_path.read_text(encoding="utf-8")) or []
all_intents = [Intent.from_dict(e) for e in entries]
active = {i.id: i for i in all_intents if i.is_active}
merged = [i for i in all_intents if i.merged_into]
problems: list[str] = []
advisories: list[str] = []

if not active:
    problems.append("the taxonomy contains no active intent")

tax = Taxonomy(tax_path)
tax.load()

# An alias must resolve back to the intent that hosts it, and that has to be judged
# with the runtime resolve(), not by testing whether the alias is itself active: the
# id of a merged-away intent legitimately stays behind as an alias on the target
# intent, which is the normal shape of a merge, and resolve() walks the merge chain
# through to the target.
for intent in tax.active():
    for alias in intent.aliases:
        if alias == intent.id:
            continue
        resolved = tax.resolve(alias)
        if resolved != intent.id:
            problems.append(
                f"alias {alias!r} resolves to {resolved!r}, not to its host "
                f"{intent.id!r} (collision or dangling)"
            )

# A merge chain must land on an active intent, and both ends must agree on whether
# a terminal action is required: resolve() hangs the source intent's instances under
# the target's name, so when terminality disagrees the labels of that whole batch of
# instances flip.
for intent in merged:
    resolved = tax.resolve(intent.merged_into)
    target = tax.get(resolved) if resolved else None
    if target is None or not target.is_active:
        problems.append(
            f"the merge target {intent.merged_into!r} of {intent.id!r} does not "
            f"resolve to an active intent"
        )
        continue
    if intent.requires_terminal_action != target.requires_terminal_action:
        problems.append(
            f"{intent.id!r}(rta={intent.requires_terminal_action}) merges into "
            f"{resolved!r}(rta={target.requires_terminal_action}): terminality mismatch"
        )

if not any(i.requires_terminal_action is True for i in tax.active()):
    advisories.append(
        "no intent has requires_terminal_action=true: this round's terminal dimension has no anchor"
    )

print(f"  active={len(active)}  merged={len(merged)}  "
      f"aliases={sum(len(i.aliases) for i in tax.active())}")
for note in advisories:
    print(f"  \u26a0\ufe0f  {note}")
if problems:
    print(f"\u274c audit failed ({len(problems)} problem(s)):")
    for item in problems:
        print(f"   - {item}")
    raise SystemExit(1)
print("  \u2705 audit passed")
PY

    # Leak guard: the snapshot must contain no episode belonging to a test-fold task.
    # Instance directory names carry the episode_id, which contains the task id, so
    # this can be verified before any evaluation cost is spent, rather than relying
    # on somebody remembering.
    echo "▶ leak check (test fold ${CV_TEST_FOLDS})"
    "$PYTHON" -m folds check-leak --spec "$FOLD_SPEC" --test $CV_TEST_FOLDS --lib "$snapshot"
    library_dir="$snapshot"
  else
    # The baseline needs no memory library, but --intent-dir must still point at an
    # existing directory, so the cold-start source will do.
    library_dir="$COLD_DIR"
  fi

  echo "▶ evaluate: ${CV_TEST_FOLDS} ($NUM_TRIALS trials per task)"
  # Pass --grow-folds alongside --test-folds: the former is a provenance label (which
  # library this evaluation is paired with) and feeds the result directory name and
  # meta.json. Both methods use the same pair of labels, which is what makes their
  # results comparable.
  "$PYTHON" run.py --env "$ENV_NAME" \
    --fold-spec "$FOLD_SPEC" --grow-folds $CV_GROW_FOLDS --test-folds $CV_TEST_FOLDS \
    --inject "$INJECT" --evolve false --agent-impl "$AGENT_IMPL" \
    --intent-dir "$library_dir" \
    --num-trials "$NUM_TRIALS" --max-concurrency "$CONCURRENCY" \
    --seed "$SEED" --shuffle 1 \
    --log-dir "$RESULT_ROOT/eval" --verbose false
  echo "✅ round $round complete"
  echo
done

# --- Report -----------------------------------------------------------------
"$PYTHON" - "$RESULT_ROOT" "$NUM_TRIALS" <<'PY'
import glob
import json
import math
import os
import sys
from collections import defaultdict

ROOT, TRIALS = sys.argv[1], int(sys.argv[2])

runs = []
for meta_path in sorted(glob.glob(os.path.join(ROOT, "**", "meta.json"), recursive=True)):
    results_path = os.path.join(os.path.dirname(meta_path), "results.json")
    if not os.path.exists(results_path):
        continue
    with open(meta_path, encoding="utf-8") as fh:
        meta = json.load(fh)
    with open(results_path, encoding="utf-8") as fh:
        records = json.load(fh)
    # Only the evaluation stage enters the report: a growth-stage reward is measured
    # while the system is still learning and is not the same thing as a frozen
    # evaluation.
    if meta.get("config", {}).get("evolve"):
        continue
    if not meta.get("fold_label"):
        continue
    runs.append((meta, records))

if not runs:
    print(f"\n⚠️  no frozen-evaluation results (meta.json + results.json) found under {ROOT}; "
          f"skipping the report.")
    raise SystemExit(0)

# A round may have been run more than once (a backfill, or a rerun after a change),
# so keep only the latest timestamp, to avoid counting the same batch of tasks twice.
latest: dict[str, tuple[str, dict, list]] = {}
for meta, records in runs:
    label = meta["fold_label"]
    stamp = str(meta.get("started_at") or "")
    if label not in latest or stamp >= latest[label][0]:
        latest[label] = (stamp, meta, records)

def pass_k(counts: dict[int, int], k: int, trials: int) -> float:
    """Paper definition: when task i succeeds counts[i] times out of trials, that task
    contributes C(c_i, k) / C(trials, k); average over tasks."""
    if not counts or trials < k:
        return float("nan")
    denom = math.comb(trials, k)
    # Use C(c_i, k) directly. math.comb already returns 0 when c_i < k, and it must
    # **not** be clipped to k beforehand: clipping would turn pass^1 into "succeeded
    # at least once" and pass^2 into "succeeded at least twice", both below the
    # paper's definition, and could even yield the impossible pass^3 > pass^1.
    return sum(math.comb(c, k) / denom for c in counts.values()) / len(counts)

per_fold: dict[str, dict[int, float]] = {}
dim_fail: dict[str, int] = defaultdict(int)
executor_tokens: list[float] = []
intent_tokens: list[float] = []
short = 0

for label in sorted(latest):
    _, _, records = latest[label]
    counts: dict[int, int] = defaultdict(int)
    seen: dict[int, int] = defaultdict(int)
    for r in records:
        tid = r.get("task_id")
        counts[tid] += 1 if r.get("reward") else 0
        seen[tid] += 1
    short += sum(1 for n in seen.values() if n < TRIALS)
    per_fold[label] = {k: pass_k(counts, k, TRIALS) for k in (1, 2, 3)}
    for r in records:
        if r.get("reward"):
            continue
        detail = r.get("detail_reward") or {}
        for dim in ("action", "search", "output"):
            if not detail.get(dim):
                dim_fail[dim] += 1
    n_tasks = max(len(counts), 1)
    executor_tokens.append(sum(r.get("total_tokens") or 0 for r in records) / n_tasks)
    intent_tokens.append(sum(r.get("intent_total_tokens") or 0 for r in records) / n_tasks)

def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")

def std(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5

bar = "=" * 78
print()
print(bar)
print(f"pass^k  -- share of tasks that succeed on all k executions "
      f"({TRIALS} trials per task, {len(per_fold)} folds)")
print(bar)
print(f"{'fold':<50}{'pass^1':>9}{'pass^2':>9}{'pass^3':>9}")
for label in sorted(per_fold):
    v = per_fold[label]
    print(f"{label:<50}{v[1] * 100:>8.1f}%{v[2] * 100:>8.1f}%{v[3] * 100:>8.1f}%")
print("-" * 78)
for k in (1, 2, 3):
    vals = [per_fold[label][k] for label in per_fold]
    print(f"{'cross-fold mean ± std: pass^' + str(k):<50}{mean(vals) * 100:>8.1f}% ±{std(vals) * 100:>5.1f}")
print()
print("The test sets of the folds are pairwise disjoint, so the cross-fold average above "
      "is pass^k over the full task set.")
print("Failures per dimension (counting only tasks judged an overall failure): "
      + "  ".join(f"{d}={dim_fail[d]}" for d in ("action", "search", "output")))
print(f"mean tokens / task: executor {mean(executor_tokens):.0f}, intent system {mean(intent_tokens):.0f}")
if short:
    print(f"⚠️  {short} task records have fewer than {TRIALS} trials "
          f"(the task errored or was truncated); pass^k is still computed over "
          f"{TRIALS} trials, which makes it conservative.")
print()
print("This script evaluates a single method. The paper's paired comparison (iel - react) "
      "needs the other method's results on the same set of tasks;")
print("the two scripts' result roots are siblings, so the difference can be taken directly.")
PY

echo
echo "✅ all done. Results: $RESULT_ROOT"
