"""Environment registry: maps a dataset name (--env) to the data binding in envs/<name>/.

There is a single environment implementation (ToolUseEnv in envs/env.py); a dataset
only supplies the task set, the system prompt and the offline data (see
envs/dataset.py). Adding a new dataset = create an envs/<name>/ directory that exports
a `DATASET`, then add one line to the registry below -- no changes to the environment
implementation and no copy of env.py.

Dataset modules are imported lazily (rather than `import`-ed at the top of the module):
the tasks.py files of the two datasets add up to 60k lines, and any single run only
uses one of them.
"""

from __future__ import annotations

import importlib
from typing import Optional

from envs.base import Env
from envs.dataset import Dataset
from envs.env import ToolUseEnv
from utils import AGENT_IMPL_INTENT

# Dataset name -> the module that provides DATASET
_DATASET_MODULES = {
    "story": "envs.story",
    "xcat": "envs.xcat",
}

# The legal values of --env. run.py's argparse choices uses this directly, so the
# list is not re-typed by hand.
ENV_NAMES = tuple(_DATASET_MODULES)


def load_dataset(env_name: str) -> Dataset:
    module_name = _DATASET_MODULES.get(env_name)
    if module_name is None:
        raise ValueError(
            f"Unknown environment: {env_name!r}. Available: {', '.join(ENV_NAMES)}"
        )
    return importlib.import_module(module_name).DATASET


def get_env(
    env_name: str,
    user_model: str,
    agent_model: str,
    inject: bool = True,
    evolve: bool = True,
    console_verbose=None,
    task_index: Optional[int] = None,
    intent_dir: str = "intents",
    run_id: str = "",
    trial_index: int = 0,
    metrics_dir: str = "",
    agent_impl: str = AGENT_IMPL_INTENT,
) -> Env:
    return ToolUseEnv(
        dataset=load_dataset(env_name),
        user_model=user_model,
        agent_model=agent_model,
        inject=inject,
        evolve=evolve,
        console_verbose=console_verbose,
        task_index=task_index,
        intent_dir=intent_dir,
        run_id=run_id,
        trial_index=trial_index,
        metrics_dir=metrics_dir,
        agent_impl=agent_impl,
    )
