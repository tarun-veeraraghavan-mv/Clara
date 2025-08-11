from django.db import models
from django.contrib.auth.models import User
from .chat import ChatSession # Import ChatSession from the new chat.py

class CustomerFeedback(models.Model):
    rating = models.IntegerField()
    review = models.TextField()
    relevancy = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
