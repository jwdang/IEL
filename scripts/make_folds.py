"""Generate a task fold-spec file, to be referenced by run.py's --fold-spec.

Usage:
    python scripts/make_folds.py --env story --k 3 --seed 10 \
        --out folds/story_3fold_seed10.json

Stratification criterion (--stratify shape, the default)
--------------------------------------------------------
Stratify by each task's **checkpoint shape**: (total of actions + searches + outputs,
number of actions). The reason is that these three kinds of checkpoint are exactly the
denominator of the reward, so they largely determine what a task "is worth" and how hard
it is to get right. At a scale of n=53, plain random assignment very easily produces one
fold consisting entirely of light tasks with 1 action and another stuffed with heavy
tasks of 4~5 actions -- that between-fold difference would then be read as the effect of
the method. After stratification each fold has a similar total number of checkpoints
(see fold_stats in the output), so that a between-fold comparison is actually comparing
methods.

Within a stratum the order is shuffled with --seed, then dealt in descending order of
difficulty in a **snake** pattern: after each full round the direction reverses
(0,1,2 / 2,1,0 / 0,1,2 ...). Dealing straight round-robin would make fold 1 always get
the heaviest task of every round, and across 53 tasks the between-fold checkpoint totals
drift as far apart as 78/74/70; snake dealing cancels this systematic skew, giving
73/74/75 for the same task set. Fold numbers are then reassigned in descending order of
size, so 53 tasks split into 3 folds gives 18/18/17 (when it does not divide evenly, the
shorter fold always ends up last).

--stratify none degrades to plain random assignment, kept for cases that need a control.

A fold spec is never overwritten silently: it errors if --out already exists, unless
--overwrite is given explicitly. A spec that has been used for experiments is part of
that batch of results; once overwritten, those results can no longer be reproduced.
"""

from __future__ import annotations

import argparse
import importlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def _load_tasks(env: str) -> List[Any]:
    module = importlib.import_module(f"envs.{env}.tasks")
    return list(module.ALL_TASKS)


def _shape(task: Any) -> Dict[str, int]:
    """A task's checkpoint shape. metadata is a utils.Validation (None for some tasks)."""
    meta = getattr(task, "metadata", None)
    actions = len(getattr(meta, "actions", []) or [])
    searches = len(getattr(meta, "searches", []) or [])
    outputs = len(getattr(meta, "outputs", []) or [])
    return {
        "actions": actions,
        "searches": searches,
        "outputs": outputs,
        "checkpoints": actions + searches + outputs,
    }


