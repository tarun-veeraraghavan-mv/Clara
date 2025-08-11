from ..agent_state import AgentState
from api.models import ChatMessage, ChatSession
from langchain_core.messages import HumanMessage, AIMessage
from ..agents import agent_executor
from django.contrib.auth.models import User
from pydantic import BaseModel, Field
from ..utils.llm import llm, get_bot_settings
from ..utils.cache import get_cached_response, add_to_cache
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.gmail import GmailSendMessage
from ..utils.speech_to_text import speech_to_text

class TextClassiferOutputParser(BaseModel):
    """Boolean value to check whether a question is related to the Peak Performance Gym"""
    score: str = Field(
      description="Question is about gym? If yes -> 'Yes' if not -> 'No'"
    )

def text_classifier(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_template("""
You are a classifier deciding if a user’s question is about any of the following topics related to a gym:

1. Gym History & Founder
2. Operating hours
3. Membership Plans or membership details (e.g., user ID, membership status)
4. Fitness classes
5. Personal trainers
6. Facilities and Equipment
7. General gym-related queries including user account or membership info
8. Image analysis and questions about images.

If the question is about any of these topics, respond with 'Yes'. Otherwise, respond with 'No'.

Examples of membership-related questions include:
- "Can you get my current membership details?"
- "My user ID is 1"
- "What is my membership status?"
- "Tell me about my account"
- "Analyze this image or I have some questions about this image"
- "Can you freeze my membership?"

User's question: {user_input}
""")
    
    structured_llm = llm.with_structured_output(TextClassiferOutputParser)
    chain = prompt | structured_llm

    res = chain.invoke(state["user_input"])

    print(res)

    state["on_topic"] = res.score

    return state

def topic_router(state: AgentState) -> AgentState:
    on_topic = state["on_topic"]

    if on_topic.lower() == "yes":
        return "on_topic"
    elif on_topic.lower() == "no":
        return "off_topic"

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

def generate_response(state: AgentState) -> AgentState:
    messages = state["conversation_history"]

    bot_settings = state.get("bot_settings", {})
    greeting_message = bot_settings.get("greeting_message", "Hello! How can I help you today?")
    fallback_reply = bot_settings.get("fallback_reply", "I'm sorry, I don't understand. Can you please rephrase?")

    result = agent_executor.invoke({"user_input": state["user_input"], "history": messages, "greeting_message": greeting_message, "fallback_reply": fallback_reply})

    state["ai_output"] = result["output"]

    return state

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

  