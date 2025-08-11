from langgraph.graph import StateGraph

from ..agent_state import CustomerFeedbackAnalysisState
from ..nodes.customer_feedback_analyzer import format_customer_review, save_analyzed_feedback

graph = StateGraph(CustomerFeedbackAnalysisState)

graph.add_node("format_review", format_customer_review)
graph.add_node("save_analyzed_feedback", save_analyzed_feedback)

graph.set_entry_point("format_review")
graph.add_edge("format_review", "save_analyzed_feedback")
graph.set_finish_point("save_analyzed_feedback")

app = graph.compile()

def run_customer_feedback_pipeline(user_id: int, session_id: int, customer_feedback: dict):  
    result = app.invoke({"user_id": user_id, "session_id": session_id, "customer_feedback": customer_feedback})
    return result