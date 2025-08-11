from rest_framework.decorators import api_view
from ..models.chat import ChatMessage # Updated import
from ..models.feedback import CustomerFeedback # Updated import
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import status

@api_view(["GET"])
def get_analytics(request):
    total_chat_messages = ChatMessage.objects.count()

    avg_response_time_ai = ChatMessage.objects.filter(sender="ai", response_time__isnull=False).aggregate(Avg('response_time'))['response_time__avg']
    if avg_response_time_ai is None:
        avg_response_time_ai = 0.0

    avg_user_satisfaction = CustomerFeedback.objects.aggregate(Avg('rating'))['rating__avg']
    if avg_user_satisfaction is None:
        avg_user_satisfaction = 0.0

    analytics_data = {
        "total_chat_messages": total_chat_messages,
        "avg_response_time_ai": round(avg_response_time_ai, 2),
        "avg_user_satisfaction": round(avg_user_satisfaction, 2),
    }

    return Response(analytics_data, status=status.HTTP_200_OK)
