"""LLM call accounting for the intent system.

The runtime decomposition calls and the whole pipeline at episode end (verifier review,
ledger semantic merging, neighbour selection, admission adjudication, contrastive
distillation, merge scan) all call `llm.invoke()` directly, and their responses never enter
graph state, while AgentLangChain._accumulate_token_usage only walks the graph's messages --
so the intent system's entire cost is invisible in the cost accounting, and the intent arm's
expense is systematically underestimated.

Here we change neither the graph nor any call site: a transparent wrapper collects the
accounting at the call entry point, and the wrapped llm is handed to the intent system.
Execution is serial, with no locking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def extract_usage(response: Any) -> dict[str, int] | None:
    """Take the token usage from one LLM response, returning None if unavailable.

    Same standard as AgentLangChain._extract_usage: prefer usage_metadata (the unified
    LangChain field), falling back to response_metadata['token_usage'] (what an
    OpenAI-compatible response returns).
    """
    usage_metadata = getattr(response, "usage_metadata", None) or {}
    if isinstance(usage_metadata, dict) and usage_metadata:
        prompt = int(usage_metadata.get("input_tokens") or 0)
        completion = int(usage_metadata.get("output_tokens") or 0)
        total = int(usage_metadata.get("total_tokens") or (prompt + completion))
        return {
            "prompt_tokens": prompt,
            "completion_tokens": completion,
            "total_tokens": total,
        }

    response_metadata = getattr(response, "response_metadata", None) or {}
    token_usage = (
        response_metadata.get("token_usage") if isinstance(response_metadata, dict) else {}
    )
    if isinstance(token_usage, dict) and token_usage:
        prompt = int(token_usage.get("prompt_tokens") or 0)
        completion = int(token_usage.get("completion_tokens") or 0)
        total = int(token_usage.get("total_tokens") or (prompt + completion))
        return {
            "prompt_tokens": prompt,
            "completion_tokens": completion,
            "total_tokens": total,
        }
    return None


@dataclass
class UsageTracker:
    """The intent system's cumulative usage.

    uncounted_calls is recorded separately: when the model returns no usage metadata, that
    call's token count cannot be known. Recording it as 0 without saying so would quietly
    undercount the cost; an explicit count is what makes it possible to state in a report "how
    many calls were still left out".
    """

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    calls: int = 0
    uncounted_calls: int = 0

    def record(self, response: Any) -> None:
        self.calls += 1
        usage = extract_usage(response)
        if usage is None:
            self.uncounted_calls += 1
            return
        self.prompt_tokens += usage["prompt_tokens"]
        self.completion_tokens += usage["completion_tokens"]
        self.total_tokens += usage["total_tokens"]

    def totals(self) -> dict[str, int]:
        return {
            "intent_prompt_tokens": self.prompt_tokens,
            "intent_completion_tokens": self.completion_tokens,
            "intent_total_tokens": self.total_tokens,
            "intent_llm_calls": self.calls,
            "intent_uncounted_llm_calls": self.uncounted_calls,
        }


@dataclass
class CountingLLM:
    """A transparent wrapper that records each invoke's usage into the tracker.

    It wraps only invoke -- the whole intent system goes through this one entry point. All
    other attributes are forwarded to the wrapped object, so call sites cannot tell the
    difference.

    **No retries here**: retries live at the call sites (invoke_with_retry throughout
    intent/*), and adding them in both layers would stack up to 3x3=9 attempts. The accounting
    stays accurate -- a failed attempt produces no response, and record is called only once on
    a successful return.
    """

    llm: Any
    tracker: UsageTracker = field(default_factory=UsageTracker)

    def invoke(self, messages: Any) -> Any:
        response = self.llm.invoke(messages)
        self.tracker.record(response)
        return response

    def __getattr__(self, name: str) -> Any:
        # the dataclass has already put llm/tracker in the instance dict; this only catches
        # other attributes
        return getattr(self.llm, name)
