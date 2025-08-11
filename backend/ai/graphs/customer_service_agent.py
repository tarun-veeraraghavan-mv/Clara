import time
from langgraph.graph import StateGraph, START, END

from ..agent_state import AgentState
from ..nodes.customer_service_agent import (
    text_classifier, 
    fetch_previous_messages, 
    generate_response, 
    topic_router, 
    off_topic,
    check_cache,
    set_cached_response_as_output,
    cache_response,
    speech_to_text_node
)
from ..nodes.sentiment_analyzer import sentiment_analyzer
from ..utils.llm import get_bot_settings
from api.models.chat import ChatMessage, ChatSession # Updated import
from django.contrib.auth.models import User

def cache_router(state: AgentState) -> str:
    if state["cache_hit"]:
        return "hit"
    return "miss"

def fetch_bot_settings_node(state: AgentState) -> AgentState:
    settings = get_bot_settings()
    state["bot_settings"] = {
        "greeting_message": settings.greeting_message,
        "fallback_reply": settings.fallback_reply,
        "max_conversation_history": settings.max_conversation_history,
        "confidence_threshold": settings.confidence_threshold,
    }
    return state

def record_end_time(state: AgentState) -> AgentState:
    user = User.objects.get(id=state["user_id"])
    session = ChatSession.objects.get(id=state["session_id"])

    end_time = time.time()
    start_time = state.get("start_time", end_time) 
    response_time = end_time - start_time
    state["response_time"] = response_time

    ChatMessage.objects.create(
        sender="ai", 
        content=state["ai_output"], 
        session=session, 
        user=user, 
        response_time=response_time)

    return state

graph = StateGraph(AgentState)

graph.add_node("fetch_bot_settings", fetch_bot_settings_node)
graph.add_node("text_classifier", text_classifier)
graph.add_node("sentiment_analyzer", sentiment_analyzer)
graph.add_node("topic_router", lambda state: state)
graph.add_node("check_cache", check_cache)
graph.add_node("fetch_previous_messages", fetch_previous_messages)
graph.add_node("generate_response", generate_response)
graph.add_node("set_cached_response_as_output", set_cached_response_as_output)
graph.add_node("cache_response", cache_response)
graph.add_node("off_topic", off_topic)
graph.add_node("record_end_time", record_end_time)

graph.add_edge(START, "fetch_bot_settings")
graph.add_edge("fetch_bot_settings", "text_classifier")
graph.add_edge("text_classifier", "sentiment_analyzer")
graph.add_edge("sentiment_analyzer", "topic_router")
graph.add_conditional_edges("topic_router", topic_router, {
    "on_topic": "check_cache",
    "off_topic": "off_topic"
})

graph.add_conditional_edges("check_cache", cache_router, {
    "hit": "set_cached_response_as_output",
    "miss": "fetch_previous_messages"
})

graph.add_edge("fetch_previous_messages", "generate_response")
graph.add_edge("generate_response", "cache_response")
graph.add_edge("set_cached_response_as_output", "record_end_time")
graph.add_edge("cache_response", "record_end_time")
graph.add_edge("off_topic", "record_end_time")
graph.add_edge("record_end_time", END)

app = graph.compile()

def run_ai_pipeline(user_input: str, user_id: int, session_id: int, audio_file_path: str = None):
    start_time = time.time() 
    result = app.invoke({
        "user_input": user_input,
        "user_id": user_id,
        "session_id": session_id,
        "cache_hit": False,
        "cached_response": None,
        "start_time": start_time,
        "audio_file_path": audio_file_path
    })
    return result
