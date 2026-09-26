"""Dataset binding: a benchmark environment is defined by three things -- a task set,
a system prompt and offline data.

Why this type is factored out separately
----------------------------------------
This repo runs two datasets: ECom-Bench (`story`, 53 tasks, home appliances) and
ECom-Bench-XCAT (`xcat`, 60 tasks, apparel + food). Their **interaction protocol, tool
interface and evaluation criteria are identical**; only the task set, system prompt and
data differ. Hence a single environment implementation (ToolUseEnv in envs/env.py)
suffices, and a dataset only supplies these three things -- if each dataset kept its own
copy of env.py, every change on the method side would have to be applied twice, and the
copy that was missed would not raise an error; it would just quietly produce results
that disagree with the paper.

`data_dir` is the initial store of the offline tool service (`products.json` /
`orders.json` etc.). Each episode copies it into a private cache directory, and the GT
check compares the "copy after the agent has modified it" against the "original after
the GT actions have been applied".
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from utils import Task


@dataclass(frozen=True)
class Dataset:
    """A runnable dataset."""

    # Matches the environment directory name (envs/<name>/); also the --env value and
    # the env field in a fold spec
    name: str
    tasks: List[Task]
    # The system prompt shown to the user simulator (the contents of wiki.md)
    user_wiki: str
    # Initial database directory of the offline tool service
    data_dir: Path

    @property
    def num_tasks(self) -> int:
        return len(self.tasks)
