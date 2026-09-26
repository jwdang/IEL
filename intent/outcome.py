"""Instance-level success/failure judging.

Judging uses no reward (ground truth), only signals observable within the trajectory.
Terminal calls are judged by the (tool, action) pair -- the same tool carries both query and
state-change semantics, and judging by tool name would misjudge
`manage_order_tool(action=query)` as terminal.
"""

from __future__ import annotations

from dataclasses import dataclass

# A value of None means every call to that tool is terminal (no action argument)
# A value of a set means only the actions in the set are terminal
TERMINAL_ACTIONS: dict[str, set[str] | None] = {
    "manage_order_tool": {'cancel', 'modify', 'add'},
    "manage_exchange_tool": {'exchange'},
    "manage_ecard_tool": {'use_balance', 'refund'},
    "manage_return_tool": None,
    "manage_urgent_tool": None,
    "manage_invoice_tool": None,
    "schedule_service_tool": None,
    "register_cashback_by_review_tool": {'cashback'},
}

# The set of success status values.
# envs/env.py returns "success"/"failure" while this module and its tests use "ok";
# accepting both spellings avoids scattering status translation logic across modules.
SUCCESS_STATUSES = frozenset({"ok", "success"})

SUCCESS = "success"
FAILURE = "failure"
UNKNOWN = "unknown"
ESCALATED = "escalated"

# Escalation-class tools: calling them means the agent escalated the user to a human line
# rather than resolving the request itself. Deliberately not put into TERMINAL_ACTIONS --
# doing so would treat an escalation as a business terminal state, so that a successful call
# would fall into the success branch, contrary to the user's ruling (an escalation does not
# count as success).
ESCALATION_TOOLS: frozenset[str] = frozenset({"transfer_to_specialist_tool"})

@dataclass
class ToolCall:
    """One tool call within an instance."""

    name: str
    action: str | None
    status: str

    @property
    def ok(self) -> bool:
        return self.status in SUCCESS_STATUSES


def is_terminal_call(name: str, action: str | None) -> bool:
    """Decide whether a call is a state-change (terminal) call."""
    if name not in TERMINAL_ACTIONS:
        return False
    allowed = TERMINAL_ACTIONS[name]
    if allowed is None:
        return True
    return action in allowed


def has_terminal_attempt(tools: list[ToolCall]) -> bool:
    """Whether a terminal call attempt occurred within the instance (successful or not)."""
    return any(is_terminal_call(call.name, call.action) for call in tools)


def has_escalation_call(tools: list[ToolCall]) -> bool:
    """Whether an escalation call occurred within the instance."""
    return any(call.name in ESCALATION_TOOLS for call in tools)


def classify_outcome(
    tools: list[ToolCall],
    *,
    negative_signal: bool,
    repeated_query: bool,
    ambiguous_attribution: bool = False,
    requires_terminal_action: bool | None = None,
) -> tuple[str, str]:
    """Judge an instance's success or failure.

    negative_signal / repeated_query are supplied by verifier; this function only composes
    the rules, so it can be unit-tested without an LLM.

    requires_terminal_action comes from the taxonomy label: True means the intent must
    produce one state change to be complete, in which case having no terminal call is always
    failure and no longer falls into the lenient query-class branch -- that branch cannot
    distinguish "naturally has no terminal tool" from "has one but it was skipped", which is
    exactly why hallucinated execution was judged success. None (unlabelled) is routed as
    False, but is marked as such in the reason.

    negative_signal / repeated_query must take part in judging unconditionally: without them
    the lenient query-class branch collapses to "any successful call means success", a much
    looser criterion than this method claims.

    When ambiguous_attribution is true, any conclusion that would be success is downgraded to
    unknown (see the excess-turn rule in instances._assign_positional): ambiguity must not
    manufacture success evidence.
    """
    verdict, reason = _classify(
        tools,
        negative_signal=negative_signal,
        repeated_query=repeated_query,
        requires_terminal_action=requires_terminal_action,
    )

    if ambiguous_attribution and verdict == SUCCESS:
        return UNKNOWN, f"tool-call attribution within the turn is ambiguous; not judged a success (original verdict: {reason})"
    return verdict, reason


def _classify(
    tools: list[ToolCall],
    *,
    negative_signal: bool,
    repeated_query: bool,
    requires_terminal_action: bool | None = None,
) -> tuple[str, str]:
    if not tools:
        return UNKNOWN, "no tool calls in this instance; not enough signal to judge"

    own_terminal_success = [
        call for call in tools if is_terminal_call(call.name, call.action) and call.ok
    ]

    # Ordering rule: first see whether the request was already completed by its own terminal
    # call; if not, the mere presence of an escalation call means escalated, without falling
    # into the lenient query-class branch below -- that branch only looks at any(call.ok), and
    # an escalation call itself returns a success status, so it would be misjudged as success
    # (the user's ruling: an escalation does not count as success).
    if not own_terminal_success and has_escalation_call(tools):
        return ESCALATED, "no successful terminal call of its own, but a transfer-to-human call was detected"

    if has_terminal_attempt(tools):
        if not own_terminal_success:
            return FAILURE, "a terminal call was attempted, but none returned successfully"
        if negative_signal:
            return FAILURE, "the terminal call succeeded, but a negative signal was found in the span"
        names = ", ".join(sorted({call.name for call in own_terminal_success}))
        return SUCCESS, f"successful terminal call {names}; no negative signal in the span"

    # The taxonomy labels this intent as one that must change state, yet there is not even a
    # single terminal call attempt: this is not a query-class intent and must not take the
    # lenient branch below.
    if requires_terminal_action is True:
        return FAILURE, "this intent is annotated as requiring a terminal action, but the instance contains no terminal call"

    suffix = "" if requires_terminal_action is False else " (this intent's terminality is unannotated)"

    if not any(call.ok for call in tools):
        return FAILURE, f"none of the query-class instance's tool calls returned successfully{suffix}"
    if repeated_query:
        return FAILURE, f"the query succeeded, but the user asked the same question again in a later turn{suffix}"
    if negative_signal:
        return FAILURE, f"the query succeeded, but a negative signal was found in the span{suffix}"
    return SUCCESS, f"the query tool returned successfully and the user did not repeat the question{suffix}"
