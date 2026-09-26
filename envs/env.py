from envs.base import Env
from envs.dataset import Dataset
import shutil
from langchain_core.messages import AIMessage, ToolMessage
from agent import OFFLINE_SERVER_DIR, OFFLINE_CACHE_DIR, ActionTools
from utils import AGENT_IMPL_INTENT, AGENT_IMPL_OFFICIAL, is_retryable_connection_error
from typing import Any, Dict, List, Optional, Tuple
from langchain_mcp_adapters.client import MultiServerMCPClient
import time
import sys
import os
import re
import traceback
import json
import asyncio
import hashlib
from itertools import count as _count
from intent.config import intent_paths
from intent.instances import TurnDecomposition, build_instances
from intent.pipeline import run_episode_pipeline
from intent.usage import CountingLLM, UsageTracker
from intent.verifier import verify_signals

# Intent-library evolution requires serial execution (main.py forces max_concurrency==1
# when evolve=True, see _assert_safe_concurrency), so several ToolUseEnv instances running
# one after another inside a process are naturally serial and can share the same counter.
# self.task_index must not be used here to derive episode_counter: the subset selected by
# --task-ids is often sparse and non-contiguous, so it never hits a multiple of
# MERGE_SCAN_EVERY_N_EPISODES; with --num-trials > 1 task_index also restarts from the
# beginning in every trial, which disturbs the count just the same. Only by switching to
# "the number of times the pipeline is actually entered", a true count accumulated across
# instances, does "scan once every N episodes" actually take effect.
_INTENT_EPISODE_COUNTER = _count(1)


