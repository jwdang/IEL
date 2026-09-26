"""A faithful copy of the official ECom-Bench executor -- used only by the baseline arm.

The reference is ECom-Bench/agent/agents_list/agent_langchain.py (byte-for-byte identical
to the repository's first commit, 913b45f).

This file **deliberately does not reuse** AgentLangChain, and its base class is not
utils.LLM either -- both of those are this paper's code (intent decomposition, experience
injection, duplicate-tool interception). The baseline follows a separate inheritance
chain, official_runtime.OfficialLLM, so that "baseline == official" holds structurally
rather than being maintained by reviewing every change line by line.

Compared line by line with the official AgentLangChain there are only three differences,
and none of them enters the reasoning path:

1. TokenUsageMixin's per-turn token accounting. The official version does not report
   cost, and the equal-budget control experiment requires it. It only reads the usage
   metadata of the AIMessage and modifies no message. It is deliberately imported from
   utils rather than copied again: pure measurement code copied twice would only drift
   apart.
2. config={"recursion_limit": 60}. The official version uses the default 25, which after
   about 10 tool iterations raises GraphRecursionError and turns the whole episode into
   an error. Together with max_retries this is harness-level robustness plumbing, and the
   authors confirmed it is shared by all arms.
3. debug=False fixed. The official version passes debug=self.verbose, which would write
   the full prompt into the log. It only affects logging.
"""

from utils import TokenUsageMixin

from .official_runtime import OfficialLLM


class AgentOfficial(TokenUsageMixin, OfficialLLM):
    def __init__(self, agent_model: str, verbose: bool = False, mcp_tools=None, temperature: float = 0.3):
        # The official signature has no inject/evolve/intent_dir -- the baseline should
        # not have those concepts, and passing them in would be a TypeError; the
        # signature itself is a line of defense.
        super().__init__(
            model_name=agent_model,
            verbose=verbose,
            mcp_tools=mcp_tools,
            temperature=0.3,
            role="agent",
        )
        self.agent_model = super()._initiate_agent()
        self.detail_messages = []
        self._init_token_usage()

    def load_system_prompt(self, system_prompt):
        self.messages.append({"role": "system", "content": system_prompt})

    async def call(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        self._call_counter += 1
        responses = await self.agent_model.ainvoke(
            input={"messages": self.messages},
            config={"recursion_limit": 60},
            debug=False,
        )
        self._accumulate_token_usage(
            responses.get("messages", []), call_index=self._call_counter
        )
        self.detail_messages.append(responses["messages"])
        self.messages.append(
            {"role": "assistant", "content": responses["messages"][-1].content}
        )
        return responses["messages"][-1].content
