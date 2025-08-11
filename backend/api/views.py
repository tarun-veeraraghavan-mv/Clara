import os
from django.core.files.storage import default_storage
from django.db.models import Avg
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import requests
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from ai.utils.vector_store import vectorstore
from ai.graphs.customer_service_agent import run_ai_pipeline
from ai.graphs.customer_feedback_analyzer import run_customer_feedback_pipeline

from .models import ChatSession, ChatMessage, MembershipPlan, BotSettings, CustomerFeedback
from .serializers import MembershipPlanSerializer, ChatSessionSerializer, ChatMessageSerializer, BotSettingsSerializer

import whisper

load_dotenv()

model = whisper.load_model("base")

@api_view(["GET"])
def simple_hello(request):
    return Response("ok")

@api_view(["POST"])
def simple_ai(request):
    user_input = request.data.get("user_input")
    user_id = request.data.get("user_id")
    session_id = request.data.get("session_id")
    audio_file = request.FILES.get('audio_file') # Get audio file

    audio_file_path = None
    if audio_file:
        # Define the maximum allowed file size (25MB)
        MAX_FILE_SIZE = 25 * 1024 * 1024 # 25 MB in bytes

        # Save the audio file temporarily
        file_name = default_storage.save(audio_file.name, audio_file)
        audio_file_path = os.path.join(default_storage.location, file_name)

        # Check file size
        if os.path.getsize(audio_file_path) > MAX_FILE_SIZE:
            os.remove(audio_file_path) # Clean up the large file
            return Response({"error": "Audio file too large. Maximum size is 25MB."}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        try:
            # Transcribe the audio and set user_input
            transcript = transcribe_speech(audio_file_path)
            user_input = transcript.text
        except Exception as e:
            # Handle transcription error
            return Response({"error": f"Audio transcription failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Clean up the temporary file
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

    try:
        session = ChatSession.objects.get(id=session_id)
        user = User.objects.get(id=user_id)
    except (ChatSession.DoesNotExist, User.DoesNotExist):
        return Response({"error": "Session or User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Save user's message (original input)
    ChatMessage.objects.create(
        sender="user",
        content=user_input if user_input else "Audio input", # Store "Audio input" or actual text
        session=session,
        user=user,
        response_time=None
    )

    if session.max_conversation_history <= 0:
        response_content = "You have reached the limit of this conversation. Upgrade to continue this conversation or enter a new conversation"
        ChatMessage.objects.create(
            sender="ai",
            content=response_content,
            session=session,
            user=User.objects.get(id=user_id) 
        )
        return Response({"result": {"ai_output": response_content}}) 

    session.max_conversation_history -= 1
    session.save()

    # Pass audio_file_path if present, otherwise user_input
    result = run_ai_pipeline(
        user_input=user_input,
        user_id=user_id,
        session_id=session_id,
        audio_file_path=audio_file_path # Pass audio file path
    )
    return Response({"result": result})

@api_view(["POST"])
def load_faq(request):
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)  

    file_path = os.path.join(upload_dir, file.name)

    # Save the uploaded file to disk
    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # Load and split the text file
    loader = TextLoader(file_path)
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=300, chunk_overlap=100)
    docs = loader.load_and_split(text_splitter=text_splitter)

    # Vectorize and store
    vectorstore.add_documents(documents=docs)

    return Response({"message": f"{file.name} uploaded and processed successfully!"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_session(request):
    user_id = request.data.get("user_id")
    user = User.objects.get(id=user_id)
    
    # Fetch bot settings to get max_conversation_history
    try:
        bot_settings = BotSettings.objects.first()
        max_convo_history = bot_settings.max_conversation_history if bot_settings else 10 # Default to 10 if no settings
    except Exception:
        max_convo_history = 10

    session = ChatSession.objects.create(user=user, max_conversation_history=max_convo_history)

    # Fetch greeting message from BotSettings
    try:
        bot_settings = BotSettings.objects.first()
        greeting_message = bot_settings.greeting_message if bot_settings else "Hello! How can I assist you today?"
    except Exception:
        greeting_message = "Hello! How can I assist you today?"

    # Create an initial chat message with the greeting
    ChatMessage.objects.create(
        sender="ai",
        content=greeting_message,
        session=session,
        user=user,
        response_time=None # Explicitly set to None for initial greeting
    )

    return Response({"session_id": session.id})

@api_view(["POST"])
def analyse_customer_feedback(request):
    customer_feedback = request.data.get("customer_feedback")
    user_id = request.data.get("user_id")
    session_id = request.data.get("session_id")

    result = run_customer_feedback_pipeline(user_id=user_id, session_id=session_id, customer_feedback=customer_feedback)

    return Response({"result": result})

@api_view(["GET"])
def get_all_plans(request):
    plans = MembershipPlan.objects.all()
    serializer = MembershipPlanSerializer(plans, many=True)
    return Response({"plans": serializer.data})

@api_view(["GET"])
def get_user_sessions(request):
    user_id = request.query_params.get("user_id")
    if not user_id:
        return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    sessions = ChatSession.objects.filter(user=user).order_by('-timestamp')
    serializer = ChatSessionSerializer(sessions, many=True)
    return Response({"sessions": serializer.data})

@api_view(["GET"])
def get_session_messages(request, session_id):
    try:
        session = ChatSession.objects.get(id=session_id)
    except ChatSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    serializer = ChatMessageSerializer(messages, many=True)
    return Response({"messages": serializer.data})

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

@api_view(["POST"])
def create_bot_settings(request):
    serializer = BotSettingsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        # Transcribe the audio
        transcript = model.transcribe(audio_file_path)
        return Response({"transcribed_text": transcript["text"]}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Speech to text failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        # Clean up the temporary file
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
