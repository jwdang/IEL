from rich.console import Console
from rich.table import Table
import json
from pydantic import BaseModel
from typing import List, Dict, Optional, Any, Annotated, Literal, TypedDict
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, create_react_agent
from abc import ABC, abstractmethod
from datetime import datetime
from itertools import count
import os
from folds import default_spec_path
from llm_config import get_llm_config
from llm_retry import call_with_retry
from intent.config import intent_paths
from intent.decomposer import decompose
from intent.store import ExperienceStore
from intent.taxonomy import Taxonomy
from intent.usage import CountingLLM, UsageTracker

_LLM_DEBUG_COUNTER = count(1)

# The two executor implementation paths.
#
# official: the official ECom-Bench create_react_agent(llm, mcp_tools) as-is, with no
#   intent nodes and no tool-repeat interception. The baseline arm must take this path --
#   none of this paper's changes may leak into the baseline, or "method vs baseline"
#   measures the method plus a pile of unrelated changes. This really happened in
#   practice: agent_wiki had three extra anti-hallucination lines and the executor had
#   been swapped for the custom graph, both of which applied to the baseline.
# intent: this paper's intent graph (decompose / inject).
#
# The two paths share only the LLM client construction (max_retries, timeout, and
# task-level retry in _initiate_llm) and the reward computation -- the former is
# harness-level infrastructure that does not change the model's reasoning quality, the
# latter is a measuring instrument that would make the two arms incomparable once forked.
AGENT_IMPL_OFFICIAL = "official"
AGENT_IMPL_INTENT = "intent"
AGENT_IMPLS = (AGENT_IMPL_OFFICIAL, AGENT_IMPL_INTENT)


class ProductInfo(BaseModel):
    product_id:str
    quantity: int
class Task(BaseModel):
    annotator:str
    user_id: str
    shop_id: str
    platform: str
    instruction: str
    metadata:Optional[Any] = None
    
class Search(BaseModel):
    name:str
    arguments: Optional[Dict[str, Any]] = None
    
class Action(BaseModel):
    name:str
    arguments: Optional[Dict[str, Any]] = None
    
class Validation(BaseModel):
    outputs: List[str] = []
    actions: List[Action] = []
    searches: List[Search] = [] 

class DetailReward(BaseModel):
    action:int
    search:int
    output:int
    time:float
    
class EnvRunResult(BaseModel):
    task_id: int
    reward: float
    traj: List[Dict[str, Any]]
    trial: int
    detail_reward: DetailReward
    total_turns: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    # The intent system's own LLM cost (one decomposition per turn plus the whole pipeline
    # at episode end). Kept separate from the main-dialogue cost above: the main-dialogue
    # accounting is unchanged so it can be compared with historical results, and for a cost
    # comparison the two must be added to get the intent arm's true expense.
    # intent_uncounted_llm_calls records the number of calls whose model returned no usage
    # metadata and therefore cannot be counted into the token totals.
    intent_prompt_tokens: int = 0
    intent_completion_tokens: int = 0
    intent_total_tokens: int = 0
    intent_llm_calls: int = 0
    intent_uncounted_llm_calls: int = 0
    # Per-turn intent routing results [{turn, matched:[{id}], downgraded:[...]}].
    # downgraded now has only one source: the LLM put an id in matched that the taxonomy
    # does not have (a format error, or it tried to propose a new intent in the wrong
    # field). Uncertain matches do not appear here -- under the current decompose rules,
    # when the LLM is unsure it emits nothing rather than matching first and being
    # downgraded later.
    intent_decompositions: Optional[List[Dict[str, Any]]] = None
    # Tool-repeat interception counts. They exist only in the intent executor (always 0
    # under official) and are an engineering guardrail rather than a contribution of this
    # paper; if the method arm wins, they let us factor out how much of it the guardrail
    # earned.
    tool_repeat_warnings: int = 0
    tool_repeat_blocks: int = 0
    # For checking: the list of tools the Agent actually called versus the search/action ground truth the task requires
    agent_executed_tools: Optional[List[Dict[str, Any]]] = None
    ground_truth_searches: Optional[List[Dict[str, Any]]] = None
    ground_truth_actions: Optional[List[Dict[str, Any]]] = None
    ground_truth_outputs: Optional[List[str]] = None
    # How the session ended: stop_signal / max_turn / timeout / error.
    # "Ran out of turns without finishing" and "finished but got it wrong" are two
    # different kinds of failure and must be separated when attributing results.
    termination: Optional[str] = None
    # Needed for the trajectory to be self-contained: no need to look back at tasks.py to
    # know what this trajectory is doing
    task_instruction: Optional[str] = None
    # Per-turn cost, for equal-budget comparison experiments
    turn_latencies: Optional[List[float]] = None
    turn_token_usage: Optional[List[Dict[str, Any]]] = None

