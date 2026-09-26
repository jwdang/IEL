import concurrent.futures
import os
import json
import random
import traceback
from math import comb
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress
from envs import ENV_NAMES, get_env
from llm_config import get_llm_config
from utils import (
    AGENT_IMPL_INTENT,
    AGENT_IMPL_OFFICIAL,
    RunConfig,
    console_verbose,
    EnvRunResult,
    DetailReward,
    is_retryable_connection_error,
)
from intent.config import intent_paths
from intent.snapshot import (
    assert_safe_snapshot_pair,
    assert_snapshot_destination_is_free,
    fork_intent_dir,
    snapshot_intent_dir,
    taxonomy_size,
)
from intent.taxonomy import Taxonomy
from folds import FoldSelection, default_spec_path, select_folds
import traceback
import asyncio

def _slugify_model(model_name: str) -> str:
    """A model id may contain '/' (e.g. Qwen/Qwen3-VL-32B-Instruct) and cannot go straight into a filename."""
    return model_name.replace("/", "-").replace(":", "-")


def _run_dir_name(*, inject: bool, evolve: bool, fold_label: str = "") -> str:
    """The result directory name records the arm shape of this run (inject / evolve).

    fold_label is appended only when running by fold (of the form
    `_story-3fold-s10_grow-fold2+fold3_test-fold1`, assembled by folds.fold_label).
    The three cross-validation rounds are identical in every other dimension -- same
    model, same arm -- and this segment is the only difference. Without it in the
    directory name, the three rounds would be distinguishable only by timestamp, yet
    "which 18 tasks was this results.json measured on" is a precondition for reading it.

    Appended rather than added as a new directory level: the reporting section of
    scripts/run_*.sh finds results recursively via `<results root>/**/meta.json`, so one
    more level would not be missed; but once the naming of existing result directories
    changes, there is no way to match historical runs afterwards, so we keep appending
    instead of restructuring the directory hierarchy.
    """
    name = f"inject-{int(bool(inject))}_evolve-{int(bool(evolve))}"
    return f"{name}_{fold_label}" if fold_label else name


# Upper bound on whole-task retries for connection-class / rate-limit errors. Model
# behaviour errors (e.g. recursion limit, output format) are not included -- retrying
# the same problem serves no purpose.
MAX_TASK_ATTEMPTS = 3


def _task_order(
    config: RunConfig, end_index: int, fold_task_ids: Optional[List[int]] = None
) -> List[int]:
    """The task execution order for this trial.

    --seed determines the random source for the shuffle: reproducible multi-seed
    growth curves depend on "same seed -> same task order". This used to call bare
    random.shuffle (the process random source), so two runs with identical arguments
    had different task orders and the growth curve could not be reproduced. When
    task_ids is given explicitly we do not shuffle (explicit order wins), and we must
    copy it -- shuffle mutates config.task_ids in place and would pollute the config
    recorded in meta.json.

    When fold_task_ids is given (running by fold), we shuffle the **full** index range
    by seed first and then filter down to the ones in this fold, rather than shuffling
    the ids inside the fold directly. Both are reproducible, but the former preserves
    one extra property: the relative order of the tasks within the fold is **exactly
    the same** as in a full run, so a "growth run for this round" and a "full growth
    run" differ only by "the test-fold tasks were removed", and the growth curves can
    be compared point by point. If we shuffled the in-fold ids directly, the two curves
    would have unrelated task orders and the difference would be mixed with a pure
    order effect whose origin could not be identified.
    """
    if config.task_ids and len(config.task_ids) > 0:
        return list(config.task_ids)
    idxs = list(range(config.start_index, end_index))
    if config.shuffle:
        random.Random(config.seed).shuffle(idxs)
    if fold_task_ids is not None:
        selected = set(fold_task_ids)
        idxs = [i for i in idxs if i in selected]
    return idxs


