from pydantic import Field, BaseModel
from django.contrib.auth.models import User

from ..agent_state import CustomerFeedbackAnalysisState
from ..utils.llm import llm
from ..prompts import analyze_customer_feedback_prompt
from api.models.feedback import CustomerFeedback # Updated import
from api.models.chat import ChatSession # Updated import

class CustomerFeedbackOutputParser(BaseModel):
    rating: int = Field(description="The rating the user gave out of 5 in integer type")
    review: str = Field(description="A quick summary of the user's feedback. Should include the issue, what the user wanted and a fix in less than 230 charecters")
    relevancy: bool = Field(description="A boolean value of whether the user's review is related to improving/feedback/comment on the review. If yes -> true. If something random -> false")

def format_customer_review(state: CustomerFeedbackAnalysisState) -> CustomerFeedbackAnalysisState:
    structured_llm = llm.with_structured_output(CustomerFeedbackOutputParser)

    chain = analyze_customer_feedback_prompt | structured_llm

    res = chain.invoke({
        "rating": state['customer_feedback']['rating'], 
        "review": state['customer_feedback']['review']})
    
    state["analyzed_feedback"] = res.dict()

    return state

def save_analyzed_feedback(state: CustomerFeedbackAnalysisState) -> CustomerFeedbackAnalysisState:
    session = ChatSession.objects.get(id=state["session_id"])
    user = User.objects.get(id=state["user_id"])

    CustomerFeedback.objects.create(
        rating=state["analyzed_feedback"]["rating"],
        review=state["analyzed_feedback"]["review"],
        relevancy=state["analyzed_feedback"]["relevancy"],
        session=session,
        user=user
    )

    return state