def _assign(shapes: List[Dict[str, int]], k: int, seed: int, stratify: str) -> List[List[int]]:
    order: List[int]
    if stratify == "none":
        order = list(range(len(shapes)))
        random.Random(seed).shuffle(order)
    else:
        strata: Dict[tuple, List[int]] = defaultdict(list)
        for task_id, shape in enumerate(shapes):
            strata[(shape["checkpoints"], shape["actions"])].append(task_id)
        rng = random.Random(seed)
        order = []
        # Descending difficulty: heavy tasks are dealt first, which spreads them evenly
        # across folds; light tasks fill in the tail difference between folds at the end.
        # The reverse (dealing light ones first) would crowd the last few heavy tasks all
        # into the same fold.
        for key in sorted(strata, reverse=True):
            bucket = strata[key]
            rng.shuffle(bucket)
            order.extend(bucket)

    folds: List[List[int]] = [[] for _ in range(k)]
    for position, task_id in enumerate(order):
        lap, seat = divmod(position, k)
        # Snake: odd rounds deal in reverse, cancelling the systematic skew where
        # "fold 1 always gets the heaviest task of each round".
        folds[(k - 1 - seat) if lap % 2 else seat].append(task_id)
    # Reassign fold numbers in descending order of size: when the task count is not
    # divisible by k, the fold with one fewer task is pinned last
    # (53/3 -> fold1=18, fold2=18, fold3=17). Snake dealing alone does not guarantee
    # this; which number the short fold lands on depends on the direction of the last
    # half-round, and only after this reordering does a number have a stable meaning.
    # Ties in size are broken by smallest task id, so the same seed always produces
    # exactly the same numbering.
    ordered = sorted(folds, key=lambda ids: (-len(ids), min(ids)))
    return [sorted(fold) for fold in ordered]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--env", default="story", help="environment name, corresponding to envs/<env>/tasks.py")
    parser.add_argument("--k", type=int, default=3, help="number of folds")
    parser.add_argument("--seed", type=int, default=10, help="randomness source for the split; same seed, same split")
    parser.add_argument("--stratify", choices=["shape", "none"], default="shape",
                        help="shape=stratify by checkpoint shape (default); none=plain random")
    parser.add_argument("--out", default="", help="output path, default folds/<env>_<k>fold_seed<seed>.json")
    parser.add_argument("--name", default="", help="spec name (goes into the result directory and log names), default <k>fold-s<seed>")
    parser.add_argument("--overwrite", action="store_true", help="allow overwriting an existing spec file")
    args = parser.parse_args()

    if args.k < 2:
        print("❌ --k must be at least 2", file=sys.stderr)
        return 2

    tasks = _load_tasks(args.env)
    if args.k > len(tasks):
        print(f"❌ --k={args.k} exceeds the number of tasks {len(tasks)}", file=sys.stderr)
        return 2

    out = Path(args.out or f"folds/{args.env}_{args.k}fold_seed{args.seed}.json")
    if out.exists() and not args.overwrite:
        print(f"❌ {out} already exists. It may be exactly the spec a batch of results was based on; "
              f"overwriting it would make that batch irreproducible.\n"
              f"   Use a different --out, or add --overwrite once you are sure you want to discard it.", file=sys.stderr)
        return 1

    # The spec name must include the dataset name: fold1/fold2/fold3 refer to completely
    # different task sets in story and in xcat, so a bare `3fold-s10` would give the two
    # specs the same name, and the spec name goes into the result directory name -- the
    # results of the two datasets would land in the same directory and could no longer be
    # told apart afterwards (see folds.fold_label).
    name = args.name or f"{args.env}-{args.k}fold-s{args.seed}"
    shapes = [_shape(task) for task in tasks]
    assignment = _assign(shapes, args.k, args.seed, args.stratify)
    fold_names = [f"fold{i + 1}" for i in range(args.k)]

    fold_stats = {}
    for fold_name, ids in zip(fold_names, assignment):
        fold_stats[fold_name] = {
            "size": len(ids),
            "actions": sum(shapes[i]["actions"] for i in ids),
            "searches": sum(shapes[i]["searches"] for i in ids),
            "outputs": sum(shapes[i]["outputs"] for i in ids),
            "checkpoints": sum(shapes[i]["checkpoints"] for i in ids),
        }

    # Standard k-fold protocol: round i grows on the other k-1 folds and tests only on
    # fold i. It is written into the file so that the spec carries its own protocol
    # description -- whoever reads the spec need not go elsewhere to confirm "which fold
    # round 1 actually tests on".
    rounds = [
        {
            "round": i + 1,
            "grow": [n for n in fold_names if n != fold_names[i]],
            "test": [fold_names[i]],
            "grow_size": sum(len(ids) for j, ids in enumerate(assignment) if j != i),
            "test_size": len(assignment[i]),
        }
        for i in range(args.k)
    ]

    spec = {
        "name": name,
        "env": args.env,
        "num_tasks": len(tasks),
        "k": args.k,
        "seed": args.seed,
        "stratify": args.stratify,
        "description": (
            f"{args.k}-fold cross-validation split for {args.env}. "
            f"stratify={args.stratify} (shape = stratified by the actions+searches+outputs "
            f"checkpoint shape), seed={args.seed}. Round i: grow the experience library on "
            f"the other {args.k - 1} folds and evaluate only on fold i."
        ),
        "generated_by": (
            f"python scripts/make_folds.py --env {args.env} --k {args.k} "
            f"--seed {args.seed} --stratify {args.stratify} --out {out}"
        ),
        "folds": {n: ids for n, ids in zip(fold_names, assignment)},
        "fold_stats": fold_stats,
        "rounds": rounds,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"✅ Wrote {out} (name={name}, env={args.env}, {len(tasks)} tasks)")
    for fold_name in fold_names:
        stats = fold_stats[fold_name]
        print(f"  {fold_name}: n={stats['size']:2d}  checkpoints={stats['checkpoints']:3d}"
              f" (action={stats['actions']:2d} search={stats['searches']:2d}"
              f" output={stats['outputs']:2d})")
    print("  Rounds:")
    for r in rounds:
        print(f"    round {r['round']}: grow {'+'.join(r['grow'])} ({r['grow_size']})"
              f" → test {'+'.join(r['test'])} ({r['test_size']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
