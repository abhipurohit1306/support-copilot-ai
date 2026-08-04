from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.graph.graph import support_graph

router = APIRouter(tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    state = support_graph.invoke(
        {
            "question": request.question,
        }
    )

    return ChatResponse(
        answer=state["response"]
    )