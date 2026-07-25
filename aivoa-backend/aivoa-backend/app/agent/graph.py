from langgraph.graph import StateGraph, END

from app.agent.state import ComplaintGraphState
from app.agent.nodes import (
    extract_fields,
    check_completeness,
    classify_risk,
    detect_duplicates,
    recommend_root_cause,
    recommend_capa,
    summarize_complaint,
)


def build_graph():
    graph = StateGraph(ComplaintGraphState)

    # Core path — always runs
    graph.add_node("extract_fields", extract_fields)
    graph.add_node("check_completeness", check_completeness)
    graph.add_node("classify_risk", classify_risk)

    # Bonus branches — optional, but wired in so they're easy to toggle
    graph.add_node("detect_duplicates", detect_duplicates)
    graph.add_node("recommend_root_cause", recommend_root_cause)
    graph.add_node("recommend_capa", recommend_capa)
    graph.add_node("summarize_complaint", summarize_complaint)

    graph.set_entry_point("extract_fields")
    graph.add_edge("extract_fields", "check_completeness")
    graph.add_edge("check_completeness", "classify_risk")
    graph.add_edge("classify_risk", "detect_duplicates")
    graph.add_edge("detect_duplicates", "recommend_root_cause")
    graph.add_edge("recommend_root_cause", "recommend_capa")
    graph.add_edge("recommend_capa", "summarize_complaint")
    graph.add_edge("summarize_complaint", END)

    return graph.compile()


# Compiled once at import time, reused across requests
complaint_graph = build_graph()
