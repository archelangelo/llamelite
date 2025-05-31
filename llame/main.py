from fastapi import FastAPI
from pydantic import BaseModel
from llame.agent import run_agent

class Item(BaseModel):
    message: str

app = FastAPI()

@app.post("/chat")
async def chat(item: Item) -> dict[str, str]:
    """Endpoint to handle chat requests."""
    response = await run_agent(item.message)
    return {"response": response}