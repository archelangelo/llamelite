from fastapi import FastAPI
from pydantic import BaseModel
from llame.agent import run_agent, agent_lifespan

class Item(BaseModel):
    message: str

app = FastAPI(lifespan=agent_lifespan)

@app.post("/chat")
async def chat(item: Item) -> dict[str, str]:
    """Endpoint to handle chat requests."""
    response = await run_agent(item.message, {"configurable": {"thread_id": "1"}})
    return {"response": response}