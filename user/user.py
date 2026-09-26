from utils import LLM

class UserBased(LLM):
    def __init__(
        self,
        user_model: str,
        verbose: bool = False,
        mcp_tools=None,
        temperature: float = 0.3,
        inject: bool = False,
    ):
        if mcp_tools is None:
            mcp_tools = []
        super().__init__(
            model_name=user_model,
            verbose=verbose,
            mcp_tools=mcp_tools,
            temperature=temperature,
            inject=inject,
            role="user",
        )
        self.detail_messages = []
        self.user_model = super()._initiate_agent()
    
    
    def load_system_prompt(self, system_prompt):
        self.messages.append({"role": "system", "content": system_prompt})
    
    
    async def call(self, message:str) -> str:
        self.messages.append({"role": "user", "content": message})
        # No retry at this graph layer, for the same reason as AgentLangChain.call: the
        # actual model call happens in the agent_node of utils.LLM._initiate_agent, and
        # the retry is already added there.
        responses = await self.user_model.ainvoke(
            {
                "messages": self.messages
            },
            # Disable LangGraph event dump to avoid printing full prompts/messages.
            debug=False
        )
        self.detail_messages.append(responses["messages"])
        self.messages.append({"role": "assistant", "content": responses["messages"][-1].content})
        return responses["messages"][-1].content


from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
import json

class Think(BaseModel):
    '''Analyse the previous conversation history'''
    history:str = Field(...,description='The needs and emotions you have already expressed as the customer')
    solution:str = Field(...,description='The information and solutions customer service has already provided')
    stage:str = Field(...,description='Which stage the conversation has currently reached')

class Intent(BaseModel):
    '''Determine your current main intent from the previous conversation history'''
    emotion:str = Field(...,description='What your current emotional state is')
    demand:str = Field(...,description='What your current core need is')
    


class Evaluate(BaseModel):
    '''Evaluate the reasonableness of the reactions'''
    reaction:str = Field(...,description='The reaction that needs to be evaluated')
    consistency:str = Field(...,description='Analyse whether the reaction is consistent with your character setting')
    coherence:str = Field(...,description='Analyse whether each reaction is coherent with the current conversation progress')
    realism:str = Field(...,description='Analyse whether each reaction matches the natural reactions of a real customer')
    effectiveness:str = Field(...,description='Analyse whether the reaction helps the conversation continue and the problem get solved, avoiding a deadlock')
    

class Stop(BaseModel):
    '''Decide whether the conversation needs to stop'''
    reason:str = Field(...,description='The reason whether the conversation needs to stop; for example, all intents are complete and the conversation is nearing its end, in which case you must choose to stop the conversation.')
    stop:bool = Field(...,description='Whether the conversation needs to stop')

class Step(BaseModel):
    '''Decide whether to proactively steer the topic and move to the next intent'''
    count:int = Field(...,description='The number of times this intent has already been discussed')
    reason:str = Field(...,description='The reason whether to move to the next intent; for example 1. customer service cannot satisfy your current need 2. a deadlock has been reached 3. the same intent has been discussed for more than 1 turn, so you need to move to the next intent.')
    step:bool = Field(...,description='Whether to move to the next intent')


class Response(BaseModel):
    '''Internal thinking framework (to be executed before every reply); before generating each customer reply, please go through the following thinking steps first'''
    think:Think = Field(...,description='Analyse the previous conversation history')
    stop:Stop = Field(...,description='Decide whether the conversation needs to stop')
    step:Step = Field(...,description='Decide whether to proactively steer the topic and move to the next intent/topic')
    intent:Intent = Field(...,description='Determine your current main intent from the previous conversation history')
    reactions:List[str] = Field(...,description='Based on your own persona and background, combined with the content of think, stop, step and intent, generate several possible customer reactions')
    evaluates:List[Evaluate] = Field(...,description='Evaluate the reasonableness of each reaction one by one and give the corresponding reason')
    final_response:str = Field(...,description='Choose the reaction that best fits the current scenario according to the evaluation results, giving priority to what helps move the conversation forward')
    
    
class UserCoT(UserBased):
    def __init__(
        self,
        user_model: str,
        verbose: bool = False,
        mcp_tools=None,
        temperature: float = 0.3,
        inject: bool = False,
    ):
        super().__init__(
            user_model=user_model,
            verbose=verbose,
            mcp_tools=mcp_tools,
            temperature=temperature,
            inject=inject,
        )
        self.parser = PydanticOutputParser(pydantic_object=Response)
        self.prompt_template = PromptTemplate(
            template="""
# This is the customer service reply:
{solution}

# This is your background information: 
{character}

# This is the conversation history:
{history}

# Output format:
{format_instructions}   
            """,
            input_variables=["solution", "character", "history"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            }
        )
    
    def load_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt
        
    async def call(self, message:str) -> str:
        prompt = self.prompt_template.format_prompt(
            solution=message,
            character = self.system_prompt,
            history = self.messages,
        )
        # No retry at this graph layer, for the same reason as AgentLangChain.call: the
        # actual model call happens in the agent_node of utils.LLM._initiate_agent, and
        # the retry is already added there.
        responses = await self.user_model.ainvoke(
            {
                "messages": {
                    "role": "user",
                    "content": prompt.to_string()
                }
            },
            # Disable LangGraph event dump to avoid printing full prompts/messages.
            debug=False
        )
        self.detail_messages.append(responses["messages"])
        response = self.parser.parse(responses["messages"][-1].content)
        final_response = response.final_response
        stop = response.stop.stop
        if stop :
            final_response = '###STOP###'
        
        self.messages.append(f"Customer service reply: {message}")
        self.messages.append(f"Your reply: {final_response}")
        return final_response


class UserHuman(LLM):
    def __init__(
        self,
        user_model: str,
        verbose: bool = False,
        mcp_tools=None,
        inject: bool = False,
    ):
        if mcp_tools is None:
            mcp_tools = []
        super().__init__(
            model_name=user_model,
            verbose=verbose,
            mcp_tools=mcp_tools,
            inject=inject,
            role="user",
        )
        self.detail_messages = []
        self.user_model = super()._initiate_agent()
    
    def load_system_prompt(self, system_prompt):
        self.messages.append({"role": "system", "content": system_prompt})
    
    
    async def call(self, message:str) -> str:
        self.messages.append({"role": "user", "content": message})
        response = input("Enter your (customer) reply (quit to stop):\t")
        response = response.strip()
        while not response:
            print("The reply cannot be empty, please enter it again:")
            response = input("Enter your (customer) reply (quit to stop):\t")
            response = response.strip()
        self.messages.append({"role": "assistant", "content": response})
        self.detail_messages.append([self.messages[-1]])
        if response == 'quit':
            response = '###STOP###'
        return response