class Episode(BaseModel):
    time: datetime  # Episode(time="2025-01-03T15:33", instruction="Instruction text")
    instruction: str
    metadata: Optional[Any] = None
class RunConfig(BaseModel):
    agent_model: str
    user_model: str
    inject: bool = True
    evolve: bool = True
    # Executor implementation. The baseline arm must pass official explicitly; none of this
    # paper's changes may leak into the baseline. The default intent keeps the same
    # convention as the inject/evolve defaults (omitting everything means the full method);
    # main.py's _assert_baseline_is_official blocks the pseudo-baseline of "both switches
    # off but still using the intent executor", rather than relying on people remembering to
    # pass the argument.
    agent_impl: Literal[AGENT_IMPLS] = AGENT_IMPL_INTENT  # type: ignore[valid-type]
    intent_dir: str = "intents"
    # At the end of the run, copy the whole intent library to this directory so each round
    # can be archived; an empty string (the default) means no snapshot. The naming (e.g.
    # intents-<arm>-r<n>/) is up to the caller; this field only passes the path through.
    snapshot_dir: str = ""
    # Whether to allow overwriting when the snapshot destination already exists. Default
    # false: that directory is very likely the read-only baseline every experiment arm
    # compares against (all six arms in run.sh point at intents-warm-r1), and rerunning the
    # warmup command once would replace it irreversibly. Discarding it must be said out loud.
    snapshot_overwrite: bool = False
    num_trials: int
    env: str
    user_strategy: str
    agent_strategy: str
    start_index: int = 0
    end_index: int = -1
    task_ids: Optional[List[int]] = None
    # Task grouping for cross-validation. fold_spec points at a spec file under folds/ (or
    # any path), but it **changes no behaviour by itself**: tasks are selected by fold only
    # when grow_folds/test_folds are given explicitly. An empty string means "use the default
    # spec for this dataset" (folds/<env>_3fold_seed10.json), resolved by main.py from env --
    # the two datasets have different task counts, so the default spec cannot be hardcoded to
    # one. All three fields go into meta.json, so which fold these results measured and which
    # folds the library grew on can be reproduced exactly afterwards. See the module docstring
    # of folds/__init__.py.
    fold_spec: str = ""
    grow_folds: Optional[List[str]] = None
    test_folds: Optional[List[str]] = None
    log_dir: str = "results"
    max_concurrency: int = 1
    seed: int = 10
    shuffle: int = 0
    verbose: bool = False
    max_time: int = 300


class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    conversation: list[Dict[str, Any]]
    tool_calls: list[Dict[str, Any]]
    available_tools: list[Dict[str, Any]]
    active_intent_context: str
    active_intent_ids: list[str]


def _coerce_message_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(str(item.get("text", item)))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(content)


def _last_ai_message(messages: list[Any]) -> AIMessage | None:
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            return message
    return None


# Warning prefix for tool-repeat interception, used to detect "has this turn already been
# warned". It must share its source with the interception logic: agent_node recognizes
# whether the warning was already injected by this prefix.
_TOOL_REPEAT_WARNING_PREFIX = "[system notice] Repeated tool call blocked: "

# The user-facing reply that ends the turn directly after interception/blocking (it must
# be non-empty, or env triggers an empty-reply retry).
_TOOL_REPEAT_USER_REPLY = (
    "Sorry, I can't complete your request right now: the system detected that the "
    "same operation failed repeatedly, which usually means some required information "
    "is missing. Could you provide the relevant product or order details, or I can "
    "transfer you to a human agent."
)


def _tool_call_fingerprint(tool_call: Any) -> str:
    """Repeat fingerprint of a tool call: tool name + arguments with null values removed
    (serialized with sorted keys).

    An explicit null in the arguments (a common model output, e.g. {"shop_id": null}) is
    equivalent to the argument being absent, so it is removed during normalization, lest
    the same failing call be missed because null and omitted are spelled differently.
    """
    fn = tool_call.get("function", {}) if isinstance(tool_call, dict) else {}
    name = str(fn.get("name", ""))
    try:
        args = json.loads(fn.get("arguments", "{}") or "{}")
    except Exception:  # noqa: BLE001
        args = {}
    if isinstance(args, dict):
        args = {k: v for k, v in args.items() if v is not None}
    return f"{name}({json.dumps(args, sort_keys=True, ensure_ascii=False)})"


