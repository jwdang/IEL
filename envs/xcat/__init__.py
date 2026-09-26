"""ECom-Bench-XCAT dataset: 60 tasks (30 apparel + 30 food), the paper's cross-category evaluation set.

The task set, system prompt and offline database all belong to the cross-category extension itself;
the interaction protocol and tool interfaces follow ECom-Bench, so the environment implementation
reuses ToolUseEnv in envs/env.py and only the data binding is done here.

Note: `metadata.outputs` of the XCAT tasks is all empty, i.e. the output dimension has no checkpoint
(`all([]) == True` holds trivially); this is a property of the dataset itself, not an omission here.
When reporting XCAT results in the paper, just state it under the same criterion.
"""

from __future__ import annotations

from pathlib import Path

from envs.dataset import Dataset

from .tasks import ALL_TASKS
from .wiki import WIKI

DATASET = Dataset(
    name="xcat",
    tasks=list(ALL_TASKS),
    user_wiki=WIKI,
    data_dir=Path(__file__).resolve().parent / "data",
)
