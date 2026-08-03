from typing import TypedDict

class GraphState(TypedDict):

    question: str
    intent: str
    answer: str
    best_score: float | None
    response: str
    confidence: str