class ToolUseEnv(Env):
    """The single implementation of the tool-calling customer-service environment; the
    dataset is decided by `dataset`.

    The interaction protocol, the tool interface and the GT-checking criteria are identical
    for the two datasets (see envs/dataset.py), so there is only one implementation here:
    changing the dataset means changing three things: tasks / user_wiki / data_dir.
    """

    def __init__(
        self,
        dataset: Dataset,
        user_model: str = "gpt-4o",
        agent_model: str = "gpt-4o",
        inject: bool = True,
        evolve: bool = True,
        task_index: Optional[int] = None,
        console_verbose=None,
        intent_dir: str = "intents",
        run_id: str = "",
        trial_index: int = 0,
        metrics_dir: str = "",
        agent_impl: str = AGENT_IMPL_INTENT,
    ):
        super().__init__(
            tasks=dataset.tasks,
            user_wiki=dataset.user_wiki,
            user_model=user_model,
            agent_model= agent_model,
            task_index=task_index,
        )
        self.dataset = dataset
        self.console_verbose = console_verbose
        self.inject = inject
        self.evolve = evolve
        # Executor implementation. official goes through the official create_react_agent
        # as-is, and none of this paper's intent decomposition / injection / tool
        # interception applies — the baseline arm relies on it to stay identical to the
        # official one.
        self.agent_impl = agent_impl
        # Intent-library directory: what is obtained here is the **working copy for this
        # run batch**, not the --intent-dir given on the command line. The six experimental
        # arms share the same read-only baseline (all pointing at intents-warm-r1 in
        # run.sh); isolation no longer relies on "one directory per arm" but on main.py's
        # _resolve_working_intent_dir forking a run-private copy when a run batch starts,
        # with the source directory read-only throughout. All reads and writes this class
        # performs on it land on the copy.
        self.intent_dir = intent_dir
        # Where the mechanism metrics are persisted. The frozen evaluation segment
        # (evolve=false) does not grow, but it still has to rebuild instances and judge the
        # outcome — every mechanism metric in the paper comes from the instances. Writes
        # must stay outside self.intent_dir: that is the read-only measuring instrument
        # shared by all evaluation arms, and the evaluation segment runs concurrently.
        # The default None = do not collect; in that case evolve=false really does nothing.
        self.metrics_dir = metrics_dir
        # The run timestamp sharing the result directory's name, used to compose a traceable episode_id
        self.run_id = run_id
        # With --num-trials > 1 the same task runs several times, so the trial must go into
        # episode_id: otherwise the 2nd run overwrites the 1st run's instance files in
        # place, the ledger deduplicates by ref so the repeated run contributes nothing to
        # the admission threshold, and the outcome re-check reads the overwritten content,
        # retroactively rewriting an already-recorded judgement.
        self.trial_index = trial_index
        # Record the agent's tool calls and their results
        self.tool_calls = []            # raw call information from AIMessage.additional_kwargs['tool_calls']
        self.tool_result_messages = []  # the return results from tool messages (raw content)
        self.data_dir = str(dataset.data_dir)
        os.makedirs(self.data_dir, mode=0o777,exist_ok=True)

        
    async def a_run(self, user_strategy, agent_strategy) -> Tuple[float, List[Dict], Dict, Dict]:
        self._create_isolated_data()
        try:
            async with MultiServerMCPClient({
            "service": {
                "command": sys.executable,
                "args": [
                    os.path.join(OFFLINE_SERVER_DIR, "server.py"),
                    "--cache_dir",self.cache_dir
                    ],
                "transport": "stdio",
            }
            }) as client_service:
                match user_strategy:
                    case 'human':
                        from user import UserHuman as User
                    case 'based':
                        from user import UserBased as User
                    case 'cot':
                        from user import UserCoT as User
                    case _:
                        raise ValueError(f"Unknown user strategy: {user_strategy}")
                match agent_strategy:
                    case 'llm':
                        # The executor implementation is decided by --agent-impl: official is
                        # the official create_react_agent as-is (baseline arm); intent is this paper's intent graph.
                        if self.agent_impl == AGENT_IMPL_OFFICIAL:
                            from agent import AgentOfficial as Agent
                        else:
                            from agent import AgentLangChain as Agent
                    case _:
                        raise ValueError(f"Unknown agent strategy: {agent_strategy}")
                debug_verbose = bool(getattr(self.console_verbose, "verbose", False))
                self.customer = User(self.user_model, verbose=debug_verbose, inject=False)
                self.service = Agent(
                    **self._build_agent_kwargs(
                        agent_strategy,
                        mcp_tools=client_service.get_tools(),
                        debug_verbose=debug_verbose,
                    )
                )
                self.customer.load_system_prompt(self.user_wiki.format(instruction=self.task.instruction))
                self.service.load_system_prompt(self.agent_wiki.format(platform=self.task.platform, shop_id=self.task.shop_id, user_id = self.task.user_id))
                self.console_verbose.print(f"\n[bold blue]=== Task execution start ===[/bold blue]")  # Task execution start
                self.console_verbose.print(f"\n[bold green]Task ID: {self.task_index}[/bold green]")  # Task ID
                service_response = "Dear, is there anything I can help you with?"
                customer_response = ""
                self.termination = "max_turn"
                self.session.append(self._assistant_turn(service_response, [], []))
                for loop in range(self.max_turn):
                    last_customer_response = customer_response
                    customer_response = await self.customer.call(service_response)
                    customer_response = customer_response if customer_response != last_customer_response else "###STOP###"
                    self.console_verbose.log(f"\n[bold magenta]===============Customer response:===============\n{customer_response}[/bold magenta]")
                    self.session.append({"role": "user", "content": customer_response})
                    if self._is_done(customer_response):
                        self.termination = "stop_signal"
                        break
                    start_time = time.time()
                    service_response, turn_messages = await self._call_service_with_retry(
                        customer_response
                    )
                    end_time = time.time()
                    turn_tools = self._extract_turn_tools(turn_messages)
                    self._save_tool_calls(turn_messages)
                    self.elapsed_time.append(round(end_time - start_time, 3))
                    self.session.append(
                        self._assistant_turn(
                            service_response,
                            turn_tools,
                            list(getattr(self.service, "last_injected_intents", []) or []),
                            latency=round(end_time - start_time, 3),
                        )
                    )
                    self.console_verbose.log(f"\n[bold brown]===============Service response:===============\n{service_response}[/bold brown]")
                self.console_verbose.print(f"\n[bold blue]=== Task execution complete ===[/bold blue]")  # Task execution complete
            if loop == self.max_turn :
                print(f"warning!!! task execution exceeded {self.max_turn} turns")
            try:
                self._run_intent_pipeline()
            except Exception as exc:
                self.console_verbose.print(
                    f"\n[bold red]Intent Pipeline failed but task result is preserved: {exc}[/bold red]"
                )
                print(traceback.format_exc())
            reward, reward_actions, reward_searches, reward_outputs, reward_time = self.calculate_reward(self.session, self.elapsed_time, 1)
            detail_reward = {
                'action': reward_actions,
                'search': reward_searches,
                'output': reward_outputs,
                'time': reward_time,
            }
            tool_audit = self._build_tool_audit()
            return reward, self.session, detail_reward, tool_audit
        except Exception as e:
            # Connection-type errors must be re-raised to main's task-level retry: if they
            # are swallowed here, a Connection error during the dialogue phase becomes an
            # error result returned instead, main.py's retry loop never sees the exception
            # and is effectively a no-op. Connection errors can only come from the LLM
            # calls of the dialogue phase (the pipeline's / the judge's LLM calls all have
            # internal fallbacks and do not propagate); at that point the intent pipeline
            # has not run and the forked copy has no writes, so retrying is safe.
            if is_retryable_connection_error(e):
                raise
            self.console_verbose.print(f"[red]Task: {self.task_index} async resource management error: {str(e)}[/red]")
            print(traceback.format_exc())
            detail_reward = {
                'action': 0,
                'search': 0,
                'output': 0,
                'time': 0,
            }
            tool_audit = {
                "agent_executed_tools": [],
                "ground_truth_searches": [],
                "ground_truth_actions": [],
                "ground_truth_outputs": [],
                "total_turns": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                **UsageTracker().totals(),
                "termination": "error",
                "task_instruction": self.task.instruction,
                "turn_latencies": [],
                "turn_token_usage": [],
            }
            return 0.0, [{"error": str(e)}], detail_reward, tool_audit
        finally:
            # Make sure resources are cleaned up. The isolated data must be deleted here:
            # if it were done inside calculate_actions_reward, a task timeout or exception
            # would skip it and the cache directory would pile up.
            self._remove_isolated_data()
            await asyncio.sleep(0.1)  # give async resources some time to clean up
    
    async def _call_service_with_retry(self, customer_response: str) -> Tuple[str, List[Any]]:
        """Call the agent; retry when the reply is empty; return (reply, all messages of this turn's attempts).

        Before every retry, the decomposition result left by the previous (empty-reply)
        attempt must be discarded: re-running the whole graph appends one more entry to
        pending_candidates, while self.session only gains one more assistant turn. Instance
        reconstruction numbers turns by enumerate(pending), but the tool_calls' turn_index
        comes from the session length; once the two sides are misaligned, after a retry
        every turn's tool calls are attributed to the previous turn's intent — wrong
        evidence into the wrong instance, and completely silently.

        But what is discarded is only the **reply**, not the side effects: the empty-reply
        attempt has very likely already called tools for real and changed the database.
        Previously the caller only took detail_messages[-1] (the last attempt) for
        accounting, so those calls never entered tool_calls — the instance lost a real
        terminal call, the intent's outcome would be misjudged as incomplete, and mixed
        with the later genuine terminal call it could not be attributed either. So here
        every attempt's messages in this turn are returned to the caller for accounting
        together.

        Concatenation is safe: the agent only writes the final reply's text back into
        self.messages, the AIMessage(tool_calls)/ToolMessage produced by the previous
        attempt will not appear in the next attempt's message list, and _save_tool_calls
        only recognises these two kinds of messages, so nothing is double-counted.
        """
        before = len(self.service.detail_messages)
        service_response = await self.service.call(customer_response)
        while len(service_response) == 0:
            discard = getattr(self.service, "discard_last_pending_candidate", None)
            if callable(discard):
                discard()
            service_response = await self.service.call(customer_response)
        turn_messages = [
            message
            for attempt in self.service.detail_messages[before:]
            for message in attempt
        ]
        return service_response, turn_messages

    def _build_agent_kwargs(self, agent_strategy: str, mcp_tools, debug_verbose: bool) -> Dict[str, Any]:
        """Assemble the Agent constructor arguments.

        inject and evolve must be forwarded together: the LLM class's _compute_intent_enabled
        uses these two switches to decide whether to enable the intent node; missing either
        one silently judges the method arm as Baseline and skips intent decomposition for the
        whole segment.
        """
        agent_kwargs: Dict[str, Any] = {
            "agent_model": self.agent_model,
            "mcp_tools": mcp_tools,
            "verbose": debug_verbose,
        }
        # The official executor's constructor signature matches the official one and has no
        # notion of inject/evolve/intent_dir at all — passing them in would raise TypeError,
        # which is exactly what we want: the baseline should not have these parameters, and
        # the signature itself is a line of defence.
        if agent_strategy == "llm" and self.agent_impl != AGENT_IMPL_OFFICIAL:
            agent_kwargs["inject"] = self.inject
            agent_kwargs["evolve"] = self.evolve
            agent_kwargs["intent_dir"] = self.intent_dir
        return agent_kwargs

    def _is_done(self, message: str) -> bool:
        return "###STOP###" in str(message)

    def _assistant_turn(self, content, tool_calls, intents, latency=None):
        """Assemble one assistant trajectory. When inject=False no skills key is written;
        the baseline trajectory should not contain any skill/intent-related field."""
        turn = {"role": "assistant", "content": content, "tool_calls": tool_calls}
        if self.inject:
            turn["skills"] = intents
        if latency is not None:
            turn["latency"] = latency
        return turn
    
    def _create_isolated_data(self):
        # generate a 16-character random uuid as the session_id
        import uuid
        self.session_id = str(uuid.uuid4())[:16]
        self.cache_dir = os.path.join(OFFLINE_CACHE_DIR, self.session_id)
        os.makedirs(self.cache_dir, exist_ok=True, mode=0o777)
        os.chmod(self.cache_dir, 0o777)
        # copy all the json files of data_dir into cache_dir
        for file in os.listdir(self.data_dir):
            if file.endswith(".json"):
                shutil.copy(os.path.join(self.data_dir, file), self.cache_dir)
    
    def _remove_isolated_data(self):
        # Delete the created folder. It may be called repeatedly, and may also be reached
        # before _create_isolated_data, so it must be idempotent here and must not let a
        # failed cleanup mask the real task exception.
        cache_dir = getattr(self, "cache_dir", None)
        if not cache_dir:
            return
        shutil.rmtree(cache_dir, ignore_errors=True)
    
    def _load_data(self, base_dir):
        data = {}
        files = os.listdir(base_dir)
        json_files = [f for f in files if f.endswith('.json')]
        if len(json_files) == 0:
            return data
        else:
            for json_file in json_files:
                file_path = os.path.join(base_dir, json_file)
                file_name = os.path.splitext(json_file)[0]
                with open(file_path, 'r',encoding='utf-8') as f:
                    data[file_name] = json.load(f)
        return data
    
    def calculate_reward(self, session: list[Dict], elapsed_time: List[float], reward: int = 1):
        """
        Compute the reward
        :param history: the history record
        :param elapsed_time: the time consumed
        :return: the reward result
        """
        self.console_verbose.log("\n[bold blue]=== Reward calculation start ===[/bold blue]")  # Reward calculation start
        reward_time = self.calculate_time_reward(elapsed_time, self.max_time_limit)
        reward_actions = 1 if self.calculate_actions_reward() else 0
        reward_searches = 1 if self.calculate_searches_reward() else 0
        reward_outputs = 1 if self.calculate_outputs_reward() else 0
        # The four reward dimensions and the final reward are the core results of the experiment, so log them even when verbose=false
        self.console_verbose.print(f"\n[bold green]Action reward [0-1]: {reward_actions}[/bold green]")
        self.console_verbose.print(f"\n[bold green]Search reward [0-1]: {reward_searches}[/bold green]")
        self.console_verbose.print(f"\n[bold green]Output reward [0-1]: {reward_outputs}[/bold green]")
        self.console_verbose.print(f"\n[bold green]Time reward [0-1]: {reward_time}[/bold green]")
        reward = 1 * reward_actions * reward_searches * reward_outputs
        self.console_verbose.print(f"\n[bold green]Final computed reward: {reward}[/bold green]")  # Reward
        return reward, reward_actions, reward_searches, reward_outputs, reward_time

    def calculate_actions_reward(self):
        self.original_data = self._load_data(base_dir=self.data_dir)
        self.modified_data = self._load_data(base_dir=self.cache_dir)
        # Cleanup is left to a_run's finally; here we only read the data
        if len(self.task.metadata.actions) > 0:
            self._actions_to_tools()
        
        # Normalise the data to ensure consistent hash computation
        def normalize_data(data):
            """Recursively normalise the data structure so that identical content produces the same hash"""
            if isinstance(data, dict):
                # sort the dict by key and recursively normalise the values
                return {k: normalize_data(v) for k, v in sorted(data.items())}
            elif isinstance(data, list):
                # normalise the list elements and sort them (if the elements are comparable)
                normalized_list = [normalize_data(item) for item in data]
                try:
                    # try to sort the list to ensure consistency
                    if all(isinstance(item, (str, int, float)) for item in normalized_list):
                        return sorted(normalized_list)
                    elif all(isinstance(item, dict) for item in normalized_list):
                        # sort the list of dicts by each dict's string representation
                        return sorted(normalized_list, key=lambda x: json.dumps(x, sort_keys=True))
                    else:
                        return normalized_list
                except (TypeError, ValueError):
                    # if it cannot be sorted, keep the original order
                    return normalized_list
            else:
                return data
            
        # normalise the data
        normalized_original = normalize_data(self.original_data)
        normalized_modified = normalize_data(self.modified_data)
        
        # compute the hash of the normalised data
        original_data_hash = hashlib.sha256(
            json.dumps(normalized_original, sort_keys=True, ensure_ascii=False).encode('utf-8')
        ).hexdigest()
        modified_data_hash = hashlib.sha256(
            json.dumps(normalized_modified, sort_keys=True, ensure_ascii=False).encode('utf-8')
        ).hexdigest()
        
        return original_data_hash == modified_data_hash

    def _actions_to_tools(self):
        action_tools = ActionTools()
        actions = self.task.metadata.actions
        tools = action_tools.get_available_functions()
        for action in actions:
            for tool in tools:
                if action.name == tool:
                    self.original_data, _ = action_tools.call_function(action.name, data = self.original_data, **action.arguments)
                    break

    def _normalize_tool_arguments(self, args):
        """Normalize tool call arguments into a dictionary."""
        if isinstance(args, dict):
            return args
        if isinstance(args, str):
            try:
                parsed = json.loads(args)
            except Exception:
                return {}
            return parsed if isinstance(parsed, dict) else {}
        return {}
    
    def _extract_turn_tools(self, detail_message):
        """Extract this turn's tool calls and their corresponding returns in call order from the turn messages, for writing into the traj."""
        calls_with_id = []  # (id, name, arguments)
        results_by_id = {}  # id -> content
        for msg in detail_message:
            if isinstance(msg, AIMessage):
                for tc in (msg.additional_kwargs.get("tool_calls") or []):
                    fn = tc.get("function", {})
                    args = self._normalize_tool_arguments(fn.get("arguments", {}))
                    calls_with_id.append((tc.get("id") or tc.get("tool_call_id"), fn.get("name", ""), args))
            if isinstance(msg, ToolMessage):
                cid = getattr(msg, "tool_call_id", None)
                if cid is not None:
                    results_by_id.setdefault(cid, []).append(getattr(msg, "content", None))
        out = []
        for call_id, name, args in calls_with_id:
            res = results_by_id.get(call_id)
            if res is not None:
                result = res[0] if len(res) == 1 else res
            else:
                result = None
            out.append({
                "name": name,
                "arguments": args,
                "result": result,
                "status": self._infer_tool_call_status(result),
            })
        return out

    def _save_tool_calls(self, detail_message):
        """Extract the tool calls and their return results from this turn's detailed messages of the agent's calls."""
        for msg in detail_message:
            # 1) save the tool_calls in the AIMessage (including id, name, arguments)
            if isinstance(msg, AIMessage):
                tool_calls = msg.additional_kwargs.get("tool_calls")
                if tool_calls:
                    for tool_call in tool_calls:
                        self.tool_calls.append(tool_call)

            # 2) save the ToolMessage: recognise it with isinstance to avoid missing any
            if isinstance(msg, ToolMessage):
                result_record = {
                    "tool_call_id": getattr(msg, "tool_call_id", None),
                    "content": getattr(msg, "content", None),
                }
                self.tool_result_messages.append(result_record)

    def _run_intent_pipeline(self) -> None:
        """Update the intent library after an episode ends; with evolve=false it degrades to
        only collecting mechanism metrics.

        Note: this never references reward — that is the labelling result and is used only
        for the final evaluation.

        When evolve=false and a metrics_dir is given it must still run: steps one and two of
        the pipeline are pure measurement (rebuild instances + judge outcome — the matcher
        is only created at step three), and the frozen evaluation segment's mechanism
        metrics depend on it entirely. Steps three to six are not executed; see the
        `if not evolve` early return in run_episode_pipeline.

        The judge (_verify_signals) is run once before judging the outcome to obtain the
        negative signals, so this method also makes one LLM call in the evaluation segment —
        it is a pure call and needs no MCP session.
        """
        # The official executor has no intent node and produces no decomposition result at
        # all, so the pipeline has nothing to do. It must return here: with evolve=false a
        # metrics_dir is still derived (see main._resolve_metrics_dir), the
        # `not evolve and not metrics_dir` check below cannot stop it, and it would run all
        # the way to self.service.consume_pending_candidates() — which by definition the
        # official executor does not have, so the baseline arm would crash at the end of the
        # episode.
        if self.agent_impl == AGENT_IMPL_OFFICIAL:
            return
        if not self.evolve and not self.metrics_dir:
            self.console_verbose.print("\n[bold cyan]Intent Pipeline: disabled by --evolve false.[/bold cyan]")
            return

        pending = self.service.consume_pending_candidates()
        # Audit record: consume clears the service-side buffer, and _build_tool_audit runs
        # only after this, by which time the decomposition result can no longer be obtained.
        # All of the offline sensitivity analysis of τ depends on this record.
        self._episode_decompositions = list(pending)
        if not pending:
            self.console_verbose.print("\n[bold cyan]Intent Pipeline: no decomposition result this turn, skipping.[/bold cyan]")
            return

        turns = [
            TurnDecomposition(
                turn_index=index,
                matched=item.get("matched", []),
                candidates=item.get("candidates", []),
                # carry the original user message so that instance reconstruction can restore the true
                # order in which multiple intents occur, by the span's position in the message
                # (otherwise it could only follow the matched-first concatenation order)
                user_message=str(item.get("user_message", "") or ""),
            )
            for index, item in enumerate(pending)
        ]
        conversation, tool_calls = self._build_distillation_inputs()

        # The pipeline is a pure write path; one episode may make dozens of LLM calls, all
        # counted against the agent's intent usage; if the service has no tracker, one is
        # created on the spot, so only this run's usage has no outlet, which does not affect
        # the main flow. The judge and the pipeline share the same tracker, so the cost of
        # the judge's one LLM call is also counted into intent usage.
        tracker = getattr(self.service, "intent_usage", None) or UsageTracker()
        signals = self._verify_signals(turns, tool_calls, conversation, tracker)
        report = run_episode_pipeline(
            episode_id=f"{self.run_id or 'run'}-t{self.task_index}-r{self.trial_index}",
            turns=turns,
            tool_calls=tool_calls,
            paths=intent_paths(self.intent_dir),
            llm=CountingLLM(getattr(self.service, "llm", None), tracker),
            # The counter's only consumer is "a merge scan once every N episodes", and the
            # merge scan only happens when evolve=true. If the frozen segment advanced it,
            # the later growth batches in the same process would never hit the divisibility
            # point they are supposed to, so it is not consumed here.
            episode_counter=next(_INTENT_EPISODE_COUNTER) if self.evolve else 0,
            signals=signals,
            evolve=self.evolve,
            instance_sink=intent_paths(self.metrics_dir) if self.metrics_dir else None,
        )
        self.console_verbose.print(
            f"\n[bold cyan]Intent Pipeline: {json.dumps(report, ensure_ascii=False, default=str)}[/bold cyan]"
        )

    def _verify_signals(
        self,
        turns: List[TurnDecomposition],
        tool_calls: List[Dict[str, Any]],
        conversation: List[Dict[str, str]],
        tracker: UsageTracker,
    ) -> Dict[str, Dict[str, bool]]:
        """Judge this episode's negative signals; a failure must never affect the task result.

        negative_signal / repeated_query are one of the three sources of negative labels for
        classify_outcome and must be obtained before the pipeline judges the outcome. Lose
        them and the criterion degrades into the looser rule "a successful call means
        success" — that would label an intent where "customer service claims completion but
        actually did nothing" as success, which does not match the criterion described in
        the paper.

        This is a pure LLM call and needs no MCP session, so it is placed outside a_run's
        async with and run together with the pipeline. verify_signals already falls back to
        an empty table on an LLM failure (all False = the judge does not intervene); here it
        is caught once more, because steps such as building instances and getting the llm
        are also outside the try: a completely failed judge should not destroy a task that
        has already run to completion, only this run's signals are missing.
        """
        try:
            instances = build_instances(turns, tool_calls)
            return verify_signals(
                CountingLLM(getattr(self.service, "llm", None), tracker),
                instances,
                conversation,
            )
        except Exception as exc:  # noqa: BLE001
            self.console_verbose.print(
                f"\n[bold red]Verifier failed but task result is preserved: {exc}[/bold red]"
            )
            print(traceback.format_exc())
            return {}

    def _build_distillation_inputs(self) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
        conversation: List[Dict[str, str]] = []
        tool_calls: List[Dict[str, Any]] = []
        pending_user_message: Optional[str] = None

        for message in self.session:
            role = str(message.get("role", "")).lower()
            if role == "user":
                pending_user_message = self._normalize_distillation_text(message.get("content", ""))
                continue

            if role != "assistant" or pending_user_message is None:
                continue

            turn_index = len(conversation)
            assistant_reply = self._normalize_distillation_text(message.get("content", ""))
            conversation.append({
                "user": pending_user_message,
                "assistant": assistant_reply,
            })

            for tool_call in (message.get("tool_calls") or []):
                tool_name = str(tool_call.get("name", "")).strip()
                if not tool_name:
                    continue
                arguments = self._normalize_tool_arguments(tool_call.get("arguments", {}))
                result = tool_call.get("result")
                tool_calls.append({
                    "turn_index": turn_index,
                    "tool_name": tool_name,
                    "parameters": self._sanitize_tool_arguments_for_distillation(arguments),
                    "result_summary": self._summarize_tool_result_for_distillation(result),
                    "status": self._infer_tool_call_status(result),
                })

            pending_user_message = None

        return conversation, tool_calls

    def _get_available_tools_for_distillation(self) -> List[Dict[str, str]]:
        available_tools: List[Dict[str, str]] = []
        seen: set[str] = set()
        for tool in getattr(self.service, "mcp_tools", []) or []:
            tool_name = str(getattr(tool, "name", "") or "").strip()
            if not tool_name or tool_name in seen:
                continue
            seen.add(tool_name)
            description = self._normalize_distillation_text(getattr(tool, "description", "") or "")
            available_tools.append({
                "tool_name": tool_name,
                "description": description or "No description provided.",
            })
        return available_tools

    def _normalize_distillation_text(self, value: Any, *, max_chars: int = 240) -> str:
        if isinstance(value, (dict, list)):
            text = json.dumps(value, ensure_ascii=False, default=str)
        else:
            text = str(value)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            return ""
        if len(text) > max_chars:
            return f"{text[: max_chars - 3]}..."
        return text

    def _sanitize_tool_arguments_for_distillation(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        sensitive_keys = {
            "address",
            "amount",
            "bank_account",
            "card_no",
            "card_number",
            "credential",
            "credentials",
            "email",
            "id_card",
            "mobile",
            "name",
            "password",
            "phone",
            "phone_number",
            "real_name",
            "recipient",
            "token",
            "user_name",
        }

        def scrub(value: Any, parent_key: str = "") -> Any:
            key = parent_key.lower()
            if key in sensitive_keys:
                return "<redacted>"
            if isinstance(value, dict):
                return {
                    str(k): scrub(v, str(k))
                    for k, v in value.items()
                }
            if isinstance(value, list):
                return [scrub(item, parent_key) for item in value[:20]]
            return value

        return scrub(arguments) if isinstance(arguments, dict) else {}

    def _summarize_tool_result_for_distillation(self, result: Any) -> str:
        if result is None:
            return "No result returned."
        return self._normalize_distillation_text(result, max_chars=200) or "Empty result."

    @staticmethod
    def _is_structured_tool_result(result: Any) -> bool:
        """Return whether this is structured data (a dict/list, or a JSON string that parses
        into one of them).

        The offline tools' convention is as in agent/servers/offline/tools/*: on a hit
        `return data, json.dumps(result, ensure_ascii=False)`, on a miss return a single
        English sentence ("no information found for ...", "product ID ... has the wrong
        format"). None of the tools expresses failure with a structured return, so "parses
        into a dict/list" is equivalent to "this query got data".
        """
        if isinstance(result, (dict, list)):
            return True
        if not isinstance(result, str):
            return False
        try:
            return isinstance(json.loads(result), (dict, list))
        except (ValueError, TypeError):
            return False

    def _infer_tool_call_status(self, result: Any) -> str:
        if result is None:
            return "failure"
        # A structured return is judged success directly and does not go into the substring
        # matching below: the body of business data naturally contains failure words (the
        # fault name "water pressure abnormal", the solution "if it is still abnormal please
        # book a repair", the fault name "ignition failed"), and matching on the body would
        # judge a successful query as a failure. calculate_searches_reward counts only
        # successful calls, so this kind of misjudgement turns directly into a reward
        # deduction — the GT search items of task 9 / 45 can never be satisfied for exactly
        # this reason.
        if self._is_structured_tool_result(result):
            return "success"
        # Business-conclusion label: the tools mark "the query completed normally and the
        # answer is negative" with a trailing (…).
        # register_cashback_by_review(action="query") is the only offline tool that returns
        # this way — the order exists and the query has completed, but the review has not
        # been submitted, yet the sentence starts with "Not found". Such returns must be
        # judged success: the call really happened and produced a business answer, so the
        # agent's search behaviour is complete. Judged failure, calculate_searches_reward
        # would skip it and this GT search item could never be satisfied however well the
        # agent did (in practice each of the three results/growth arms structurally lost
        # points on 6 tasks for this reason, most of which had already passed action/output).
        # The label is at the end of the sentence, so it must not be looked for in the text
        # truncated to 200 characters below.
        completion_markers = ('(review not submitted)', '(review submitted)', '(cashback issued)')
        if self._normalize_distillation_text(result, max_chars=4000).rstrip().endswith(
            completion_markers
        ):
            return "success"
        text = self._normalize_distillation_text(result, max_chars=200).lower()
        failure_markers = (
            "error",
            "exception",
            "failed",
            "failure",
            "traceback",
            "invalid",
            "not found",
            "no result returned",
            # The real failure returns of this environment's offline tools
            # (manage_order/get_*_info etc.) are phrased in English, e.g. "no information
            # found for user {id}", "no information found for order {id}" or "product ID
            # {id} has the wrong format"; the markers below catch them. "cannot" / "does not
            # support" are deliberately not added: product descriptions and installation
            # instructions often contain "cannot install it yourself" or "does not support
            # the 7-day no-reason return", which would wrongly hit normal product-data
            # returns.
            'Not found',
            'not found',
        )
        return "failure" if any(marker in text for marker in failure_markers) else "success"

    def _collect_decomposition_audit(self) -> List[Dict[str, Any]]:
        """The per-turn intent routing result, keeping only the fields the τ sensitivity
        analysis needs.

        Two ways to obtain the data: if the pipeline ran, use the record it left when
        consuming (`_episode_decompositions`); if it did not run (--evolve false with no
        metrics_dir, or the pipeline threw midway), read the service-side buffer that has
        not been cleared. Both empty means no intent node was enabled this turn at all
        (baseline arm), so return an empty list.

        Deliberately no span or slots: they are already in the instances, and results.json
        is already on the order of 2MB, so storing the original text turn by turn again
        would double its size, while not a single character of the τ analysis needs them.
        """
        pending = getattr(self, "_episode_decompositions", None)
        if not pending:
            pending = list(getattr(self.service, "pending_candidates", None) or [])
        audit: List[Dict[str, Any]] = []
        for index, item in enumerate(pending):
            matched = [
                {"id": m.get("id"), "confidence": m.get("confidence")}
                for m in (item.get("matched") or [])
            ]
            # Only keep the candidates with from_matched: candidates proposed directly by the
            # LLM have no confidence, and mixing them in would inflate τ's denominator and
            # depress the distribution.
            downgraded = [
                {"id": c.get("proposed_id"), "confidence": c.get("confidence")}
                for c in (item.get("candidates") or [])
                if c.get("from_matched")
            ]
            if not matched and not downgraded:
                continue
            audit.append({"turn": index, "matched": matched, "downgraded": downgraded})
        return audit

    def _build_tool_audit(self):
        """Collect the tool calls executed by the Agent and the task ground truth, to write into the result JSON for inspection."""
        # build a mapping from call id -> returned content by tool_call_id (one id may correspond to several entries, so use a list)
        results_by_id = {}
        for r in self.tool_result_messages:
            cid = r.get("tool_call_id")
            if cid is not None:
                results_by_id.setdefault(cid, []).append(r.get("content"))

        agent_executed_tools = []
        for tool_call in self.tool_calls:
            fn = tool_call.get("function", {})
            name = fn.get("name", "")
            args = self._normalize_tool_arguments(fn.get("arguments", {}))
            call_id = tool_call.get("id") or tool_call.get("tool_call_id")
            result_list = results_by_id.get(call_id) if call_id else None
            if not result_list:
                tool_record = {"name": name, "arguments": args}
            else:
                tool_record = {
                    "name": name,
                    "arguments": args,
                    "results": result_list[0] if len(result_list) == 1 else result_list,
                }
            agent_executed_tools.append(tool_record)
        ground_truth_searches = [s.model_dump() for s in self.task.metadata.searches]
        ground_truth_actions = [a.model_dump() for a in self.task.metadata.actions]
        total_turns = max(
            0,
            sum(1 for msg in self.session if msg.get("role") == "assistant") - 1,
        )
        token_usage = getattr(self.service, "token_usage_totals", {}) or {}
        prompt_tokens = int(token_usage.get("prompt_tokens") or 0)
        completion_tokens = int(token_usage.get("completion_tokens") or 0)
        total_tokens = int(token_usage.get("total_tokens") or (prompt_tokens + completion_tokens))
        # The intent system's overhead is listed separately from the main dialogue's: the
        # main-dialogue numbers keep their original scale so they can be compared with
        # historical results, while the intent numbers are listed on their own, so that when
        # comparing against a budget the two must be added to get the intent arm's real cost.
        intent_usage = getattr(self.service, "intent_usage", None)
        intent_totals = (
            intent_usage.totals()
            if intent_usage is not None
            else UsageTracker().totals()
        )
        return {
            **intent_totals,
            "intent_decompositions": self._collect_decomposition_audit(),
            # The number of times tool-repeat interception triggered. It exists only in the
            # intent executor and is an engineering guardrail rather than a contribution of
            # this paper — when the method arm beats the baseline it must be able to be
            # pulled out and attributed separately.
            # begin_turn accumulates it every turn; the official arm does not have these two
            # attributes, so take 0.
            "tool_repeat_warnings": int(getattr(self.service, "tool_repeat_warnings", 0) or 0),
            "tool_repeat_blocks": int(getattr(self.service, "tool_repeat_blocks", 0) or 0),
            "agent_executed_tools": agent_executed_tools,
            "ground_truth_searches": ground_truth_searches,
            "ground_truth_actions": ground_truth_actions,
            "ground_truth_outputs": list(self.task.metadata.outputs or []),
            "total_turns": total_turns,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "termination": getattr(self, "termination", None),
            "task_instruction": self.task.instruction,
            "turn_latencies": list(self.elapsed_time),
            "turn_token_usage": list(getattr(self.service, "token_usage_per_turn", []) or []),
        }

    def calculate_searches_reward(self):
        """Search reward. **The criterion is identical to the official ECom-Bench: the call
        status is not inspected.**

        The upstream ECom-Bench implementation
        (envs/story/env.py::calculate_searches_reward) counts every entry in self.tool_calls
        into the hash set, and treats it as a hit as long as the signature matches a GT
        search item, regardless of whether that call succeeded.

        A status=="success" filter was once added here, on the grounds that "a query with
        wrong parameters should not satisfy the GT". That reason holds in itself, but it
        turned the reward into a different ruler from the official one: reward is a
        **measuring instrument**, not the object being measured; once it diverges, this
        work's absolute numbers can no longer be aligned with the original paper, and the
        collateral damage of tightening had to be patched up by _infer_tool_call_status
        (in practice the "(review not submitted)" return of register_cashback_by_review was
        misjudged as failure, so the GT search items of 7 tasks could never be satisfied).
        It has now been reverted to the official criterion: all arms share the same ruler,
        and that ruler is the official one.
        """
        service_data_hash = set()
        for tool_call in self.tool_calls:
            fn = tool_call.get("function", {})
            raw_arguments = fn.get("arguments", {})
            if isinstance(raw_arguments, str):
                try:
                    arguments = json.loads(raw_arguments)
                except Exception:  # noqa: BLE001
                    # The official code does traceback.print_exc() then continue here: a call
                    # whose arguments cannot be parsed does not enter the hash set. Keep the
                    # same trade-off, only without printing the stack.
                    continue
            else:
                arguments = raw_arguments
            hashed_fn = {"name": fn.get("name", ""), "arguments": arguments}
            service_data_hash.add(self._function_to_hash(hashed_fn))
        search_data_hash = set()
        for search in self.task.metadata.searches:
            search_data_hash.add(self._function_to_hash(search.model_dump()))
        try:
            tool_functions = [tool_call['function'] for tool_call in self.tool_calls]
            self.console_verbose.log_table(
                tool_functions, 
                title="The Tools Invoked by Agent", 
                name_column="Name", 
                args_column="Arguments"
            )
        except:
            self.console_verbose.log(f"\n[bold red]The Tools Invoked by Agent:\n\n{json.dumps([tool_call['function'] for tool_call in self.tool_calls], ensure_ascii=False, indent=2)}[/bold red]")
            
        return search_data_hash.issubset(service_data_hash)
    
    def _function_to_hash(self, function):
        """
        function = {
            "name": "get_product_info",
            "arguments": {
                "product_id": "123456"
            }
        }
        """
        function = json.dumps(function, sort_keys=True, ensure_ascii=False)
        data_hash = hashlib.sha256(function.encode('utf-8')).hexdigest()
        return data_hash
        
    def calculate_outputs_reward(self):
        long_string = "".join([msg['content'] for msg in self.session if msg['role'] == 'assistant'])
        return all([output in long_string for output in self.task.metadata.outputs])
    
    def calculate_time_reward(self, elapsed_time: List[float], max_limit:int):
        """
        Compute the time reward
        :param elapsed_time: the time consumed
        :param max_limit: the maximum limit
        :param ratio: the ratio
        :return: the reward result

        Return 0.0 when there is no usable timing (not a single dialogue turn ran) instead
        of raising. The time dimension does not enter the final reward (in calculate_reward
        reward = actions * searches * outputs); it only lands in detail_reward; letting it
        raise would mean using a non-scoring metric to throw away the whole episode's
        result together with the session, the tool audit and the intent instances — in
        practice results/e1's full arm task 8 was lost exactly this way: elapsed_time was
        empty, the ZeroDivisionError bubbled up to a_run's fallback, that episode was
        recorded as termination=error and reward=0, giving the control group a point for
        free.
        """
        if not elapsed_time:
            return 0.0
        avg_time = sum(elapsed_time) / len(elapsed_time)
        if avg_time <= 0:
            return 0.0
        elif avg_time > max_limit:
            return 0.0
        else:
            # Use an inverse-proportion function to produce a smooth curve, keeping it between 0 and 0.5
            return round((max_limit - avg_time) / (max_limit + avg_time), 3)
            
    
