"""Decomposition quality evaluation.

This is the only place in the whole codebase where the ground-truth intents (the tagged intent
blocks in the task instruction; see _INTENT_BLOCK below) are allowed to appear. It is for offline measurement only and
must never enter runtime input or distillation supervision.

To avoid tuning on the test set: the dev split is used to develop and debug the decomposer and
is frozen once tuning is done; the remaining tasks are run only once, for the final report.
"""

from __future__ import annotations

import json
import re
from typing import Any

from llm_retry import invoke_with_retry
TOTAL_TASKS = 53
DEV_SPLIT_TASK_IDS = [task_id for task_id in range(TOTAL_TASKS) if task_id % 5 == 0]
HELDOUT_TASK_IDS = [task_id for task_id in range(TOTAL_TASKS) if task_id % 5 != 0]

# The GT-intent markers are written two ways across the two datasets: `<intent_1>` and
# `<Intent 1>` (the task-text translation was done per dataset, and the two passes chose
# different conventions). Match both; the closing marker may be `<\intent_1>` or
# `</Intent 1>`.
_INTENT_BLOCK = re.compile(
    r"<\\?(?:intent|Intent)\s*[ _]?\s*(\d+)[^>]*>(.*?)<[\\/]?\s*(?:intent|Intent)",
    re.S,
)


def extract_gt_intents(instruction: str) -> list[str]:
    """Extract the GT intent texts from the task instruction."""
    return [body.strip() for _, body in _INTENT_BLOCK.findall(instruction) if body.strip()]


def align_intents(
    gt_intents: list[str], predicted: list[str], llm: Any
) -> list[int | None]:
    """Align one GT index to each predicted intent; unmatched ones are recorded as None."""
    if not predicted:
        return []
    prompt = (
        "Align each predicted intent to a reference intent, one by one. Give the index of "
        "the reference intent it matches, or null when there is no match.\n"
        f"Reference intents (0-indexed): {json.dumps(gt_intents, ensure_ascii=False)}\n"
        f"Predicted intents: {json.dumps(predicted, ensure_ascii=False)}\n"
        'Output JSON only: {"alignment": [index or null, ...]}, with the length equal to '
        "the number of predicted intents."
    )
    try:
        response = invoke_with_retry(
            llm, [{"role": "user", "content": prompt}], description="intent.align_predictions"
        )
        raw = getattr(response, "content", response)
        payload = json.loads(raw if isinstance(raw, str) else str(raw))
        alignment = payload["alignment"]
    except Exception:  # noqa: BLE001
        return [None] * len(predicted)

    if not isinstance(alignment, list) or len(alignment) != len(predicted):
        return [None] * len(predicted)

    normalized: list[int | None] = []
    for item in alignment:
        if isinstance(item, int) and 0 <= item < len(gt_intents):
            normalized.append(item)
        else:
            normalized.append(None)
    return normalized


def precision_recall(alignment: list[int | None], gt_count: int) -> tuple[float, float]:
    """precision = matched predictions / total predictions; recall = covered GTs / total GTs."""
    if not alignment or gt_count <= 0:
        return 0.0, 0.0
    hits = [item for item in alignment if item is not None]
    precision = len(hits) / len(alignment)
    recall = len(set(hits)) / gt_count
    return precision, recall


def evaluate_task(instruction: str, predicted: list[str], llm: Any) -> dict[str, Any]:
    gt_intents = extract_gt_intents(instruction)
    alignment = align_intents(gt_intents, predicted, llm)
    precision, recall = precision_recall(alignment, len(gt_intents))
    return {
        "gt_count": len(gt_intents),
        "predicted_count": len(predicted),
        "alignment": alignment,
        "precision": precision,
        "recall": recall,
    }
