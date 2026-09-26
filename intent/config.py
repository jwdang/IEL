"""All tunable parameters and the path layout of the intent system.

All thresholds are centralized here, making them easy to adjust together during experiments.
No list of e-commerce object/action candidates may appear here -- that would be a domain prior,
which this approach explicitly excludes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Adjudication: the number of neighbours to run pairwise discrimination against the candidate
NEIGHBOR_TOP_K = 5
# Adjudication: the minimum number of instances a ledger entry needs to enter adjudication
MIN_INSTANCES_FOR_ADJUDICATION = 2
# Adjudication: the minimum number of successful instances a ledger entry needs to enter adjudication
MIN_SUCCESS_FOR_ADJUDICATION = 1

# Merge scan: how many episodes trigger one
MERGE_SCAN_EVERY_N_EPISODES = 10
# Merge scan: intent pairs whose discrimination accuracy is below this are force-merged
DISCRIMINATION_ACCURACY_THRESHOLD = 0.8

# Terminality tightening: for an intent to be labelled requires_terminal_action=true, at least
# this many unambiguously attributed instances carrying a successful terminal call must
# independently support it. A threshold of 1 amounts to "rewrite the taxonomy after seeing it
# once", whereas the typical shape of a misattribution is exactly "one out of a large N"
# (measured: of product.query's 16 instances only 1 carried a successful terminal call). The
# value comes from experience, not from a tunable hyperparameter.
MIN_TERMINAL_SUPPORT = 2


@dataclass(frozen=True)
class IntentPaths:
    """The directory layout of the intent library."""

    root: Path
    taxonomy: Path
    ledger: Path
    instances: Path
    experiences: Path
    evolution_log: Path

    def ensure(self) -> None:
        """Create directories that do not yet exist."""
        self.root.mkdir(parents=True, exist_ok=True)
        self.instances.mkdir(parents=True, exist_ok=True)
        self.experiences.mkdir(parents=True, exist_ok=True)


def intent_paths(root: Path | str) -> IntentPaths:
    root_path = Path(root)
    return IntentPaths(
        root=root_path,
        taxonomy=root_path / "taxonomy.yaml",
        ledger=root_path / "ledger.json",
        instances=root_path / "instances",
        experiences=root_path / "experiences",
        evolution_log=root_path / "evolution_log.jsonl",
    )
