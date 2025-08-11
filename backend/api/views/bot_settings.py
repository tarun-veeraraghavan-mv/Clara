from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.bot_settings import BotSettings # Updated import
from ..serializers import BotSettingsSerializer

@api_view(["POST"])
def create_bot_settings(request):
    serializer = BotSettingsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_current_bot_settings(request):
    try:
        settings = BotSettings.objects.first()
        if settings:
            serializer = BotSettingsSerializer(settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If no settings exist, return a default or an empty response
            return Response({"detail": "Bot settings not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)