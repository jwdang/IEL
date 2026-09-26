from utils import AGENT_IMPL_INTENT, LLM, TokenUsageMixin

class AgentLangChain(TokenUsageMixin, LLM):
    """This paper's executor: intent decomposition / experience injection.

    The baseline arm **does not go through here**; it uses
    agent_official.AgentOfficial (the official create_react_agent, unchanged). The only
    things the two share are the LLM client construction and token accounting.
    """

    def __init__(self, agent_model:str, verbose=False, mcp_tools= [], temperature = 0.3, inject: bool = True, intent_dir: str = "intents", evolve: bool = True):
        super().__init__(model_name=agent_model, verbose=verbose, mcp_tools=mcp_tools, temperature = 0.3, inject=inject, intent_dir=intent_dir, evolve=evolve, agent_impl=AGENT_IMPL_INTENT)
        self.agent_model = super()._initiate_agent()
        self.detail_messages = []
        self.active_intent_context = ""
        self.active_intent_ids = []
        # Tokens added in each turn (each call), used for cost accounting in the
        # equal-budget control experiment
        self._init_token_usage()


    def load_system_prompt(self, system_prompt):
        self.messages.append({"role": "system", "content": system_prompt})


    async def call(self, message:str) -> str:
        # Per-turn state (the ban/warning tables of the duplicate-tool interceptor) is
        # cleared every turn: they are based on this turn's tool-call sequence, and the
        # previous turn's AIMessage(tool_calls) is never written back to self.messages.
        self.begin_turn()
        self.messages.append({"role": "user", "content": message})
        self._call_counter += 1
        # **Deliberately no retry here**: ainvoke runs the whole graph, so tools already
        # executed along the way (placing an order, refunding) would be executed again on
        # a retry, corrupting the env state and the reward. The actual model call inside
        # the graph is the agent_node in utils.LLM._initiate_agent, and the retry is added
        # there (it has no side effects); connection-type errors are caught further up by
        # main's task-level retry (which switches to a clean isolated_env).
        responses = await self.agent_model.ainvoke(
            input = {
                "messages": self.messages,
                "active_intent_context": self.active_intent_context,
                "active_intent_ids": self.active_intent_ids,
            },
            # The default recursion_limit=25 only covers about 10 tool iterations, so
            # when the model calls tools repeatedly it turns the whole episode into an
            # error (4 of 10 warmup runs were lost to this). Raised to 60 (about 27
            # iterations), which is still bounded together with max_turn=20.
            config={"recursion_limit": 60},
            # Disable LangGraph event dump to avoid printing full prompts/messages.
            debug=False
        )
        self.active_intent_context = str(responses.get("active_intent_context", "") or "")
        self.active_intent_ids = [str(intent_id) for intent_id in (responses.get("active_intent_ids", []) or [])]
        self._accumulate_token_usage(
            responses.get("messages", []),
            call_index=self._call_counter,
        )
        self.detail_messages.append(responses["messages"])
        self.messages.append({"role": "assistant", "content": responses["messages"][-1].content})
        # print(self.detail_messages)
        return responses["messages"][-1].content
