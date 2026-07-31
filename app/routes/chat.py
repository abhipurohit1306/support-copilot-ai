from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services import chatbot

router = APIRouter(tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    answer = chatbot.ask(request.question)

    return ChatResponse(
        answer=answer
    )