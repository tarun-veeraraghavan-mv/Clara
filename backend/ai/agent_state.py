from typing import TypedDict, Annotated, Optional
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    session_id: int
    user_id: int
    user_input: str
    ai_output: str
    on_topic: str
    conversation_history: list[BaseMessage]
    cache_hit: bool
    cached_response: Optional[str]
    conversation_over: bool
    summary: Optional[str]
    sentiment: Optional[str]
    start_time: float 
    response_time: float

class CustomerFeedbackAnalysisState(TypedDict):
    user_id: int
    session_id: int
    customer_feedback: Annotated[dict, "This dictionary is used to store a customer feedback with 'rating' field which goes from 1 - 5 and the 'review' text block"]
    analyzed_feedback: Annotated[dict, "Analyzed customer feedback"]
    


