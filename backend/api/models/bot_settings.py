from django.db import models

class BotSettings(models.Model):
    greeting_message = models.TextField(default="Hello! How can I help you today?")
    fallback_reply = models.TextField(default="I'm sorry, I don't understand. Can you please rephrase?")
    max_conversation_history = models.IntegerField(default=10)
    confidence_threshold = models.FloatField(default=0.8)