def _write_checkpoint(path: str, results: List[EnvRunResult]) -> None:
    """Write the completed results to the checkpoint file (atomic replace, so an
    interruption cannot corrupt the JSON).

    Progress is not lost when a long run (53 tasks x several arms) is interrupted or
    crashes midway: this is called once per finished task. It writes a temp file and
    then renames, so a killed process never leaves behind half a JSON.
    """
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in results], f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def _empty_tool_audit(termination: str) -> Dict[str, Any]:
    """When a task times out or raises, no execution information is available, but we
    still have to record which class of termination it was."""
    return {
        "intent_decompositions": [],
        "tool_repeat_warnings": 0,
        "tool_repeat_blocks": 0,
        "agent_executed_tools": [],
        "ground_truth_searches": [],
        "ground_truth_actions": [],
        "ground_truth_outputs": [],
        "total_turns": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "intent_prompt_tokens": 0,
        "intent_completion_tokens": 0,
        "intent_total_tokens": 0,
        "intent_llm_calls": 0,
        "intent_uncounted_llm_calls": 0,
        "termination": termination,
        "task_instruction": None,
        "turn_latencies": [],
        "turn_token_usage": [],
    }


def _assert_safe_concurrency(config: RunConfig) -> None:
    """Block the "concurrently evolving the same intent library" combination.

    intent/pipeline.py is by design unlocked and serial: one pipeline call does
    load -> (several seconds of LLM round-trips) -> save taxonomy/ledger/evolution_log.
    When several threads run the same intent_dir concurrently, that window has no
    mutual exclusion and they overwrite each other's writes -- candidate counts are
    undercounted, entries that should have been admitted are not, and the records in
    evolution_log no longer match the actual state of the taxonomy. Nothing raises,
    no test fails; it just quietly produces a taxonomy that is too small and wrong.
    Rather than add locking (which would violate the established "serial execution"
    design), we simply refuse this combination at startup. With --evolve false there
    are no writes at all, so any level of concurrency is safe.
    """
    if config.evolve and config.max_concurrency > 1:
        raise ValueError(
            "evolve=True and max_concurrency>1 cannot be used together: multiple threads "
            "would concurrently read and write the same intent library (taxonomy.yaml / "
            "ledger.json / evolution_log.jsonl), and the evolution pipeline is by design "
            "unlocked. Pass --max-concurrency 1 to evolve serially, or pass --evolve false "
            "to turn off taxonomy evolution before raising concurrency."
        )


def _resolve_fold_selection(config: RunConfig) -> Optional[FoldSelection]:
    """Resolve the cross-validation fold selection and block several combinations that
    would silently run wrong.

    When --grow-folds/--test-folds are not given, returns None: that is a full run and
    this function changes no behaviour (the same is true when --fold-spec is given on
    its own, since it only points at where to find a spec).

    Three refusals:

    1. **--task-ids given together with folds.** Both answer "which tasks to run", so
       giving both means two answers. Letting one silently win costs the hardest kind
       of bug to track down: the result directory says `test-fold1` while a different
       set of tasks was actually run.

    2. **--start-index/--end-index given together with folds.** Folds select by task id,
       the range truncates by index, and once the two intersect what actually runs is
       the intersection -- some in-fold tasks are silently dropped, while results.json
       merely "has a few fewer entries", with nothing showing they were truncated.

    3. **--test-folds with --evolve true.** This is the one thing cross-validation
       exists to prevent: evolving on the test fold feeds the test fold's episodes into
       the experience library, after which every evaluation measures training-set
       performance. It raises nothing, does not slow down, it only makes the numbers
       look better -- so it must be blocked at startup, not left to whoever runs the
       batch remembering to turn evolve off.
    """
    selection = select_folds(
        # Empty string = use the default spec for this dataset. The two datasets have
        # different task counts (53 / 60), so the default spec cannot be hardcoded to
        # one: the spec for the wrong dataset would be caught by the num_tasks check,
        # but it could also just happen to mismatch -- so we resolve by env from the start.
        config.fold_spec or default_spec_path(config.env),
        config.grow_folds or [],
        config.test_folds or [],
    )
    if selection is None:
        return None
    if config.task_ids:
        raise ValueError(
            f"--task-ids {config.task_ids} and fold selection (grow={list(selection.grow)} "
            f"test={list(selection.test)}) cannot be used together: both specify which tasks "
            "to run. To run a fold, pass only fold; to run specific tasks, do not pass fold."
        )
    if config.start_index != 0 or config.end_index != -1:
        raise ValueError(
            f"--start-index/--end-index (currently {config.start_index}/{config.end_index}) "
            "cannot be used together with fold selection: the range would truncate part of "
            "the in-fold tasks, and the results would not show which ones are missing. When "
            "running by fold, keep the range at its default values."
        )
    if selection.test and config.evolve:
        raise ValueError(
            f"--test-folds {list(selection.test)} with --evolve true would evolve the "
            "experience library on the test fold -- exactly the data leakage cross-validation "
            "exists to prevent, after which every evaluation round measures training-set "
            "performance. For the evaluation stage pass --evolve false; to grow on these "
            "tasks, pass them as --grow-folds."
        )
    return selection


