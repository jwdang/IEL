"""Reading, validation and naming of task grouping (fold) specs.

Why the grouping spec has to be a **file** rather than hardcoded
---------------------------------------------------------------
The cross-validation grouping is part of the experimental protocol: once results exist, "which
18 tasks was round 1 actually measured on" must be reproducible as-is, and must be archivable
alongside the results and citable by the paper. A grouping written in code quietly changes with
an unrelated refactor (say, someone alters the shuffle implementation), leaving no trace
afterwards of which version was in use. As JSON, the spec is data: there can be a second and a
third (different k, different seed, different stratification), it can be diffed, it can go into
git history, and run.py only has to reference it by name.

Invariants (enforced by load_fold_spec; a violation means refusing to load)
---------------------------------------------------------------------------
1. The folds are pairwise disjoint -- that is the entire point of cross-validation. With
   overlap, the "growth folds" would contain "test fold" tasks, the measured numbers would be
   training-set performance, and that leakage would look exactly like a genuine result in the
   output rather than exposing itself.
2. The union of the folds is exactly range(num_tasks) -- no task is omitted and no task falls
   outside the declared range. When some tasks should be held out, put them in an explicitly
   named fold (say "holdout") and simply never pass it to --grow-folds/--test-folds, rather
   than letting them vanish from the spec: the former is visible in the file, the latter can
   only be found by counting.
3. num_tasks must equal the environment's actual task count (checked at run time by
   assert_matches_env, since this module cannot see the environment). A mismatch means the spec
   was written for a different task set and the ids point at the wrong tasks -- that misalignment
   raises no error and only produces a quietly wrong result.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

# The default directory for spec files, namely this package itself: the specs are this
# package's data and should not be scattered around the repository, nor should callers have to
# remember a path prefix.
SPEC_DIR = Path(__file__).resolve().parent

# The spec name each dataset references by default. Naming convention <env>_<k>fold_seed<seed>:
# the two datasets each have one (folds/story_3fold_seed10.json, folds/xcat_3fold_seed10.json),
# and fold1/fold2/fold3 in a spec name refer to completely different task sets in the two, so
# the dataset name must be part of the spec name, or the two sets of results would land in the
# same directory and could not be told apart afterwards.
#
# Note it is **not** "run by fold by default": without --grow-folds/--test-folds this module
# takes no part at all, and a full run's behaviour and directory name are word-for-word as
# before. It merely saves typing the path of the most commonly used spec.
DEFAULT_FOLDS = 3
DEFAULT_FOLD_SEED = 10


def default_spec_name(env: str, k: int = DEFAULT_FOLDS, seed: int = DEFAULT_FOLD_SEED) -> str:
    """The spec name a dataset references by default (without the .json suffix)."""
    return f"{env}_{k}fold_seed{seed}"


def default_spec_path(env: str) -> str:
    """The spec path a dataset references by default, i.e. what --fold-spec takes when not
    given."""
    return f"folds/{default_spec_name(env)}.json"

# Fold names and spec names both go into directory names and log filenames, so only characters
# needing no escaping in either the filesystem or the shell are allowed. '+' is this module's
# separator when joining several folds and '_' is the segment separator; neither may appear in
# a name, or the label could not be read back by a person (or a glob).
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.-]*$")


class FoldSpecError(ValueError):
    """The spec file itself is invalid, or a fold it does not define was referenced."""


@dataclass(frozen=True)
class FoldSpec:
    """A grouping spec that has already been validated."""

    name: str
    env: str
    num_tasks: int
    # Ordered: the order written in the file is the display order, and `python -m folds show`
    # outputs in it.
    folds: Mapping[str, Tuple[int, ...]]
    path: Path
    raw: Mapping

    @property
    def fold_names(self) -> List[str]:
        return list(self.folds)

    def task_ids(self, fold_names: Sequence[str]) -> List[int]:
        """Take the union of the task ids of several folds (ascending).

        A missing name errors rather than being treated as an empty set: with
        `--test-folds fold4` mistyped by one character, an empty set would quietly run 0 tasks
        or run the full set, both of which are harder to notice than an error.
        """
        ids: List[int] = []
        for name in fold_names:
            if name not in self.folds:
                raise FoldSpecError(
                    f"spec {self.name!r} ({self.path}) has no fold named {name!r}; "
                    f"available: {', '.join(self.fold_names)}"
                )
            ids.extend(self.folds[name])
        return sorted(set(ids))

    def assert_matches_env(self, num_env_tasks: int) -> None:
        """The task count declared by the spec must match the environment's actual task count.

        On a mismatch the ids in the fold no longer point at the tasks the spec author picked:
        if the count grew, the tasks at the end are never selected; if it shrank, out-of-range
        ids raise IndexError outright or (worse) get silently truncated elsewhere. This is a hard
        error meaning "the spec and the environment are not the same set".
        """
        if self.num_tasks != num_env_tasks:
            raise FoldSpecError(
                f"grouping spec {self.name!r} ({self.path}) declares num_tasks={self.num_tasks}, "
                f"but environment {self.env!r} actually has {num_env_tasks} tasks. The task ids in "
                "the spec were assigned for the task set as it was back then, and on a mismatch "
                "they do not select the same tasks. Use the spec corresponding to this dataset "
                "(folds/<dataset>_3fold_seed10.json), or regenerate it: "
                "python scripts/make_folds.py --env <dataset> --k <num-folds> --seed <seed>"
            )


@dataclass(frozen=True)
class FoldSelection:
    """The folds (growth / test) actually selected by one run, and their task set."""

    spec: FoldSpec
    grow: Tuple[str, ...]
    test: Tuple[str, ...]
    # The task ids actually to be executed this time: the test fold if one was given,
    # otherwise the growth folds.
    task_ids: Tuple[int, ...]
    # Which stage is being executed this time. "test" = frozen evaluation, "grow" = growth.
    role: str

    @property
    def label(self) -> str:
        return fold_label(self.spec, self.grow, self.test)


def available_specs() -> List[Path]:
    return sorted(SPEC_DIR.glob("*.json"))


def resolve_spec_path(spec: str) -> Path:
    """Resolve the value of --fold-spec into a file path that really exists.

    It accepts both a path (folds/story_3fold_seed10.json, an absolute path, a spec file
    elsewhere) and a bare name (story_3fold_seed10), the latter looked up in this package's
    directory. The bare name is a convenience spelling for the command line, the path is for
    scripts and for specs archived elsewhere.
    """
    candidate = Path(spec)
    if candidate.is_file():
        return candidate
    if candidate.suffix != ".json":
        named = SPEC_DIR / f"{candidate.name}.json"
        if named.is_file():
            return named
    known = ", ".join(p.stem for p in available_specs()) or "(none)"
    raise FoldSpecError(
        f"cannot find grouping spec {spec!r}. It is neither an existing file nor a spec name "
        f"under {SPEC_DIR}. Existing specs: {known}"
    )


def load_fold_spec(spec: str) -> FoldSpec:
    """Read and validate a grouping spec. The three invariants in the module docstring are
    enforced here."""
    path = resolve_spec_path(spec)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FoldSpecError(f"grouping spec {path} is not valid JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise FoldSpecError(f"the top level of grouping spec {path} must be an object, but is {type(raw).__name__}")

    for key in ("name", "env", "num_tasks", "folds"):
        if key not in raw:
            raise FoldSpecError(f"grouping spec {path} is missing the required field {key!r}")

    name = str(raw["name"])
    if not _NAME_RE.match(name):
        raise FoldSpecError(
            f"grouping spec {path} has name={name!r}, which contains characters that cannot go "
            "into a directory/log name; only alphanumerics and '.' '-' are allowed (and not at "
            "the start)"
        )

    num_tasks = raw["num_tasks"]
    if not isinstance(num_tasks, int) or num_tasks <= 0:
        raise FoldSpecError(f"grouping spec {path} has num_tasks which must be a positive integer, but is {num_tasks!r}")

    raw_folds = raw["folds"]
    if not isinstance(raw_folds, dict) or not raw_folds:
        raise FoldSpecError(f"the folds of grouping spec {path} must be a non-empty object")

    folds: Dict[str, Tuple[int, ...]] = {}
    seen: Dict[int, str] = {}
    for fold_name, ids in raw_folds.items():
        if not _NAME_RE.match(str(fold_name)):
            raise FoldSpecError(
                f"grouping spec {path} has fold name {fold_name!r}, which contains characters "
                "that cannot go into a directory/log name; only alphanumerics and '.' '-' are "
                "allowed (and not at the start)"
            )
        if not isinstance(ids, list) or not ids:
            raise FoldSpecError(f"fold {fold_name!r} of grouping spec {path} must be a non-empty list of task ids")
        normalized: List[int] = []
        for task_id in ids:
            if not isinstance(task_id, int) or isinstance(task_id, bool):
                raise FoldSpecError(
                    f"fold {fold_name!r} of grouping spec {path} contains a non-integer task id {task_id!r}"
                )
            if not 0 <= task_id < num_tasks:
                raise FoldSpecError(
                    f"fold {fold_name!r} of grouping spec {path} contains out-of-range task id {task_id}"
                    f" (legal range 0..{num_tasks - 1})"
                )
            # Invariant 1: pairwise disjoint. Overlap means data leakage, and a leaked result
            # looks entirely normal.
            if task_id in seen:
                raise FoldSpecError(
                    f"task {task_id} of grouping spec {path} appears in both fold {seen[task_id]!r} and "
                    f"{fold_name!r}. Folds must be disjoint: with overlap the growth folds would "
                    "include the test fold's tasks, and what is measured is training-set performance."
                )
            seen[task_id] = str(fold_name)
            normalized.append(task_id)
        folds[str(fold_name)] = tuple(normalized)

    # Invariant 2: the union covers exactly 0..num_tasks-1.
    missing = sorted(set(range(num_tasks)) - set(seen))
    if missing:
        raise FoldSpecError(
            f"grouping spec {path} does not cover all tasks; it is missing {missing}. "
            "If you really want to hold some tasks out, put them in an explicitly named fold "
            "(e.g. \"holdout\") and do not pass it to --grow-folds/--test-folds, rather than "
            "letting them vanish from the spec."
        )

    return FoldSpec(name=name, env=str(raw["env"]), num_tasks=num_tasks,
                    folds=folds, path=path, raw=raw)


# The instance directory name is the episode_id: `<run_id>-t<task_index>-r<trial>`
# (assembled in envs/env.py). The intent library therefore carries its own record of "which
# tasks grew me".
_EPISODE_TASK_RE = re.compile(r"-t(\d+)-r\d+$")


def library_task_ids(intent_dir: str) -> Optional[List[int]]:
    """Which tasks' episodes an intent library grew from.

    A None return means **it cannot be determined** (instances/ does not exist, or the
    directory names are not parseable episode_ids) -- e.g. a hand-assembled library, one
    imported from elsewhere, or one with a future naming scheme. Callers must treat None as
    "unverified", never as "no leakage".
    """
    instances = Path(intent_dir) / "instances"
    if not instances.is_dir():
        return None
    task_ids = set()
    parsed = False
    for episode_dir in instances.iterdir():
        if not episode_dir.is_dir():
            continue
        match = _EPISODE_TASK_RE.search(episode_dir.name)
        if match:
            parsed = True
            task_ids.add(int(match.group(1)))
    return sorted(task_ids) if parsed else None


def fold_label(spec: Optional[FoldSpec], grow: Sequence[str], test: Sequence[str]) -> str:
    """The fold label used in result directory names and log filenames.

    Of the form `story-3fold-s10_grow-fold2+fold3_test-fold1`. With no fold selected it returns
    an empty string, so a full run's directory name is exactly as before (existing results need
    no migration).

    The spec name must be part of the label: the same set of fold names (fold1/fold2/fold3)
    refers to completely different task sets in different specs, so writing only
    `grow-fold2+fold3` would make the two specs' results land in the same directory and be
    indistinguishable afterwards.
    """
    if spec is None or (not grow and not test):
        return ""
    parts = [spec.name]
    if grow:
        parts.append("grow-" + "+".join(grow))
    if test:
        parts.append("test-" + "+".join(test))
    return "_".join(parts)


def select_folds(
    spec: str,
    grow: Sequence[str] = (),
    test: Sequence[str] = (),
) -> Optional[FoldSelection]:
    """Resolve --fold-spec/--grow-folds/--test-folds into one run's task set.

    With neither switch given it returns None -- that is the ordinary "no grouping, run
    everything" run, which this module has nothing to do with.

    When a test fold is given, what executes this time is the **test fold**'s tasks; the growth
    folds are then a provenance label recording "which folds the experience library under test
    grew on", which goes into the directory name and meta.json -- otherwise all one could do
    afterwards is guess from timestamps which round's library a given evaluation used.
    """
    grow = tuple(grow or ())
    test = tuple(test or ())
    if not grow and not test:
        return None

    loaded = load_fold_spec(spec)
    grow_ids = loaded.task_ids(grow)
    test_ids = loaded.task_ids(test)

    overlap = sorted(set(grow_ids) & set(test_ids))
    if overlap:
        raise FoldSpecError(
            f"growth folds {list(grow)} and test folds {list(test)} overlap on tasks {overlap}. "
            "Cross-validation requires them to be disjoint, or what is measured is training-set "
            "performance."
        )

    if test:
        return FoldSelection(spec=loaded, grow=grow, test=test,
                             task_ids=tuple(test_ids), role="test")
    return FoldSelection(spec=loaded, grow=grow, test=test,
                         task_ids=tuple(grow_ids), role="grow")