def _repeated_tool_fingerprint(messages: list[Any], threshold: int = 3) -> str | None:
    """Whether the most recent consecutive tool calls contain >= threshold identical
    fingerprints.

    Scans from the tail of the messages backwards: collects AIMessage tool_calls
    fingerprints (skipping non-AI messages such as ToolMessage) until a different
    fingerprint appears. Returns the repeated fingerprint (for the warning text to cite),
    otherwise None.

    Rationale: tools are deterministic -- identical arguments necessarily yield identical
    results, so a run of identical calls means the model is repeating a known-failed
    attempt (observed in practice: the model called the same tool 20+ times with the same
    null arguments until the recursion_limit cut it off).

    The threshold is 3 rather than 2: a hit costs that fingerprint being blocked, and a
    model sending the same query twice in one turn (checking once, then verifying before
    answering) is common and harmless. The pathological form is 20+ times, and a threshold
    of 3 still stops it early without locking out a tool over one harmless repeat.
    """
    seq: list[str] = []
    for msg in reversed(messages):
        if not isinstance(msg, AIMessage):
            continue
        calls = msg.additional_kwargs.get("tool_calls") or []
        for tc in reversed(calls):
            fp = _tool_call_fingerprint(tc)
            if seq and fp != seq[-1]:
                return seq[-1] if len(seq) >= threshold else None
            seq.append(fp)
    return seq[-1] if seq and len(seq) >= threshold else None


def _filter_blocked_tool_calls(response: AIMessage, blocked: set[str]) -> AIMessage:
    """Remove blocked tool calls from the model output; when all are blocked, replace it
    with a user-facing reply.

    The fingerprints in blocked come from same-turn repeat detection or cross-turn
    blocking: calls with the same (tool, arguments) have already failed repeatedly, so
    executing them just burns tokens again (observed: 20+ consecutive ineffective calls).
    If unblocked calls remain after removal they execute as usual; if all are blocked, no
    tool is called this turn and the turn ends with a text reply (non-empty, to avoid
    triggering env's empty-reply retry).
    """
    calls = response.additional_kwargs.get("tool_calls") or []
    if not calls:
        return response
    kept = [tc for tc in calls if _tool_call_fingerprint(tc) not in blocked]
    if len(kept) == len(calls):
        return response
    if kept:
        return AIMessage(
            content=response.content,
            additional_kwargs={**response.additional_kwargs, "tool_calls": kept},
        )
    return AIMessage(content=_TOOL_REPEAT_USER_REPLY)


def is_retryable_connection_error(exc: BaseException) -> bool:
    """Decide whether an exception is a connection-class error worth retrying the whole task.

    It matches only connection/timeout/rate-limit signals, without broad matching (a bare
    "500" would collide with unrelated digits in an error message). openai's
    APIConnectionError message body is literally "Connection error." -- one of the 5 error
    runs in warmup was exactly that.

    It lives in utils rather than main because env.a_run also needs it to decide whether to
    re-raise connection-class errors (a_run's except swallows every exception into an error
    result, and without letting it through here main's task-level retry would never fire).
    """
    name = type(exc).__name__.lower()
    text = f"{name}: {exc}".lower()
    return any(
        token in text
        for token in (
            "connectionerror",
            "connecterror",
            "connection error",
            "apiconnection",
            "timeout",
            "ratelimit",
            "error code: 500",
            "error code: 502",
            "error code: 503",
            "error code: 504",
        )
    )


def _message_role(message: Any) -> str:
    if isinstance(message, HumanMessage):
        return "human"
    if isinstance(message, AIMessage):
        return "ai"
    if isinstance(message, ToolMessage):
        return "tool"
    if isinstance(message, dict):
        role = str(message.get("role", "")).lower()
        if role == "user":
            return "human"
        if role == "assistant":
            return "ai"
        return role
    message_type = str(getattr(message, "type", "")).lower()
    if message_type in {"human", "ai", "tool", "system"}:
        return message_type
    return ""


def _message_content(message: Any) -> str:
    if isinstance(message, dict):
        return _coerce_message_content(message.get("content", ""))
    return _coerce_message_content(getattr(message, "content", ""))


def _message_tool_calls(message: Any) -> Any:
    if isinstance(message, AIMessage):
        if message.tool_calls:
            return message.tool_calls
        additional_kwargs = getattr(message, "additional_kwargs", {})
        if isinstance(additional_kwargs, dict):
            return additional_kwargs.get("tool_calls")
        return None
    if isinstance(message, dict):
        tool_calls = message.get("tool_calls")
        if tool_calls:
            return tool_calls
        additional_kwargs = message.get("additional_kwargs", {})
        if isinstance(additional_kwargs, dict):
            return additional_kwargs.get("tool_calls")
    return None


def _format_messages_for_debug(messages: list[Any]) -> str:
    lines: list[str] = []
    for idx, message in enumerate(messages, start=1):
        role = _message_role(message) or "unknown"
        content = _message_content(message)
        lines.append(f"{idx}. [{role}] {content}")
        tool_calls = _message_tool_calls(message)
        if tool_calls:
            lines.append(f"   tool_calls: {json.dumps(tool_calls, ensure_ascii=False)}")
    return "\n".join(lines)


def _normalize_messages_for_debug(messages: Any) -> list[Any]:
    if isinstance(messages, list):
        return messages
    if isinstance(messages, tuple):
        return list(messages)
    return [messages]