def _warn_if_the_vocabulary_looks_unusable(config: RunConfig, working_intent_dir: str) -> None:
    """When the vocabulary is unusable but the configuration itself is legal, we must at
    least shout about it rather than run to completion silently.

    After run.sh makes every evolve arm warm start from intents-warm-r1, if the warmup
    produces a thin vocabulary (not a single active intent with
    requires_terminal_action true), or if --intent-dir was mistyped as intents-warm-rl,
    the run still starts normally -- fork treats the missing source as a legal cold start
    and builds an empty library, nothing can be recalled in the end, and it reads like
    "the method does not help" when in fact the experience library was empty from the
    start.

    So we separate "a deliberate cold start" from "the source is missing / unusable":
    the former stays legal, the latter is no longer silent. We use console_verbose.print
    rather than .log -- every arm in run.sh runs under --verbose false, where .log
    outputs nothing, and this notice is valuable precisely in that scenario.
    """
    if not os.path.exists(config.intent_dir):
        console_verbose.print(
            f"[bold red]INTENT-DIR-MISSING: --intent-dir {config.intent_dir!r} does not "
            "exist, so this run is treated as a cold start (empty vocabulary). If this is a "
            "warm-start arm, the path is wrong -- stop now and double-check the snapshot "
            "directory name.[/bold red]"
        )
    taxonomy = Taxonomy(intent_paths(working_intent_dir).taxonomy)
    taxonomy.load()
    if not any(intent.requires_terminal_action is True for intent in taxonomy.active()):
        console_verbose.print(
            f"[bold red]VOCAB-NO-TERMINAL: the working vocabulary "
            f"{working_intent_dir!r} has no active intent with requires_terminal_action "
            "true, so terminality judging has no anchor right now. Cold starts and online "
            "growth are legal, but if the vocabulary never grows such intents, this arm's "
            "terminality coverage metric is uninterpretable.[/bold red]"
        )


def _resolve_working_intent_dir(config: RunConfig, run_dir: str) -> str:
    """Determine the intent library directory this run actually reads and writes.

    With evolve=true we fork a copy to <run_dir>/intents/ and the source directory stays
    read-only throughout; with evolve=false there are no writes at all, so we use the
    source directory directly instead of making a pointless copy.
    """
    if not config.evolve:
        working_intent_dir = config.intent_dir
    else:
        working_intent_dir = fork_intent_dir(
            config.intent_dir, os.path.join(run_dir, "intents")
        )
    _warn_if_the_vocabulary_looks_unusable(config, working_intent_dir)
    return working_intent_dir


def _resolve_metrics_dir(config: RunConfig, run_dir: str) -> str:
    """Where the mechanism metrics of the frozen evaluation stage (evolve=false) land.

    An empty string means not collected. With evolve=true the instances are already
    written into the working copy, so opening a second metrics directory would only
    write the same instances twice.

    The frozen stage, on the other hand, must have a destination **outside the library**:
    intent_dir is the shared read-only measuring instrument of every evaluation arm (the
    taxonomy supplies requires_terminal_action, which outcome judging depends on), and
    the frozen stage runs concurrently -- writing into it would let the arms pollute each
    other, and the differences between arms would no longer be just configuration
    differences. Not made a command-line switch: it has no second sensible destination,
    and one more switch is just one more place to misconfigure.
    """
    if config.evolve:
        return ""
    return os.path.join(run_dir, "metrics")


def _assert_baseline_is_official(config: RunConfig) -> None:
    """A baseline-shaped configuration must use the official executor, or we refuse to start.

    "inject/evolve both off" is semantically the baseline, but it previously still ran
    this paper's own execution graph -- with tool-repeat interception and intent nodes --
    which is not the same thing as the official create_react_agent. The measured
    consequence: the baseline score was mixed with this paper's changes, so "method vs
    baseline" measured the method plus a pile of unrelated changes, and cross-paper
    comparison lost its meaning.
    """
    baseline_shaped = not config.inject and not config.evolve
    if baseline_shaped and config.agent_impl != AGENT_IMPL_OFFICIAL:
        raise ValueError(
            "--inject false --evolve false is the baseline configuration and must be "
            f"combined with --agent-impl {AGENT_IMPL_OFFICIAL}: the default "
            f"{AGENT_IMPL_INTENT} runs this paper's own execution graph (with tool-repeat "
            "interception and intent nodes), not the official ECom-Bench "
            "create_react_agent, so what it produces is not a baseline."
        )


