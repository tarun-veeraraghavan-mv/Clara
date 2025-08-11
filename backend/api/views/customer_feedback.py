from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ai.graphs.customer_feedback_analyzer import run_customer_feedback_pipeline

@api_view(["POST"])
def analyse_customer_feedback(request):
    customer_feedback = request.data.get("customer_feedback")
    user_id = request.data.get("user_id")
    session_id = request.data.get("session_id")

    result = run_customer_feedback_pipeline(user_id=user_id, session_id=session_id, customer_feedback=customer_feedback)

    return Response({"result": result})