def _format_response_for_debug(response: Any) -> str:
    role = _message_role(response) or "assistant"
    content = _message_content(response)
    lines = [f"[{role}] {content}"]
    tool_calls = _message_tool_calls(response)
    if tool_calls:
        lines.append(f"tool_calls: {json.dumps(tool_calls, ensure_ascii=False)}")
    return "\n".join(lines)


def _print_llm_debug_call(
    stage: str,
    model_name: str,
    input_messages: Any,
    output_message: Any,
    enabled: bool,
) -> None:
    if not enabled:
        return
    normalized_input = _normalize_messages_for_debug(input_messages)
    call_id = next(_LLM_DEBUG_COUNTER)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "=" * 100)
    print(f"[LLM DEBUG #{call_id}] Time: {ts} | Stage: {stage} | Model: {model_name}")
    print("-" * 100)
    # print("[INPUT]")
    # print(_format_messages_for_debug(normalized_input))
    print("[INPUT] (omitted)")
    print("-" * 100)
    print("[OUTPUT]")
    print(_format_response_for_debug(output_message))
    print("=" * 100)


def _latest_human_message_content(messages: list[Any]) -> str:
    for message in reversed(messages):
        if _message_role(message) == "human":
            return _message_content(message)
    return ""


def _format_recent_context(messages: list[Any], max_messages: int = 3) -> str:
    non_system = [msg for msg in messages if _message_role(msg) in {"human", "ai", "tool"}]
    if not non_system:
        return "(no recent context)"
    recent = non_system[-max_messages:]
    lines: list[str] = []
    for idx, msg in enumerate(recent, start=1):
        lines.append(f"{idx}. [{_message_role(msg)}] {_message_content(msg)}")
    return "\n".join(lines)


def build_intent_context(intent_ids: list[str], experiences: "ExperienceStore") -> str:
    """Assemble the injected text from the experiences of the matched intents.

    intent_ids are already the intents decompose() judged to be certain matches (see rules
    6/7 of DECOMPOSE_RULES), with no second confidence filter, so we look up each
    experience in turn and inject as many as there are, with no count truncation.
    """
    chunks: list[str] = []
    for intent_id in intent_ids:
        body = experiences.read(intent_id)
        if not body:
            continue
        chunks.append(f"## Intent experience: {intent_id}\n{body.strip()}")
    return "\n\n".join(chunks)


# The injection preamble = the principle of conditional use + grounding constraints.
#
# The last three items originally lived in wikis/agent_wiki.md, which is **the official
# prompt** that the baseline also receives -- so the "method vs baseline" difference already
# had one of the method's own remedies fed to the control group. They now live in the
# injection preamble: they switch on and off with --inject, and belong to the same "choose
# well" step as experience injection, so the three lines need no separate ablation -- one
# switch, one ablation.
#
# Semantically they were already an extension of the same thing: the first two lines say
# "experience is only a reference; when it conflicts with on-the-spot evidence, the
# evidence wins", and the last three say "product policy comes only from what the tools
# return; if it cannot be found, say it cannot be found". Both are the same principle --
# **do not fill gaps in the on-the-spot evidence with what is in your head**.
INJECTION_PREAMBLE = (
    "The following reference experience was returned by the intent router. Use it "
    "only when it fits the current request and the current tool evidence; otherwise "
    "ignore it.\n"
    "- For policies or rules about a specific product, rely on the actual information "
    "returned by the tools for that product.\n"
    "- If the tool cannot find the product, or its result clearly conflicts with the "
    "user's product description, do not fill in product-specific policy using general "
    "knowledge, industry conventions, or the stored experience.\n"
    "- In that situation, you must clearly tell the user that the policy information "
    "for this product cannot be retrieved right now, and that they need to provide the "
    "correct order number or product id, or wait for further verification before you "
    "answer."
)


def inject_intent_context(messages: list[Any], intent_context: str) -> list[Any]:
    """Insert the experience as reference material before the last user message.

    Deliberately not at the system level, so it does not override on-the-spot evidence in
    the dialogue.

    Injected only when the last message is a user message -- that is, on the first entry
    into agent_node each turn. When agent_node is re-entered inside the tool loop the last
    message is a tool result, and appending the experience there would make the model treat
    it as the latest user input (HumanMessage role) and would repeat the same experience on
    every tool iteration. The experience is already visible on the first call of the turn,
    so there is no need to inject it again inside the loop.
    """
    if not intent_context.strip():
        return messages
    if not messages or _message_role(messages[-1]) != "human":
        return messages

    injected = list(messages)
    reference = HumanMessage(content=f"{INJECTION_PREAMBLE}\n\n{intent_context.strip()}")
    injected.insert(len(injected) - 1, reference)
    return injected


