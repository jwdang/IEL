# Copyright Sierra

import argparse
import os
from folds import default_spec_path
from utils import AGENT_IMPL_INTENT, AGENT_IMPLS, RunConfig
from envs import ENV_NAMES
from llm_config import resolve_model_name
from main import run
import asyncio
from rich.console import Console
import signal
import sys
console = Console()


def _str2bool(value):
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y", "on"}:
        return True
    if text in {"false", "0", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError("Expected a boolean value: true/false")


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-trials", type=int, default=1)
    parser.add_argument(
        "--env", type=str, choices=list(ENV_NAMES), default=ENV_NAMES[0],
        help="dataset: story=ECom-Bench (53 tasks, home appliances); xcat=ECom-Bench-XCAT"
             " (60 tasks, apparel + food). The two datasets share the same environment "
             "implementation and tool interface.",
    )
    parser.add_argument(
        "--user-model",
        type=str,
        default="",
        help="Model id for the user simulator (defaults to USER_LLM_MODEL in .env)",
    )
    parser.add_argument(
        "--user-strategy",
        type=str,
        choices=['human', 'based', 'cot'],
        default='based',
    )
    parser.add_argument(
        "--agent-model",
        type=str,
        default="",
        help="Model id for the agent under test (defaults to AGENT_LLM_MODEL in .env)",
    )
    parser.add_argument(
        "--agent-strategy",
        type=str,
        choices=['llm'],
        default='llm',
    )
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--end-index", type=int, default=-1, help="Run all tasks if -1")
    parser.add_argument("--task-ids", type=int, nargs="+", help="(Optional) run only the tasks with the given IDs")
    parser.add_argument(
        "--fold-spec",
        type=str,
        default="",
        help="cross-validation grouping spec: a spec name under folds/ (e.g. story_3fold_seed10) "
             "or any spec file path. By default resolves from --env to folds/<env>_3fold_seed10.json. "
             "Giving it alone changes no behaviour -- tasks are selected by fold only when "
             "--grow-folds/--test-folds are also given. To view a spec: python -m folds show "
             "--spec <spec>; to generate a new one: python scripts/make_folds.py --env <dataset>",
    )
    parser.add_argument(
        "--grow-folds",
        type=str,
        nargs="+",
        help="growth folds (the experience library grows on these). Without --test-folds, this "
             "run executes these folds' tasks; with --test-folds it is a provenance label "
             "recording which folds the library under test grew on, and goes into the directory "
             "name and meta.json",
    )
    parser.add_argument(
        "--test-folds",
        type=str,
        nargs="+",
        help="test folds (evaluate only on these). Giving it makes this run execute these "
             "folds' tasks, and it must be paired with --evolve false -- evolving on the test "
             "fold is data leakage and run.py will refuse to start",
    )
    parser.add_argument("--log-dir", type=str, default="results")
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=1,
        help="Number of tasks to run in parallel",
    )
    parser.add_argument("--seed", type=int, default=10)
    parser.add_argument("--shuffle", type=int, default=0)
    parser.add_argument("--inject", type=_str2bool, default=True, help="whether to inject recalled intent experience into the prompt (true/false)")
    parser.add_argument("--evolve", type=_str2bool, default=True, help="whether to update the taxonomy/ledger/experiences after an episode ends (true/false)")
    parser.add_argument(
        "--agent-impl", type=str, default=AGENT_IMPL_INTENT, choices=list(AGENT_IMPLS),
        help="executor implementation: official=the official ECom-Bench create_react_agent "
             "as-is (the baseline arm must use it; this paper's intent decomposition / injection "
             "/ tool interception have no effect at all); intent=this paper's intent graph",
    )
    parser.add_argument(
        "--intent-dir", type=str, default="",
        help="intent library directory, for round-by-round iteration and snapshots. Defaults to "
             "intents-<env> -- experience libraries must be kept separate per dataset: process "
             "experience grown on story (whose tools, entities and policies are all home-appliance "
             "categories) is meaningless when routed into xcat's apparel/food dialogues, and "
             "sharing one directory would only let the two pollute each other.",
    )
    parser.add_argument(
        "--snapshot-dir",
        type=str,
        default="",
        help="copy the whole intent library to this directory after the run; the default empty "
             "string means no snapshot. The naming (e.g. intents-<arm>-r<n>/) is up to the caller",
    )
    parser.add_argument(
        "--snapshot-overwrite",
        type=_str2bool,
        default=False,
        help="whether to overwrite --snapshot-dir when it already exists. Default false: that "
             "directory is usually the read-only baseline other experiment arms compare against, "
             "and it cannot be restored once overwritten (true/false)",
    )
    parser.add_argument("--verbose", type=_str2bool, default=True, help="Enable verbose logging (true/false)")
    parser.add_argument("--max-time",type=int, default=6000, help="max time of every task")
    args = parser.parse_args()
    os.environ["ECOM_DEBUG_LLM_IO"] = "1" if args.verbose else "0"
    console.print(f"[green]{args}[/green]")  # Info color
    return RunConfig(
        # fall back to the .env default model, so the result directory name records the model id actually run
        user_model=resolve_model_name("user", args.user_model),
        agent_model=resolve_model_name("agent", args.agent_model),
        inject=args.inject,
        evolve=args.evolve,
        # without --intent-dir, take the default directory per dataset; see that argument's help for why
        intent_dir=args.intent_dir or f"intents-{args.env}",
        snapshot_dir=args.snapshot_dir,
        snapshot_overwrite=args.snapshot_overwrite,
        user_strategy=args.user_strategy,
        agent_strategy=args.agent_strategy,
        agent_impl=args.agent_impl,
        num_trials=args.num_trials,
        env=args.env,
        start_index=args.start_index,
        end_index=args.end_index,
        task_ids=args.task_ids,
        # on an empty string, resolve the default spec from --env, so meta.json records a concrete path rather than an empty string
        fold_spec=args.fold_spec or default_spec_path(args.env),
        grow_folds=args.grow_folds,
        test_folds=args.test_folds,
        log_dir=args.log_dir,
        max_concurrency=args.max_concurrency,
        seed=args.seed,
        shuffle=args.shuffle,
        verbose=args.verbose,
        max_time=args.max_time,
        # Add any other arguments you want to pass to RunConfig
    )


async def main():
    config = parse_args()
    await run(config)

def signal_handler(sig, frame):
    console.print("[yellow]Program is exiting, cleaning up resources...[/yellow]")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("[yellow]Program interrupted by the user[/yellow]")
    except Exception as e:
        console.print(f"[red]Program execution error: {e}[/red]")
    finally:
        # ignore event-loop errors on exit
        import warnings
        warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*Event loop is closed.*")
