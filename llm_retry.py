"""Unified retry wrapper for LLM calls.

Network traffic goes through a proxy with occasional SSL disconnects and 5xx responses: a
single failed call scrapping a whole episode is pure noise in a long-running experiment -- the
difference between two runs of the same task may be nothing more than "it did not hiccup this
time". Here we provide call-site-level retries, which stack with the existing two layers of
protection into three:

1. openai-python's `max_retries=3` (inside the client, covering only the errors it deems
   retryable);
2. this module: explicit retries at the call site, catching **any** exception and retrying
   after exponential backoff;
3. main.py's MAX_TASK_ATTEMPTS: whole-task retries, for connection-class errors.

**It wraps only pure model calls, never agent-graph calls.** `agent_model.ainvoke` inside
`AgentLangChain.call` / `AgentOfficial.call` runs the whole graph, and tools (placing orders,
refunds) execute midway. Retrying at that layer would run already-effective tool calls again,
polluting env state and reward. The real model call inside the graph is
`utils.LLM._initiate_agent`'s `model_with_tools.invoke`, and the retry goes there -- no side
effects, and a failure still propagates up to main's task-level retry.

Once retries are exhausted the exception is re-raised as-is, so the existing fallback logic at
call sites (`except Exception: return an empty result` throughout the intent system) is
completely unchanged.
"""

from __future__ import annotations

import asyncio
import sys
import time
from typing import Any, Callable

# The maximum number of attempts per call site (first try + 2 retries)
LLM_MAX_ATTEMPTS = 3

# Base of the exponential backoff: after the n-th failure wait 2^(n-1) * BASE seconds, i.e.
# 2 / 4 / 8 ...
LLM_RETRY_BASE_SECONDS = 2.0


def retry_delay(attempt: int, base_seconds: float = LLM_RETRY_BASE_SECONDS) -> float:
    """The number of seconds to wait after the attempt-th attempt (1-based) fails."""
    return base_seconds * (2 ** (attempt - 1))


def _warn(description: str, attempt: int, attempts: int, exc: BaseException, delay: float) -> None:
    """Write the retry to stderr. Not the rich console: this module is imported by modules that
    have no console."""
    print(
        f"[llm-retry] {description} attempt {attempt}/{attempts} failed"
        f" ({type(exc).__name__}: {exc}), retrying in {delay:g}s",
        file=sys.stderr,
        flush=True,
    )


def call_with_retry(
    call: Callable[[], Any],
    *,
    description: str = "llm call",
    attempts: int = LLM_MAX_ATTEMPTS,
    base_seconds: float = LLM_RETRY_BASE_SECONDS,
) -> Any:
    """Call call() synchronously, retrying with exponential backoff on failure, and raising the
    last exception once attempts are exhausted.

    Catches Exception rather than BaseException: KeyboardInterrupt and
    asyncio.CancelledError must pass through untouched, or Ctrl-C and main.py's
    asyncio.wait_for(max_time) would be swallowed here.
    """
    for attempt in range(1, attempts + 1):
        try:
            return call()
        except Exception as exc:  # noqa: BLE001 -- any model-side exception is worth one retry
            if attempt >= attempts:
                raise
            delay = retry_delay(attempt, base_seconds)
            _warn(description, attempt, attempts, exc, delay)
            time.sleep(delay)


async def acall_with_retry(
    call: Callable[[], Any],
    *,
    description: str = "llm call",
    attempts: int = LLM_MAX_ATTEMPTS,
    base_seconds: float = LLM_RETRY_BASE_SECONDS,
) -> Any:
    """The coroutine version of call(): waits with asyncio.sleep, without blocking the event
    loop."""
    for attempt in range(1, attempts + 1):
        try:
            return await call()
        except Exception as exc:  # noqa: BLE001
            if attempt >= attempts:
                raise
            delay = retry_delay(attempt, base_seconds)
            _warn(description, attempt, attempts, exc, delay)
            await asyncio.sleep(delay)


def invoke_with_retry(llm: Any, messages: Any, *, description: str = "llm.invoke") -> Any:
    """A retrying version of `llm.invoke(messages)`. Almost every call site in the intent
    system has this shape."""
    return call_with_retry(lambda: llm.invoke(messages), description=description)
