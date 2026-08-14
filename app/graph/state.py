from typing import TypedDict

class GraphState(TypedDict):

    question: str
    intent: str
    session_id: str
    history: list[dict]
    answer: str
    sources: list[dict]
    best_score: float | None
    response: str
    confidence: str
    escalation_reason: str | None
    escalation_context: dict | None