from langchain_openai import ChatOpenAI
from api.models.bot_settings import BotSettings # Updated import
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
  )

def get_bot_settings():
    try:
        settings = BotSettings.objects.first()
        if not settings:
            # Create default settings if none exist
            settings = BotSettings.objects.create(
                greeting_message="Hello! How can I help you today?",
                fallback_reply="I'm sorry, I don't understand. Can you please rephrase?",
                max_conversation_history=10,
                confidence_threshold=0.8
            )
        return settings
    except Exception as e:
        print(f"Error fetching bot settings: {e}")
        # Return default values in case of an error
        return BotSettings(
            greeting_message="Hello! How can I help you today?",
            fallback_reply="I'm sorry, I don't understand. Can you please rephrase?",
            max_conversation_history=10,
            confidence_threshold=0.8
        )
