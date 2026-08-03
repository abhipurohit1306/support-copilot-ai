from app.graph.state import GraphState
from app.logger import logger
from app.services import chatbot
from app.config import CONFIDENCE_THRESHOLD


def classify_intent(state: GraphState):
    question = (
        state["question"]
        .lower()
        .strip()
    )
    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    ]

    if question in greetings:
        state["intent"] = "greeting"

    else:
        state["intent"] = "support"

    logger.info(
        "Detected intent: %s",
        state["intent"]
    )

    return state


def greeting_node(state: GraphState):

    state["response"] = (
        "Hello! 👋\n\n"
        "I'm Support Copilot AI.\n"
        "How can I help you today?"
    )

    logger.info("Greeting response generated.")

    return state


def generate_node(state: GraphState):
    result = chatbot.ask(
        state["question"]
    )

    state["answer"] = result["answer"]

    state["best_score"] = result["best_score"]

    logger.info(
        "Answer generated. Best Score: %.4f",
        state["best_score"],
    )

    return state

def confidence_node(state: GraphState):
    best_score = state["best_score"]
    if best_score <= CONFIDENCE_THRESHOLD:
        state["confidence"] = "high"
    else:
        state["confidence"] = "low"

    logger.info(
        "Confidence: %s (%.4f)",
        state["confidence"],
        best_score,
    )
    return state

def respond_node(state: GraphState):
    state["response"] = state["answer"]
    logger.info(
        "Returning AI response."
    )
    return state

def escalate_node(state: GraphState):
    state["response"] = (
        "I'm not confident enough to answer your question accurately.\n\n"
        "I've forwarded your request to a human support agent."
    )
    logger.warning(
        "Low confidence detected. Escalating to human support."
    )
    return state