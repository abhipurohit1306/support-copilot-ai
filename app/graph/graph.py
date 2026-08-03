from langgraph.graph import START, END, StateGraph
from app.graph.state import GraphState
from app.graph.nodes import (
    classify_intent,
    greeting_node,
    generate_node,
    confidence_node,
    respond_node,
    escalate_node,
)

from app.graph.router import (
    route_intent,
    route_confidence,
)

builder = StateGraph(GraphState)

builder.add_node("classify_intent", classify_intent)
builder.add_node("greeting_node", greeting_node)
builder.add_node("generate_node", generate_node)
builder.add_node("confidence_node", confidence_node)
builder.add_node("respond_node", respond_node)
builder.add_node("escalate_node", escalate_node)

builder.add_edge(START, "classify_intent",)
builder.add_conditional_edges("classify_intent", route_intent, )

builder.add_edge("generate_node", "confidence_node",)

builder.add_conditional_edges("confidence_node", route_confidence,)

builder.add_edge("greeting_node", END,)

builder.add_edge("respond_node", END,)

builder.add_edge("escalate_node", END, )

support_graph = builder.compile()