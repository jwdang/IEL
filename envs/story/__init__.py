"""ECom-Bench `story` dataset: 53 tasks, home-appliance category, the paper's in-domain evaluation set."""

from __future__ import annotations

from pathlib import Path

from envs.dataset import Dataset

from .tasks import ALL_TASKS
from .wiki import WIKI

DATASET = Dataset(
    name="story",
    tasks=list(ALL_TASKS),
    user_wiki=WIKI,
    data_dir=Path(__file__).resolve().parent / "data",
)