def _assert_safe_snapshot(config: RunConfig) -> None:
    """The path checks for --snapshot-dir and "is the destination already taken" must be
    done at startup.

    The snapshot is the last step of the run (see the end of run()); if these checks were
    left until then, a batch that runs for hours would fail at the very end on a path
    conflict and everything before it would be wasted. intent.snapshot.
    assert_safe_snapshot_pair is a pure path judgement that touches no filesystem, so it
    is safe to call here early; assert_snapshot_destination_is_free reads the filesystem
    once (an exists check only, changing nothing), and it too can run early -- in fact
    early is where it pays off most, since "the destination already exists" is the check
    a rerun of the warmup command is bound to hit, and it should not be caught hours
    later. It still runs again inside snapshot_intent_dir, which is the authoritative
    position: this is a head start, not a replacement. When snapshot_dir is the empty
    string (the default, no snapshot) we skip entirely.

    What actually gets snapshotted is working_intent_dir (see
    _resolve_working_intent_dir), not config.intent_dir -- after fork lands, the two are
    the same only when evolve=false. But working_intent_dir depends on the timestamp in
    run_dir, and at the time this function is called (run() calls it immediately on
    entry) the timestamp has not been generated, so we cannot obtain working_intent_dir
    itself for the check. As a fallback we check a structural fact that always holds:
    whether or not it forks, working_intent_dir always lives under config.log_dir (when
    forking, `<log_dir>/.../<timestamp>/intents`; when not, the intent_dir check below
    hits it directly). Substituting log_dir for working_intent_dir is a conservative
    approximation -- other subdirectories under log_dir that are actually unrelated to
    snapshot_dir get blocked as well, but in exchange startup genuinely covers the
    directory that will be snapshotted, instead of only validating a path pair the run
    never uses as it did before fork.
    """
    if not config.snapshot_dir:
        return
    assert_snapshot_destination_is_free(config.snapshot_dir, config.snapshot_overwrite)
    assert_safe_snapshot_pair(config.log_dir, config.snapshot_dir)
    # When evolve=false, working_intent_dir is config.intent_dir itself (no fork), so
    # this check hits the exact pair of paths that will be copied, and it is load-bearing.
    # When evolve=true the source directory is read-only throughout and is never used by
    # copytree as a source (the real source is the forked copy, already covered by the
    # log_dir check above), so continuing to check here is only defensive hygiene: it
    # rejects one harmless combination (e.g. --snapshot-dir <intent_dir>/snap), in
    # exchange for which the rule "the source and snapshot directories must not contain
    # one another" does not have to fork on evolve, and callers do not have to remember
    # two mental models. Weighing it up, we keep it rather than adding
    # `if not config.evolve:` to let it through.
    assert_safe_snapshot_pair(config.intent_dir, config.snapshot_dir)


def _git_commit() -> str:
    """Record the code version this experiment ran at, so results are traceable to an
    implementation."""
    try:
        import subprocess

        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return "unknown"


