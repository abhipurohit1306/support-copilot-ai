from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    session_id: str | None = Field(
        default=None,
        description="Conversation session identifier",
    )

    question: str = Field(
        ...,
        min_length=1,
        description="User's support question",
    )


class SourceInfo(BaseModel):

    title: str

    source: str

    score: float


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[SourceInfo]
    escalated: bool
    escalation_reason: str | None