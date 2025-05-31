# %%
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from langchain.chat_models import init_chat_model

from langchain_tavily import TavilySearch

# from IPython.display import Image, display

# Creating a LLM node
llm = init_chat_model(
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    model_provider="bedrock_converse",
)

# Creating tools
search_tool = TavilySearch(max_results=5)

tools = [search_tool]

agent = create_react_agent(
    llm,
    tools=tools,
    checkpointer=InMemorySaver(),
)

# display(Image(agent.get_graph().draw_mermaid_png()))
# %%

async def run_agent(query: str, config: dict) -> str:
    """Run the agent with the given query."""
    response = await agent.ainvoke({"messages": [{"role": "user", "content": query}]}, config=config)
    return response.get("messages", [{}])[-1].content