class RunLogger:
    def __init__(self, verbose=False):
        self.console = Console()
        self.verbose = verbose  # logging is off by default
    def reset(self, verbose):
        self.verbose = verbose
    def print(self, *args):
        self.console.print(*args)
    def log(self, *args):
        if self.verbose:
            self.console.log(*args)
        else:
            # if logging is not enabled, do nothing
            pass

    def log_table(self, data_list, title="Table", name_column="Name", args_column="Arguments"):
        """Render data in table form

        Args:
            data_list: a list of dicts, each of which should have 'name' and 'arguments' keys
            title: the table title
            name_column: the header of the name column
            args_column: the header of the arguments column
        """
        if self.verbose:
            print("\n\n")
            table = Table(
                title=title, 
                show_header=True, 
                header_style="bold magenta",
                show_lines=True,  # add this parameter to show row separator lines
            )
            table.add_column(name_column, style="cyan", justify="left")
            table.add_column(args_column, style="yellow", justify="left")
            
            for item in data_list:
                name = item.get('name', 'N/A')
                arguments = item.get('arguments', {})
                # format arguments as a JSON string, keeping it short so the table stays neat
                args_str = json.dumps(arguments, ensure_ascii=False, indent=2)
                table.add_row(name, args_str)

            self.console.print(table)
        else:
            # if logging is not enabled, do nothing
            pass

console_verbose = RunLogger()

class TokenUsageMixin:
    """Per-turn token accounting.

    Pure measurement: it only reads AIMessage usage metadata and never enters the
    reasoning path, so sharing it between the two executor implementations does not make
    the official arm deviate from official behaviour. The official code lacks this because
    it never reports cost at all, but the equal-budget comparison experiments require it.
    """

    def _init_token_usage(self) -> None:
        self.token_usage_totals = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        self.token_usage_per_turn = []
        self._counted_ai_message_keys = set()
        self._call_counter = 0

    def _accumulate_token_usage(self, messages, call_index: int) -> None:
        turn_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        for idx, msg in enumerate(messages):
            if not isinstance(msg, AIMessage):
                continue
            usage = self._extract_usage(msg)
            if usage is None:
                continue
            key = self._ai_message_dedup_key(msg, idx=idx)
            if key in self._counted_ai_message_keys:
                continue
            self._counted_ai_message_keys.add(key)
            for field in turn_usage:
                turn_usage[field] += usage[field]
                self.token_usage_totals[field] += usage[field]
        self.token_usage_per_turn.append({"turn": call_index, **turn_usage})

    def _ai_message_dedup_key(self, msg: AIMessage, idx: int) -> str:
        msg_id = getattr(msg, "id", None)
        if msg_id:
            return f"id:{msg_id}"
        content = getattr(msg, "content", "")
        usage = getattr(msg, "usage_metadata", None) or {}
        payload = {"content": content, "usage": usage, "idx": idx}
        payload_str = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
        import hashlib as _hashlib

        digest = _hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        return f"hash:{digest}"

    def _extract_usage(self, msg: AIMessage):
        usage_metadata = getattr(msg, "usage_metadata", None) or {}
        if isinstance(usage_metadata, dict) and usage_metadata:
            prompt = int(usage_metadata.get("input_tokens") or 0)
            completion = int(usage_metadata.get("output_tokens") or 0)
            total = int(usage_metadata.get("total_tokens") or (prompt + completion))
            return {
                "prompt_tokens": prompt,
                "completion_tokens": completion,
                "total_tokens": total,
            }

        response_metadata = getattr(msg, "response_metadata", None) or {}
        token_usage = response_metadata.get("token_usage") if isinstance(response_metadata, dict) else {}
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


