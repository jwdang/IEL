"""A standalone copy of the official ECom-Bench executor base class -- used only by the
baseline arm, and it does not touch utils.LLM.

Reference: `utils.py::LLM` as of the repository's first commit, 913b45f (the original
official code).

**Why a separate copy instead of reusing utils.LLM**
utils.LLM has grown to 800 lines, and it contains this paper's machinery: intent nodes,
experience injection, duplicate-tool interception, and the CountingLLM accounting
wrapper. Even if agent_impl is set to official so that none of those branches execute and
behaviour is equivalent, the baseline would still be running **our class** -- its
__init__ creates pending_candidates, intent_usage, CountingLLM and the fingerprint
tables, and any change to utils.LLM could leak into the baseline down the inheritance
chain, which is exactly what this file exists to prevent. The baseline's code path must
stand on its own, so that "baseline == official" holds structurally rather than being
maintained by reviewing every change.

**Differences from the official LLM, item by item**

1. `_initiate_llm` takes base_url/api_key/model from llm_config.get_llm_config, whereas
   the official code is a series of hardcoded branches of the form
   `if model_name == 'glm-4-flash'`. This had to change: this whole repo goes through an
   OpenAI-compatible interface plus .env credentials, so copying that official block
   would fail to reach the model. The model parameter (temperature) keeps the official
   value.
2. `max_retries=3` and a per-call timeout. The official version has neither. Confirmed
   with the authors: robustness plumbing belongs to the harness layer and is shared by
   all arms -- it does not change the quality of model reasoning, it only determines
   whether an episode can finish; without retries a single network hiccup would hand the
   baseline a gratuitous 0, which would actually favor this paper's method.
3. Only the abstract methods load_system_prompt / call are kept, matching the official
   version.

Otherwise -- the graph built by create_react_agent, the maintenance of messages, the set
of attributes -- it matches the official code line for line. None of this paper's
machinery is in here.
"""

from abc import ABC, abstractmethod

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from llm_config import get_llm_config


class OfficialLLM(ABC):
    """A standalone copy of the official utils.LLM. Nothing from this paper is in its
    inheritance tree."""

    def __init__(self, model_name: str, verbose: bool = False, mcp_tools=None, temperature: float = 0.3, role: str = "agent"):
        self.model_name = model_name
        # role decides which set of .env credentials is read, see llm_config.py. The
        # official code has no such concept (it branches on a hardcoded model_name); this
        # is required by the integration layer and does not affect behaviour.
        self.role = role
        self.verbose = verbose
        self.mcp_tools = [] if mcp_tools is None else mcp_tools
        self.llm = None
        self.messages = []
        self.temperature = temperature
        self._initiate_llm()

    def _initiate_llm(self):
        config = get_llm_config(self.role, self.model_name)
        # Record the model id that actually takes effect: this is what the logs and
        # result file names use
        self.model_name = config.model
        self.llm = ChatOpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            model=config.model,
            temperature=self.temperature,
            # See item 2 of the module docstring: harness-level robustness plumbing,
            # shared by all arms.
            max_retries=3,
            timeout=300,
        )

    def _initiate_agent(self):
        # Exactly as the official code: a single create_react_agent, no custom graph and
        # no duplicate-tool interception.
        return create_react_agent(
            self.llm,
            self.mcp_tools,
        )

    @abstractmethod
    def load_system_prompt(self, system_prompt):
        """Initialize the system prompt"""

    @abstractmethod
    async def call(self, message: str) -> str:
        """Handle one turn of user messages and return the customer-service reply text"""