async def run(config: RunConfig) -> List:
    # The dataset must come from the registry: with a hardcoded list, adding a dataset
    # would silently let through a name envs.get_env does not know, and it would only
    # blow up inside get_env after the directories were built.
    assert config.env in ENV_NAMES, f"unknown dataset {config.env!r}, available: {ENV_NAMES}"
    _assert_safe_concurrency(config)
    _assert_baseline_is_official(config)
    _assert_safe_snapshot(config)
    # Fold resolution must happen before the directories are built: run_dir's name carries
    # the fold label, and all three refusals here (see the function docstring) are
    # "the configuration itself is wrong", so they must be reported before the first
    # token is spent.
    fold_selection = _resolve_fold_selection(config)
    random.seed(config.seed)
    max_time = config.max_time
    time_str = datetime.now().strftime("%m%d_%H%M%S")
    # results/agent-<model>_user-<model>/inject-<0|1>_evolve-<0|1>[_<fold-label>]/<timestamp>/{results,meta}.json
    #
    # The model in the directory name must be the one that is **actually in effect**; we
    # cannot just copy config.agent_model/user_model -- those are CLI labels, and when
    # left empty (the recommended usage, see run.py's help) the real model comes from
    # AGENT_LLM_MODEL/USER_LLM_MODEL in .env. Running get_llm_config performs exactly the
    # same resolution as LLM._initiate_llm (a non-empty CLI value overrides, otherwise
    # .env is read), so the directory name matches the model this run actually calls and
    # we never get "changed .env but the directory name/log did not change".
    agent_model_resolved = get_llm_config("agent", config.agent_model).model
    user_model_resolved = get_llm_config("user", config.user_model).model
    run_dir = os.path.join(
        config.log_dir,
        f"agent-{_slugify_model(agent_model_resolved)}_user-{_slugify_model(user_model_resolved)}",
        _run_dir_name(
            inject=config.inject,
            evolve=config.evolve,
            fold_label=fold_selection.label if fold_selection else "",
        ),
        time_str,
    )
    os.makedirs(run_dir, exist_ok=True)
    # With evolve=true we fork the source intent library under run_dir, and this run reads
    # and writes the copy throughout while the source directory stays read-only; with
    # evolve=false there are no writes, so we use the source directory directly. From here
    # on, everything that reads or writes the intent library uses working_intent_dir and
    # must not touch config.intent_dir again (that is the read-only source, only allowed to
    # be read when checking "is the source usable").
    working_intent_dir = _resolve_working_intent_dir(config, run_dir)
    metrics_dir = _resolve_metrics_dir(config, run_dir)
    ckpt_path = os.path.join(run_dir, "results.json")
    meta_path = os.path.join(run_dir, "meta.json")
    console_verbose.reset(config.verbose)

    # The taxonomy is continuously modified by the evolve pipeline during the run, so the
    # starting size must be sampled before the first episode begins; otherwise there is no
    # way afterwards to know how much this run actually changed.
    intent_dir_paths = intent_paths(working_intent_dir)
    taxonomy_size_start = taxonomy_size(intent_dir_paths)

    env = get_env(
        env_name=config.env,
        user_model=config.user_model,
        agent_model=config.agent_model,
        inject=config.inject,
        evolve=config.evolve,
        agent_impl=config.agent_impl,
        console_verbose=console_verbose,
        intent_dir=working_intent_dir,
        run_id=time_str,
        metrics_dir=metrics_dir,
    )
    end_index = (
        len(env.tasks) if config.end_index == -1 else min(config.end_index, len(env.tasks))
    )
    # The spec's ids were assigned for the task set as it was back then; if the environment's
    # task count has changed they are no longer the same tasks. This check has to wait until
    # here: env is only built at this point.
    fold_task_ids = None
    if fold_selection is not None:
        fold_selection.spec.assert_matches_env(len(env.tasks))
        fold_task_ids = list(fold_selection.task_ids)
    all_env_results = [] # results of num_trials, used to record details
    all_tasks_results = [] # results of num_trials, used to record success/failure
    if fold_selection is not None:
        console_verbose.print(
            f"[yellow]Running fold {fold_selection.role}={'+'.join(fold_selection.test or fold_selection.grow)} "
            f"of {fold_selection.spec.name}: {len(fold_task_ids)} tasks {fold_task_ids} "
            f"(checkpoint path: {ckpt_path})[/yellow]"
        )
    elif config.task_ids and len(config.task_ids) > 0:
        console_verbose.print(f"[yellow]Running tasks {config.task_ids} (checkpoint path: {ckpt_path})[/yellow]")  # Running tasks
    else:
        console_verbose.print(
            f"[yellow]Running tasks {config.start_index} to {end_index} (checkpoint path: {ckpt_path})[/yellow]"  # Task range
        )
        
    with Progress() as progress:
        for i in range(config.num_trials):
            idxs = _task_order(config, end_index, fold_task_ids)
            # Bind the current trial explicitly: _run executes in a thread pool, and i is
            # reassigned later in the printing loop below, so a closure over i is not
            # reliable. The trial must go into episode_id, otherwise multiple trials
            # overwrite each other's instance files (see MockStoryEnv.trial_index).
            trial_index = i

            def _run(idx: int, trial_index: int = trial_index) -> Tuple[float, Dict]:
                # Whole-task retry for connection-class errors (at most MAX_TASK_ATTEMPTS
                # times). Retry safety rests on this: such failures all happen during the
                # dialogue stage (the graph call raises), when the intent pipeline has not
                # yet run and no evidence has been written. If a failure path that raises
                # *after* the pipeline ever appears, this must gate the retry on whether
                # the pipeline has already run, or the same episode's evidence would be
                # banked twice.
                for attempt in range(MAX_TASK_ATTEMPTS):
                    isolated_env = get_env(
                        env_name=config.env,
                        user_model=config.user_model,
                        agent_model=config.agent_model,
                        inject=config.inject,
                        evolve=config.evolve,
                        agent_impl=config.agent_impl,
                        console_verbose=console_verbose,
                        task_index=idx,
                        intent_dir=working_intent_dir,
                        run_id=time_str,
                        trial_index=trial_index,
                        metrics_dir=metrics_dir,
                    )
                    try:
                        async def run_with_timeout():
                            return await isolated_env.a_run(user_strategy=config.user_strategy, agent_strategy=config.agent_strategy)
            
                        reward, traj, detail_reward, tool_audit = asyncio.run(
                            asyncio.wait_for(run_with_timeout(), timeout=max_time)
                        )
                        task_result_str = (
                            f"✅" if reward > 0 else f"❌",
                            f"task_id={idx}",
                            # result.info,
                            # "\n[dim]-----------------------------------------------------------------[/dim]"
                        )
                    except asyncio.TimeoutError:
                    # handle the timeout error
                        reward, traj = 0.0, [{"error": f"Task {idx} timed out after {max_time} seconds", "timeout": True}]
                        detail_reward = {"action": 0, "search": 0, "output": 0, "time": max_time}
                        tool_audit = _empty_tool_audit("timeout")

                        console_verbose.print(f"[red]\nTask {idx} timed out ({max_time}s)[/red]")
                        task_result_str = (
                            f"⏰",  # clock emoji to indicate a timeout
                            f"task_id={idx}",
                        )
                    except Exception as e:
                        if is_retryable_connection_error(e) and attempt < MAX_TASK_ATTEMPTS - 1:
                            console_verbose.print(
                                f"[yellow]\nTask {idx} hit a connection-class error "
                                f"({type(e).__name__}: {e}), "
                                f"attempt {attempt + 2}/{MAX_TASK_ATTEMPTS}[/yellow]"
                            )
                            continue
                        reward, traj = 0.0, [{"error": str(e), "traceback": traceback.format_exc()}]
                        detail_reward = {"action": 0, "search": 0, "output": 0, "time": 0.0}
                        tool_audit = _empty_tool_audit("error")
                        console_verbose.print(f"[red]\nError while processing task {idx}: {str(e)}[/red]")
                        console_verbose.print(traceback.format_exc())  # this prints the full stack trace
                        task_result_str = (
                            f"✅" if reward > 0 else f"❌",
                            f"task_id={idx}",
                            # result.info,
                            # "\n[dim]-----------------------------------------------------------------[/dim]"
                        )
                    env_run_result = EnvRunResult(
                        reward=reward,
                        task_id=idx,
                        traj=traj,
                        trial=trial_index,
                        detail_reward=DetailReward(
                            **detail_reward
                        ),
                        total_turns=int(tool_audit.get("total_turns") or 0),
                        prompt_tokens=int(tool_audit.get("prompt_tokens") or tool_audit.get("agent_prompt_tokens") or 0),
                        completion_tokens=int(tool_audit.get("completion_tokens") or tool_audit.get("agent_completion_tokens") or 0),
                        total_tokens=int(tool_audit.get("total_tokens") or tool_audit.get("agent_total_tokens") or 0),
                        intent_prompt_tokens=int(tool_audit.get("intent_prompt_tokens") or 0),
                        intent_completion_tokens=int(tool_audit.get("intent_completion_tokens") or 0),
                        intent_total_tokens=int(tool_audit.get("intent_total_tokens") or 0),
                        intent_llm_calls=int(tool_audit.get("intent_llm_calls") or 0),
                        intent_uncounted_llm_calls=int(tool_audit.get("intent_uncounted_llm_calls") or 0),
                        intent_decompositions=tool_audit.get("intent_decompositions"),
                        tool_repeat_warnings=int(tool_audit.get("tool_repeat_warnings") or 0),
                        tool_repeat_blocks=int(tool_audit.get("tool_repeat_blocks") or 0),
                        agent_executed_tools=tool_audit.get("agent_executed_tools"),
                        ground_truth_searches=tool_audit.get("ground_truth_searches"),
                        ground_truth_actions=tool_audit.get("ground_truth_actions"),
                        ground_truth_outputs=tool_audit.get("ground_truth_outputs"),
                        termination=tool_audit.get("termination"),
                        task_instruction=tool_audit.get("task_instruction"),
                        turn_latencies=tool_audit.get("turn_latencies"),
                        turn_token_usage=tool_audit.get("turn_token_usage"),
                    )
                    # It must return inside the for loop: any attempt that succeeds (or hits
                    # a non-retryable error) returns that attempt's result immediately. A
                    # previous version had the return outside the loop, which ran every task
                    # 3 full times (the first two results were overwritten and discarded,
                    # tripling token cost, and the same task appearing 3 times in the growth
                    # sequence polluted the taxonomy).
                    return (env_run_result, task_result_str)

            task_progress = progress.add_task(f"[yellow]Trial {i + 1} tasks", total=len(idxs))
            env_results = [] # results of each trial, rewards
            tasks_results = [] # results of each trial
            with ThreadPoolExecutor(max_workers=config.max_concurrency) as executor:
                # submit all tasks
                future_to_idx = {executor.submit(_run, idx): idx for idx in idxs}
                # process completed results
                for future in concurrent.futures.as_completed(future_to_idx):
                    idx = future_to_idx[future]
                    try:
                        result = future.result()
                        env_results.append(result[0])
                        tasks_results.append(result[1])
                        # update task progress
                        progress.update(task_progress, advance=1)
                        # Write a checkpoint after every finished task: progress is not lost
                        # when a long run is interrupted or crashes midway (previously it was
                        # written only once at the end of run(), so a variable named
                        # checkpoint served no checkpoint purpose).
                        _write_checkpoint(ckpt_path, [*all_env_results, *env_results])
                    except Exception as e:
                        console_verbose.print(f"[red]\nError while processing task {idx}: {str(e)}[/red]")
                        console_verbose.print(traceback.format_exc())  # this prints the full stack trace

            all_env_results.extend(env_results)
            all_tasks_results.append({"num_trial": i+1, "results": tasks_results})
            progress.remove_task(task_progress)
            # print all task results together
            console_verbose.print("\n[bold blue]===== Task result summary =====[/bold blue]")
            for results in all_tasks_results:
                console_verbose.print(f"[bold blue]Trial {results['num_trial']}[/bold blue]:\n")
                batch_size = 10
                for i in range(0, len(results['results']), batch_size):  
                    batch_results = results['results'][i:i+batch_size]
                    batch_results = [' '.join(r) for r in batch_results]
                    console_verbose.print(f"[bold blue] {'  '.join(batch_results)}")
                console_verbose.print("\n[bold blue]-------------------[/bold blue]\n")


    display_metrics(all_env_results) 

    _write_checkpoint(ckpt_path, all_env_results)

    # Sample the size once more after all tasks have run, and write it into meta together
    # with the starting value; this pair of numbers is the net effect this run had on the
    # taxonomy.
    taxonomy_size_end = taxonomy_size(intent_dir_paths)

    meta = {
        "run_id": time_str,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "git_commit": _git_commit(),
        "config": config.model_dump(),
        # config.agent_model/user_model may be empty strings (the recommended usage of
        # leaving them blank and going through .env), in which case config alone does not
        # say which model this run actually called. These two fields record the real model
        # ids resolved by get_llm_config, so they can be checked afterwards or on a resume.
        "resolved_agent_model": agent_model_resolved,
        "resolved_user_model": user_model_resolved,
        "num_records": len(all_env_results),
        "task_ids": sorted({r.task_id for r in all_env_results}),
        # Fold provenance: spec file, spec name, growth folds, test folds, and the task set
        # actually selected this time. config already holds the **input values** of
        # fold_spec/grow_folds/test_folds; what is recorded here is the resolved **result**
        # -- if the spec file is modified or renamed afterwards, a mismatch between the two
        # is clear evidence. All None when not running by fold, so the existing way of
        # reading meta.json is unchanged.
        "fold_spec_path": str(fold_selection.spec.path) if fold_selection else None,
        "fold_spec_name": fold_selection.spec.name if fold_selection else None,
        "fold_label": fold_selection.label if fold_selection else None,
        "grow_folds": list(fold_selection.grow) if fold_selection else None,
        "test_folds": list(fold_selection.test) if fold_selection else None,
        "fold_role": fold_selection.role if fold_selection else None,
        "fold_task_ids": fold_task_ids,
        "intent_dir_base": config.intent_dir,
        "intent_dir_working": working_intent_dir,
        "inject": config.inject,
        "evolve": config.evolve,
        "taxonomy_size_start": taxonomy_size_start,
        "taxonomy_size_end": taxonomy_size_end,
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    console_verbose.print(f"\n[blue]📄 Results saved to {run_dir}[/blue]\n")  # Saved result info

    # The snapshot is the very last step of the pipeline and captures the state of the
    # intent library after this run finished; the intent_dir_paths.root passed here is
    # working_intent_dir itself, which _assert_safe_snapshot could not check directly at
    # startup (the timestamp did not exist yet) and instead checked via its structural
    # upper bound config.log_dir (working_intent_dir always lives under it) against the
    # safety of snapshot_dir; when evolve=false, working_intent_dir is config.intent_dir
    # itself, and that check additionally covered this exact pair of paths.
    if config.snapshot_dir:
        snapshot_intent_dir(
            intent_dir_paths.root, config.snapshot_dir, config.snapshot_overwrite
        )
        console_verbose.print(
            f"[blue]📸 Intent dir snapshotted to {config.snapshot_dir}[/blue]\n"
        )

    return all_env_results



def display_metrics(results: List[EnvRunResult]) -> None:
    
    def is_successful(reward: float) -> bool:
        return 0+1e-6 < reward <= (1 + 1e-6)

    num_trials = len(set([r.trial for r in results]))
    rewards = [r.reward for r in results]
    avg_reward = sum(rewards) / len(rewards)
    avg_turns = sum(r.total_turns for r in results) / len(results)
    avg_prompt_tokens = sum(r.prompt_tokens for r in results) / len(results)
    avg_completion_tokens = sum(r.completion_tokens for r in results) / len(results)
    avg_total_tokens = sum(r.total_tokens for r in results) / len(results)
    # c from https://arxiv.org/pdf/2406.12045
    c_per_task_id: dict[int, int] = {}
    for result in results:
        if result.task_id not in c_per_task_id:
            c_per_task_id[result.task_id] = 1 if is_successful(result.reward) else 0
        else:
            c_per_task_id[result.task_id] += 1 if is_successful(result.reward) else 0
    pass_hat_ks: dict[int, float] = {}
    # binomial coefficients
    # Example: (5, 3 ✅, 2❌), one task repeated 5 times. k = 1 means: the probability of
    # succeeding once; k = 2 means: the probability of succeeding twice
    for k in range(1, num_trials + 1):
        sum_task_pass_hat_k = 0
        for c in c_per_task_id.values():
            sum_task_pass_hat_k += comb(c, k) / comb(num_trials, k)
        pass_hat_ks[k] = sum_task_pass_hat_k / len(c_per_task_id)
    console_verbose.print(f"🏆 Average reward: {avg_reward}")
    console_verbose.print(f"🔁 Average turns: {avg_turns}")
    avg_intent_total_tokens = sum(r.intent_total_tokens for r in results) / len(results)
    avg_intent_calls = sum(r.intent_llm_calls for r in results) / len(results)
    uncounted_intent_calls = sum(r.intent_uncounted_llm_calls for r in results)
    console_verbose.print(
        "🧮 Average agent token cost: "
        f"prompt={avg_prompt_tokens}, completion={avg_completion_tokens}, total={avg_total_tokens}"
    )
    # The intent system's cost is listed separately: the main-dialogue figures exclude it,
    # and a cost comparison must add the two together
    console_verbose.print(
        "🧠 Average intent-system token cost: "
        f"total={avg_intent_total_tokens}, calls={avg_intent_calls}"
    )
    if uncounted_intent_calls:
        console_verbose.print(
            f"⚠️  {uncounted_intent_calls} intent LLM calls returned no usage metadata "
            "and are excluded from the token totals above"
        )
    console_verbose.print("📈 Pass^k")
    for k, pass_hat_k in pass_hat_ks.items():
        console_verbose.print(f"  k={k}: {pass_hat_k}")

