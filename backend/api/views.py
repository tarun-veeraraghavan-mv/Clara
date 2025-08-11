import os
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import requests
from dotenv import load_dotenv

from ai.graphs.customer_feedback_analyzer import run_customer_feedback_pipeline



import whisper

load_dotenv()

model = whisper.load_model("base")



@api_view(["POST"])
def run_huggingface_inference(request):
    text_input = request.data.get("text_input")

    if not text_input:
        return Response({"error": "text_input is required"}, status=status.HTTP_400_BAD_REQUEST)

    API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text_input})
        response.raise_for_status()  # Raise an exception for HTTP errors
        return Response(response.json(), status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": f"Hugging Face API request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from ai.utils.speech_to_text import speech_to_text as transcribe_speech # Import the utility function

@api_view(["POST"])
def speech_to_text(request):
    if "file" not in request.FILES:
        return Response({"error": "No audio file found"}, status=status.HTTP_400_BAD_REQUEST)

    audio_file = request.FILES.data.get("file")
    audio_path = "uploaded.wav"
    with open(audio_path, "wb+") as destination:
        for chunk in audio_file.chunks():
            destination.write(chunk)

    audio_file_path = audio_path

    try:
        transcript = model.transcribe(audio_file_path)
        return Response({"transcribed_text": transcript["text"]}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Speech to text failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

