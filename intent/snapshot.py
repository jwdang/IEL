"""Intent library snapshots and size statistics.

With evolve=on the taxonomy keeps changing during a run, and a snapshot is the only way to
restore its state at the time afterwards.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from intent.config import IntentPaths, intent_paths


def taxonomy_size(paths: IntentPaths) -> int:
    """The current number of active intents."""
    if not paths.taxonomy.exists():
        return 0
    raw = yaml.safe_load(paths.taxonomy.read_text(encoding="utf-8")) or []
    return sum(1 for item in raw if str(item.get("status", "active")) == "active")


def assert_safe_snapshot_pair(source: Path | str, destination: Path | str) -> None:
    """Validate the safety of the snapshot source/destination, making no filesystem changes.

    If source and destination have any containment relation (including being identical), the
    operation is forbidden outright, and this judgement must be complete before any filesystem
    change:

    - destination inside source: `shutil.copytree` takes a snapshot of source's direct
      children once before it starts copying, but re-`scandir`s only when recursing into a
      subdirectory; if destination hangs under one of source's existing subdirectories,
      `os.makedirs(destination)` turns destination itself into a newly appearing entry of that
      subdirectory at that moment, and the next level's `scandir` treats it as part of the
      source and copies it again, nesting into itself over and over until the path length runs
      out and it errors, leaving junk directories permanently inside source.
    - destination is an ancestor of source (contains it the other way): this direction is more
      dangerous. If the judgement were made after `rmtree`, then when
      `destination_path.exists()` is true it would first run
      `shutil.rmtree(destination_path)`, and that tree contains the live source -- before
      `copytree` even starts, the source data plus other unrelated files under destination
      have been deleted, and `copytree` then crashes because the source is gone, with the loss
      already beyond recovery. This is not a scenario that "cleaning up a stale existing
      target" could save (the target might not have existed at all to begin with), so both
      directions must be blocked before any rmtree/copytree.

    Deliberately a pure path judgement that touches no filesystem: main.py must call it before
    a run starts -- the snapshot is usually the last step of a long run, and if a path
    conflict only errored at that point, the preceding hours of work would be wasted; a pure
    path judgement can be computed immediately at startup, without waiting for intent_dir to
    actually be created.
    """
    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()

    if destination_path == source_path:
        raise ValueError(
            f"snapshot destination is the same as the source directory: destination={destination_path} source={source_path}"
        )
    if destination_path.is_relative_to(source_path):
        raise ValueError(
            f"snapshot destination must not be inside the source directory: destination={destination_path} "
            f"source={source_path}"
        )
    if source_path.is_relative_to(destination_path):
        raise ValueError(
            f"snapshot destination must not be an ancestor of the source directory (it would delete the source data before copying): "
            f"destination={destination_path} source={source_path}"
        )


def assert_snapshot_destination_is_free(
    destination: Path | str, overwrite: bool = False
) -> None:
    """When the snapshot destination already exists, refuse unless overwriting was explicitly
    requested.

    The snapshot directory is a **read-only baseline shared across arms**: run.sh makes all
    six arms use --intent-dir intents-warm-r1, and that directory is the common origin of
    every number. Rerunning the warmup command once (restarting after a crash, wanting to run
    a few more tasks, or merely scrolling back to that line in the shell and hitting enter)
    would, under the old unconditional-rmtree behaviour, replace it entirely: the baseline
    every previous arm compared against disappears, no error is raised, and it cannot be
    restored. The intent_dir_base and taxonomy_size_start recorded in meta.json are enough to
    notice afterwards that the baseline changed, but not enough to bring it back.

    This is exactly the class of bug this round of changes exists to eradicate ("running the
    same arm a second time continues from the first run's results and irreversibly overwrites
    them") -- fork solved the working-directory half, but the snapshot-destination half could
    still be overwritten. A round suffix like `-r1` is only a convention that nothing
    enforces, so the enforcement has to live here.

    overwrite can only be turned on explicitly by the caller (--snapshot-overwrite), meaning
    "I know which baseline I am discarding".
    """
    if overwrite:
        return
    destination_path = Path(destination)
    if destination_path.exists():
        raise FileExistsError(
            f"snapshot destination already exists, refusing to overwrite: {destination_path}. It may be "
            "the read-only baseline other experiment arms compare against, and it cannot be restored once "
            "overwritten. Use a new round directory name instead (e.g. ...-r2), or explicitly pass "
            "--snapshot-overwrite true when you confirm you want to discard it."
        )


def fork_intent_dir(source: Path | str, destination: Path | str) -> str:
    """Copy the source intent library to destination and return destination's string path.

    The difference from snapshot_intent_dir is timing and direction: the snapshot is the
    archive taken at the **end** of a run, the fork is the branching done at the **start**.
    After forking, the source directory is read-only throughout and all of this run's
    evolution lands on the copy -- otherwise, running the same arm twice would make the second
    run continue from the first run's results instead of rerunning, and the first run's
    instance files would be rewritten in place and could not be recovered.

    A missing source is a legal cold start (spec section 4.4), in which case only the empty
    directory structure is created and nothing errors; that is also why, unlike
    snapshot_intent_dir, this does not call ensure() on source -- the source must stay
    read-only, and any "convenient" directory creation on it violates that contract.
    """
    source_path = Path(source)
    destination_path = Path(destination)
    assert_safe_snapshot_pair(source_path, destination_path)
    if destination_path.exists():
        shutil.rmtree(destination_path)
    if source_path.exists():
        shutil.copytree(source_path, destination_path)
    intent_paths(destination_path).ensure()
    return str(destination_path)


def snapshot_intent_dir(
    source: Path | str, destination: Path | str, overwrite: bool = False
) -> Path:
    """Copy the whole intent library to the snapshot directory, erroring when the destination
    exists (only overwrite=True clears it first).

    A missing source is treated as an empty taxonomy, and `ensure()` builds the directory
    skeleton first and then copies, so that every round's snapshot has a consistent directory
    structure and callers need not special-case "have not run a round yet".

    The overwrite protection lives here rather than at main.py's call site so that every
    caller (today's run pipeline, tomorrow's scripts) inherits it automatically instead of each
    remembering to check again; see assert_snapshot_destination_is_free for the reasoning.
    """
    assert_safe_snapshot_pair(source, destination)
    assert_snapshot_destination_is_free(destination, overwrite)
    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()

    intent_paths(source_path).ensure()
    if destination_path.exists():
        shutil.rmtree(destination_path)
    shutil.copytree(source_path, destination_path)
    return destination_path
