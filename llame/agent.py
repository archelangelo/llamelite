# %%
from contextlib import asynccontextmanager
from fastapi import FastAPI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch

DB_URL = "postgresql://llame:llamapass@postgres:5432/llamedb"
MODEL_NAME = "anthropic.claude-3-5-sonnet-20240620-v1:0"
MODEL_PROVIDER = "bedrock_converse"

agent = None  # Will be set up asynchronously


@asynccontextmanager
async def agent_lifespan(app: FastAPI):
    global agent
    llm = init_chat_model(
        MODEL_NAME,
        model_provider=MODEL_PROVIDER,
    )
    search_tool = TavilySearch(max_results=5)
    tools = [search_tool]
    # If AsyncPostgresSaver needs async setup, do it here
    # checkpointer = await AsyncPostgresSaver(DB_URL).setup()

    async with (
        AsyncPostgresSaver.from_conn_string(DB_URL) as checkpointer,
        AsyncPostgresStore.from_conn_string(DB_URL) as store,
        ):
        await checkpointer.setup()
        await store.setup()
        agent = create_react_agent(
            llm,
            tools=tools,
            checkpointer=checkpointer,
            store=store,
        )
        yield


async def run_agent(query: str, config: dict) -> str:
    if agent is None:
        raise RuntimeError("Agent not initialized. Call setup_agent() first.")
    response = await agent.ainvoke({"messages": [{"role": "user", "content": query}]}, config=config)
    return response.get("messages", [{}])[-1].content