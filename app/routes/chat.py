from uuid import uuid4

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.graph.graph import support_graph
from app.memory import conversation_memory


router = APIRouter(tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest):

    session_id = request.session_id

    if not session_id:

        session_id = str(uuid4())

    history = conversation_memory.get_history(
        session_id
    )

    state = support_graph.invoke(
        {
            "question": request.question,
            "session_id": session_id,
            "history": history,
        }
    )

    conversation_memory.add_message(
        session_id=session_id,
        role="user",
        content=request.question,
    )

    conversation_memory.add_message(
        session_id=session_id,
        role="assistant",
        content=state["response"],
    )

    return ChatResponse(
        session_id=session_id,
        answer=state["response"],
        sources=state["sources"],
    )