from ..agent_state import AgentState
from api.models.chat import ChatMessage, ChatSession # Updated import
from langchain_core.messages import HumanMessage, AIMessage
from ..agents import agent_executor
from django.contrib.auth.models import User
from pydantic import BaseModel, Field
from ..utils.llm import llm, get_bot_settings
from ..utils.cache import get_cached_response, add_to_cache
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.gmail import GmailSendMessage
from ..utils.speech_to_text import speech_to_text



def fetch_previous_messages(state: AgentState) -> AgentState:
    messages = ChatMessage.objects.filter(
        user_id=state["user_id"],
        session_id=state["session_id"]
    ).order_by("timestamp")  

    state["conversation_history"] = []

    for msg in messages:
        if msg.sender == "user":
            state["conversation_history"].append(HumanMessage(content=msg.content))
        elif msg.sender == "ai":
            state["conversation_history"].append(AIMessage(content=msg.content))

    return state

def check_cache(state: AgentState) -> AgentState:
    cached_response = get_cached_response(state["user_input"])
    if cached_response:
        state["cached_response"] = cached_response
        state["cache_hit"] = True
    else:
        state["cache_hit"] = False
    return state

def set_cached_response_as_output(state: AgentState) -> AgentState:
    state["ai_output"] = state["cached_response"]
    return state

def cache_response(state: AgentState) -> AgentState:
    add_to_cache(state["user_input"], state["ai_output"])
    return state

def agent_orchestrator(state: AgentState) -> dict: # Return a dict of updates
    messages = state["conversation_history"]

    bot_settings = state.get("bot_settings", {})
    fallback_reply = bot_settings.get("fallback_reply", "I'm sorry, I don't understand. Can you please rephrase?")

    result = agent_executor.invoke({"user_input": state["user_input"], "history": messages, "greeting_message": bot_settings.get("greeting_message"), "fallback_reply": fallback_reply})

    ai_output = result["output"]

    # Determine the routing decision
    route_decision = "continue"
    if ai_output == fallback_reply:
        route_decision = "off_topic"

    # Return a dictionary of updates to the state
    return {"ai_output": ai_output, "route_decision": route_decision}

def off_topic(state: AgentState) -> AgentState:
    user = User.objects.get(id=state["user_id"])
    session = ChatSession.objects.get(id=state["session_id"])

    bot_settings = get_bot_settings()
    state["ai_output"] = bot_settings.fallback_reply

    return state

def speech_to_text_node(state: AgentState) -> AgentState:
    audio_file_path = state.get("audio_file_path")
    if audio_file_path:
        try:
            transcript = speech_to_text(audio_file_path) # Assuming speech_to_text takes a path
            state["user_input"] = transcript.text # Assuming transcript has a .text attribute
        except Exception as e:
            print(f"Error during speech to text conversion: {e}")
            state["user_input"] = "Error: Could not process audio." # Fallback
    return state