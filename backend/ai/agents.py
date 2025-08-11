from langchain.agents import create_tool_calling_agent, AgentExecutor
from .utils.llm import llm
from .tools.main import tools
from .prompts import agent_prompt

agent = create_tool_calling_agent(
    llm=llm,
    prompt=agent_prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)
