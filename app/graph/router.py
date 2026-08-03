from app.graph.state import GraphState


def route_intent(state: GraphState):
    if state["intent"] == "greeting":
        return "greeting_node"
    
    return "generate_node"


def route_confidence(state: GraphState):
    if state["confidence"] == "high":
        return "respond_node"
    
    return "escalate_node"