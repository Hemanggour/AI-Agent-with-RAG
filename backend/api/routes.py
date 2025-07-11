from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.agent.graph import get_langgraph

router = APIRouter()
graph = get_langgraph()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    try:
        result = graph.invoke({
            "message": payload.message,
            "response": None,
            "context": None
        })
        return {"response": result["response"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
