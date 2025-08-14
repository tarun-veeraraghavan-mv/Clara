from django.db import models
from django.contrib.auth.models import User

class BotSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    greeting_message = models.TextField(default="Hello! How can I help you today?")
    fallback_reply = models.TextField(default="I'm sorry, I don't understand. Can you please rephrase?")
    max_conversation_history = models.IntegerField(default=10)
    confidence_threshold = models.FloatField(default=0.8)