class LLM(ABC):
    def __init__(self, model_name:str, verbose:bool=False, mcp_tools=[], temperature=0.3, inject: bool = True, role: str = "agent", intent_dir: str = "intents", evolve: bool = True, agent_impl: str = AGENT_IMPL_INTENT):
        self.model_name = model_name
        # role decides which set of .env credentials to read: "agent" or "user", see llm_config.py
        self.role = role
        self.verbose = verbose
        self.mcp_tools = mcp_tools
        self.inject = inject
        self.evolve = evolve
        # Executor implementation: official = the official create_react_agent as-is,
        # intent = this paper's intent graph. See the comment on AGENT_IMPL_OFFICIAL.
        #
        # Any non-agent role is forced to official. The user simulator is **part of the
        # benchmark environment**, not this paper's method: it likewise calls
        # super()._initiate_agent(), and if it followed the default to intent, the customer
        # side would run on our custom graph (bind_tools([]) + a custom loop) whereas the
        # official one is create_react_agent(llm, []). That would make **both arms'**
        # dialogues deviate from official at once, with no benefit -- what the method needs
        # to validate is the service-agent side, not the customer side.
        self.agent_impl = AGENT_IMPL_OFFICIAL if role != "agent" else agent_impl
        self.llm = None  # initialize the llm attribute
        self.messages = []
        self.temperature = temperature
        self._initiate_llm()  # create the LLM instance directly at initialization
        # pending_candidates exists for all roles (an empty list is fine), so that
        # consume_pending_candidates() can also be called safely by non-agent roles and
        # return [].
        self.pending_candidates: list[Dict[str, Any]] = []
        # The intent ids routed out by intent_node each turn (in the LLM's raw output order,
        # all certain matches). env records them in traj's skills field, so that "which
        # experiences were injected this turn" can be checked afterwards -- previously env
        # hardcoded an empty list and the injection chain was completely unauditable.
        self.last_injected_intents: list[str] = []
        self.intent_dir = intent_dir
        # The intent system's LLM cost is accounted separately: these calls never enter
        # graph state and _accumulate_token_usage only walks the graph's messages, so unless
        # they are captured this way they are hidden cost. The pipeline at episode end
        # shares this tracker too (see env._run_intent_pipeline).
        self.intent_usage = UsageTracker()
        self.intent_llm = CountingLLM(self.llm, self.intent_usage)
        self.intent_enabled = self._compute_intent_enabled()
        self._intent_paths = intent_paths(intent_dir) if self.intent_enabled else None
        self._experiences: Optional[ExperienceStore] = None
        # Within-turn tool blocklist: fingerprints intercepted this turn are removed and not
        # executed if the model emits them again.
        #
        # It must be **within-turn**. Detection can only see this turn's tool calls -- the
        # previous turn's AIMessage(tool_calls) is never written back into self.messages, so
        # the next turn's graph cannot see them -- which means the evidence's lifetime is one
        # turn. This table used to be episode-level: long after the evidence was gone the ban
        # remained, and every later turn in which the model legitimately used that
        # (tool, arguments) was removed by _filter_blocked_tool_calls; if that turn had only
        # this one call, it simply ended with "Sorry, I can't complete your request right
        # now". On a growth curve this showed up as random tasks dropping to zero, and
        # completely silently. begin_turn() clears it at the start of every turn.
        self._blocked_tool_fingerprints: set[str] = set()
        # Which fingerprints have already been warned about this turn. This used to be
        # decided by "is that SystemMessage in the messages", but the warning was only added
        # to agent_node's local messages and never returned into graph state via
        # {"messages": [response]} -- so the check was always False and the two-level
        # escalation really had only one level. Changed to instance state, with the same
        # lifetime as the blocklist.
        self._warned_tool_fingerprints: set[str] = set()
        # Episode-level accumulators: how many times tool-repeat interception fired. See the
        # note in begin_turn -- this is an engineering guardrail, not a contribution of this
        # paper, and if the method arm beats the baseline we must be able to factor it out.
        self.tool_repeat_warnings = 0
        self.tool_repeat_blocks = 0
        if self.intent_enabled:
            self._intent_paths.ensure()
            self._experiences = ExperienceStore(self._intent_paths)

    def _compute_intent_enabled(self) -> bool:
        """Intent decomposition is enabled only for the agent role and only when someone
        actually consumes the decomposition result.

        role gate: the user simulator does not take part in decomposition/injection,
        otherwise it would insert an extra real LLM call on the customer side every turn,
        and that call is not counted in token accounting, which would quietly break the
        cost accounting of the equal-budget comparison experiments; it would also mkdir a
        ./intents that the customer side never uses.

        inject / evolve gate: the baseline arm (inject=false, evolve=false) has neither, so
        nobody consumes the decomposition result, and still firing one decomposition call
        per turn would directly pollute the baseline arm's cost and latency -- and then the
        baseline is no longer a baseline. When either switch is true on its own, decomposition
        must continue: inject=false/evolve=true needs decomposition to collect candidates,
        and inject=true/evolve=false needs it to recall experiences.

        agent_impl gate: the official implementation is a faithful replica of the official
        create_react_agent, whose graph has no intent node at all, so a decomposition result
        has nowhere to be produced and nowhere to be consumed. When the baseline arm takes
        this path it must be turned off entirely, or it would fire a pile of unwanted
        decomposition calls and pollute the baseline's cost and latency.
        """
        if self.agent_impl == AGENT_IMPL_OFFICIAL:
            return False
        return self.role == "agent" and (self.inject or self.evolve)

    def _initiate_llm(self):
        config = get_llm_config(self.role, self.model_name)
        # record the model id actually in effect; logs and result filenames use it
        self.model_name = config.model
        self.llm = ChatOpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            model=config.model,
            temperature=self.temperature,
            # Network traffic goes through a proxy with occasional SSL disconnects: internal
            # retries raised from the default 2 to 3, which together with main's task-level
            # retry (up to 3 times) forms two layers of protection.
            max_retries=3,
            # Hard cap on a single call. Without it we get openai-python's 600-second
            # default, which with max_retries=3 makes a single call worst-case 40 minutes --
            # and the pipeline's llm.invoke is a synchronous blocking call, so the event loop
            # stalls and main.py's asyncio.wait_for(max_time) cannot get control during that
            # stretch and never fires at all. Measured on gate2 task 18: the dialogue took
            # only 140 seconds, after which 9 intent-system calls ate about 100 minutes, and
            # the whole task took 6288 seconds > max_time 6000 seconds yet was still recorded
            # as a normal finish. 120 seconds caps a single call at 6 minutes worst case
            # (4 attempts).
            timeout=120,
        )

    def _initiate_agent(self):
        # official path: the official ECom-Bench executor as-is -- one call to
        # create_react_agent, no intent nodes and no tool-repeat interception. The baseline
        # arm takes this path so none of this paper's changes leak in (see the comment on
        # AGENT_IMPL_OFFICIAL).
        if self.agent_impl == AGENT_IMPL_OFFICIAL:
            return create_react_agent(self.llm, self.mcp_tools)

        # intent_node decomposes the current turn's user message into intents and injects
        # the matched ones (subject to inject) into agent_node's input; unmatched candidates
        # are only stashed, left for the pipeline after the episode ends.
        all_tools = [*self.mcp_tools]
        model_with_tools = self.llm.bind_tools(all_tools)
        tool_node = ToolNode(all_tools)

        def intent_node(state: AgentState) -> Dict[str, Any]:
            messages = state.get("messages", [])
            if not messages or _message_role(messages[-1]) != "human":
                return {"active_intent_context": "", "active_intent_ids": []}

            user_message = _latest_human_message_content(messages).strip()
            recent_context = _format_recent_context(messages[:-1], max_messages=3)

            # The taxonomy is reloaded every turn: it is rewritten by the pipeline at episode end
            taxonomy = Taxonomy(self._intent_paths.taxonomy)
            taxonomy.load()
            tool_names = [str(getattr(t, "name", "")) for t in (self.mcp_tools or [])]

            # goes through the counting wrapper, so this call lands in the intent usage stats
            result = decompose(
                self.intent_llm, user_message, recent_context, taxonomy, tool_names
            )

            # candidates are not injected this turn; they are stashed until the episode ends
            self.pending_candidates.append(
                {
                    "user_message": user_message,
                    "matched": [
                        {"id": m.id, "slots": m.slots, "span": m.span}
                        for m in result.matched
                    ],
                    "candidates": [
                        {"proposed_id": c.proposed_id, "desc": c.desc,
                         "slots": c.slots, "span": c.span,
                         "from_matched": c.from_matched}
                        for c in result.candidates
                    ],
                    "non_transactional": result.non_transactional,
                }
            )

            # Every item in matched is a certain match (rules 6/7 of DECOMPOSE_RULES), with
            # no confidence left to sort by -- injecting in the LLM's raw output order is fine.
            ordered = [m.id for m in result.matched]
            # record the routing result whether or not inject is on (traj auditing needs to
            # know which intents were matched this turn)
            self.last_injected_intents = list(ordered)
            if not self.inject:
                return {"active_intent_context": "", "active_intent_ids": ordered}
            return {
                "active_intent_context": build_intent_context(ordered, self._experiences),
                "active_intent_ids": ordered,
            }

        def agent_node(state: AgentState) -> Dict[str, Any]:
            messages = state.get("messages", [])
            # Infinite-loop guard: >= 2 consecutive identical (tool, arguments) fingerprints
            # -> intercept and block. The first interception injects a system warning to make
            # the model change strategy and records the fingerprint in the cross-turn block
            # table; if it repeats after the warning (or the same fingerprint is emitted in a
            # later turn), we stop reasoning and stop executing and end the turn with a reply
            # -- tools are deterministic, identical arguments necessarily fail repeatedly, and
            # continuing to reason only burns tokens (observed: 20+ consecutive ineffective
            # calls until timeout).
            repeat = _repeated_tool_fingerprint(messages)
            if repeat is not None:
                if repeat in self._warned_tool_fingerprints:
                    # warned already and still repeating: no more reasoning, no more
                    # execution, end the turn with a reply directly.
                    return {"messages": [AIMessage(content=_TOOL_REPEAT_USER_REPLY)]}
                self._warned_tool_fingerprints.add(repeat)
                self._blocked_tool_fingerprints.add(repeat)
                messages = [
                    *messages,
                    SystemMessage(
                        content=(
                            f"{_TOOL_REPEAT_WARNING_PREFIX}You have called {repeat} "
                            "repeatedly with identical arguments, and none of them "
                            "succeeded. That call is now blocked by the system and will "
                            "not be executed again this turn or in later turns. First "
                            "look up the information you need (product / order / shop, "
                            "etc.) or ask the user for the missing details, then call "
                            "again with different arguments."
                        )
                    ),
                ]
            model_messages = inject_intent_context(
                messages, state.get("active_intent_context", "")
            )
            # Retries go here, not on AgentLangChain.call's agent_model.ainvoke: the latter
            # runs the whole graph, so tools already executed midway (placing orders,
            # refunds) would be executed again, polluting env state and reward. This is a
            # pure model call, where retrying has no side effects; if all three fail it still
            # raises as usual and is handed to main's task-level retry (with a clean env).
            response = call_with_retry(
                lambda: model_with_tools.invoke(model_messages),
                description=f"agent_node({self.model_name})",
            )
            # cross-turn blocking: if the model still emits a blocked fingerprint, remove it
            # and do not execute
            if self._blocked_tool_fingerprints:
                response = _filter_blocked_tool_calls(
                    response, self._blocked_tool_fingerprints
                )
            _print_llm_debug_call(
                stage="agent_node",
                model_name=self.model_name,
                input_messages=model_messages,
                output_message=response,
                enabled=self.verbose,
            )
            return {"messages": [response]}

        def route_from_start(state: AgentState) -> Literal["intent_node", "agent_node"]:
            # Only route through decomposition when the intent system is enabled; the user
            # simulator and the baseline arm (inject / evolve both false) go straight to
            # agent_node, see the gate description in _compute_intent_enabled.
            return "intent_node" if self.intent_enabled else "agent_node"

        def route_after_agent(state: AgentState) -> Literal["tool_node", "end"]:
            messages = state.get("messages", [])
            last_ai = _last_ai_message(messages)
            if isinstance(last_ai, AIMessage) and bool(last_ai.tool_calls):
                return "tool_node"
            return "end"

        def start_state_reset_node(state: AgentState) -> Dict[str, Any]:
            return {
                "active_intent_context": "",
                "active_intent_ids": [],
            }

        workflow = StateGraph(AgentState)
        workflow.add_node("start_state_reset_node", start_state_reset_node)
        workflow.add_node("agent_node", agent_node)
        workflow.add_node("tool_node", tool_node)

        workflow.add_edge(START, "start_state_reset_node")
        if self.intent_enabled:
            workflow.add_node("intent_node", intent_node)
            workflow.add_conditional_edges(
                "start_state_reset_node",
                route_from_start,
                {
                    "intent_node": "intent_node",
                },
            )
            workflow.add_edge("intent_node", "agent_node")
        else:
            workflow.add_conditional_edges(
                "start_state_reset_node",
                route_from_start,
                {
                    "agent_node": "agent_node",
                },
            )
        workflow.add_conditional_edges(
            "agent_node",
            route_after_agent,
            {
                "tool_node": "tool_node",
                "end": END,
            },
        )
        workflow.add_edge("tool_node", "agent_node")
        return workflow.compile()

    def begin_turn(self) -> None:
        """Reset the within-turn state at the start of every dialogue turn.

        Currently this is the two tool-repeat interception tables. Their basis (this turn's
        tool-call sequence) disappears when the turn ends, and a ban must not outlive its
        evidence -- see the note on _blocked_tool_fingerprints.

        Before clearing, the turn's interception counts are accumulated into the
        episode-level counters. Tool-repeat interception exists only in the intent executor
        (not in the official path); it is an engineering guardrail rather than this paper's
        academic contribution -- if the method arm beats the baseline, we must be able to
        answer "how much of that did the guardrail earn". A count of 0 lets us say cleanly:
        this item contributed nothing. Without recording it, that question could not be
        answered afterwards, because interception only changes the messages sent to the
        model and leaves no trace in the trajectory.
        """
        self.tool_repeat_warnings += len(self._warned_tool_fingerprints)
        self.tool_repeat_blocks += len(self._blocked_tool_fingerprints)
        self._blocked_tool_fingerprints.clear()
        self._warned_tool_fingerprints.clear()

    def consume_pending_candidates(self) -> list[Dict[str, Any]]:
        """Take away this episode's stashed per-turn decomposition results and clear them."""
        pending = self.pending_candidates
        self.pending_candidates = []
        return pending

    def discard_last_pending_candidate(self) -> None:
        """Discard the last stashed decomposition result.

        When the agent reply is empty the environment reruns the whole graph, and every
        graph run appends one entry to pending_candidates, while the session only gains one
        assistant turn. Instance reconstruction numbers turns by enumerate(pending) whereas
        tool calls' turn_index comes from the session length; once the two sides are out of
        step, after a retry every later turn's tool calls would be attributed to the previous
        turn's intents. The environment calls this before each retry, guaranteeing "one
        pending entry corresponds to one session turn". It is a no-op when the list is empty
        (including for non-agent roles).
        """
        if self.pending_candidates:
            self.pending_candidates.pop()

    @abstractmethod
    def load_system_prompt(self, system_prompt):
        """Initialize the system prompt"""
        pass

    @abstractmethod
    def call(self, message: str) -> str:
        """Message-handling method that subclasses must implement

        Args:
            message: the input message text

        Returns:
            the processed message text
        """
        pass
