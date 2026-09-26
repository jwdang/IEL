"""Command-line query entry point for grouping specs.

    python -m folds list                                   # which specs exist
    python -m folds show --spec story_3fold_seed10         # a spec's folds and rounds
    python -m folds label --spec ... --grow fold2 fold3 --test fold1
    python -m folds tasks --spec ... --test fold1          # space-separated task ids
    python -m folds round --spec ... --round 1             # eval-able KEY=VALUE
    python -m folds check-leak --spec ... --test fold1 --lib intents-e1b-L-...

The round subcommand lets run scripts read the protocol straight from the spec file:
`eval "$(python -m folds round --spec ... --round 1)"`. The definition of the rounds (round i
grows on the other folds and tests only fold i) is therefore written once, in the spec file, and
the shell need not transcribe a copy -- a transcription would sooner or later disagree with a
new spec that changed k.

The label subcommand exists for one reason only: run scripts must write the fold keyword into
log filenames, and the label's spelling must be **word-for-word identical** to the one in the
result directory name. Building it again in the shell would create a second implementation, and
any change to the label format would inevitably miss one of them, after which the logs and the
result directories stop matching.

check-leak guards against the mistake that is easiest to make and hardest to notice in
cross-validation: evaluating one fold with a library grown from all 53 tasks. The test fold's
episodes are already in the library, the scores come out too high, and the result files, logs
and directory names all look perfectly normal. The intent library's instance directory names
carry the episode_id (which includes the task id), so this can be **verified** before a run,
instead of relying on someone remembering to swap libraries.
"""

from __future__ import annotations

import argparse
import sys

from . import (
    FoldSpecError,
    available_specs,
    fold_label,
    library_task_ids,
    load_fold_spec,
    select_folds,
)


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m folds", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="list all specs")

    for name, help_text in (
        ("show", "print a spec's folds, sizes and standard rounds"),
        ("label", "print the fold label used in result directory/log names"),
        ("tasks", "print the task ids selected this time (space-separated)"),
        ("check-leak", "verify that an intent library contains no test-fold episode"),
        ("round", "print one round's growth folds / test folds / label (KEY=VALUE, eval-able)"),
    ):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--spec", required=True, help="spec name or spec file path")
        if name not in ("show", "round"):
            p.add_argument("--grow", nargs="*", default=[], help="growth folds")
            p.add_argument("--test", nargs="*", default=[], help="test folds")
        if name == "check-leak":
            p.add_argument("--lib", required=True, help="intent library directory to verify")
        if name == "round":
            p.add_argument("--round", type=int,
                           help="which round (1-based); without it prints CV_ROUNDS=\"1 2 3\"")

    args = parser.parse_args()

    if args.cmd == "list":
        for path in available_specs():
            try:
                spec = load_fold_spec(str(path))
            except FoldSpecError as exc:
                print(f"{path.stem:<28} ❌ {exc}")
                continue
            sizes = ", ".join(f"{n}={len(ids)}" for n, ids in spec.folds.items())
            print(f"{path.stem:<28} name={spec.name} env={spec.env} n={spec.num_tasks}  {sizes}")
        return 0

    if args.cmd == "show":
        spec = load_fold_spec(args.spec)
        print(f"{spec.path}  name={spec.name} env={spec.env} num_tasks={spec.num_tasks}")
        if spec.raw.get("description"):
            print(f"  {spec.raw['description']}")
        for fold_name, ids in spec.folds.items():
            stats = (spec.raw.get("fold_stats") or {}).get(fold_name, {})
            extra = f" checkpoints={stats['checkpoints']}" if "checkpoints" in stats else ""
            print(f"  {fold_name}: n={len(ids)}{extra}  {list(ids)}")
        for rnd in spec.raw.get("rounds") or []:
            grow, test = "+".join(rnd["grow"]), "+".join(rnd["test"])
            print(f"  round {rnd['round']}: --grow-folds {' '.join(rnd['grow'])}"
                  f" --test-folds {' '.join(rnd['test'])}"
                  f"   [{fold_label(spec, rnd['grow'], rnd['test'])}]"
                  f"   grow {grow} / test {test}")
        return 0

    if args.cmd == "round":
        spec = load_fold_spec(args.spec)
        rounds = {int(r["round"]): r for r in spec.raw.get("rounds") or []}
        if args.round is None:
            # Run scripts use this to decide how many rounds to loop over -- the round count is
            # determined by the spec (a 5-fold spec means 1..5), and scripts should not hardcode
            # a 3.
            print(f'CV_ROUNDS="{" ".join(str(i) for i in sorted(rounds))}"')
            return 0
        if args.round not in rounds:
            raise FoldSpecError(
                f"spec {spec.name!r} has no round {args.round}; it has "
                f"{sorted(rounds) or '(rounds field missing)'}"
            )
        rnd = rounds[args.round]
        grow, test = list(rnd["grow"]), list(rnd["test"])
        # Fold names are already restricted to [A-Za-z0-9.-] when loading, containing no spaces
        # or quotes, so wrapping them in double quotes here is safe for the shell to eval.
        print(f'CV_ROUND="{args.round}"')
        print(f'CV_SPEC_NAME="{spec.name}"')
        print(f'CV_GROW_FOLDS="{" ".join(grow)}"')
        print(f'CV_TEST_FOLDS="{" ".join(test)}"')
        print(f'CV_GROW_LABEL="{fold_label(spec, grow, [])}"')
        print(f'CV_LABEL="{fold_label(spec, grow, test)}"')
        return 0

    selection = select_folds(args.spec, args.grow, args.test)
    if selection is None:
        # No fold selected = a full run: the label is an empty string (directory names as
        # before) and the task list is empty too, so there is no "test fold must not appear in
        # the library" concern and check-leak has nothing to check.
        return 0
    if args.cmd == "label":
        print(selection.label)
        return 0
    if args.cmd == "tasks":
        print(" ".join(str(i) for i in selection.task_ids))
        return 0

    # check-leak
    if not selection.test:
        print("⚠️  --test not given, so there is nothing to check for leakage (growth folds appearing in the library is expected)")
        return 0
    grown_from = library_task_ids(args.lib)
    test_ids = set(selection.spec.task_ids(selection.test))
    if grown_from is None:
        # Unverified is not the same as no leakage: say clearly which one it is, so the caller
        # does not read silence as a pass.
        print(f"⚠️  cannot verify {args.lib}: no parseable instances/<episode_id>/ directories. "
              "Please confirm yourself that this library contains no test-fold episode.")
        return 0
    leaked = sorted(test_ids & set(grown_from))
    if leaked:
        print(f"❌ leakage: intent library {args.lib} contains episodes of "
              f"{len(leaked)} tasks from test fold {'+'.join(selection.test)}: {leaked}\n"
              "   This library cannot be used to evaluate this fold -- it has already seen these "
              "tasks. Use the snapshot produced by the **same round's** growth stage instead.", file=sys.stderr)
        return 1
    print(f"✅ {args.lib} grew from the episodes of {len(grown_from)} tasks, "
          f"with no overlap with test fold {'+'.join(selection.test)} ({len(test_ids)} tasks)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FoldSpecError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        raise SystemExit(2)
