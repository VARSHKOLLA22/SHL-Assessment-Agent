from fastapi import FastAPI
from models.schemas import ChatRequest, ChatResponse

from services.agent import SHLAgent

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0"
)

agent = SHLAgent()


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return agent.reply(request.messages)