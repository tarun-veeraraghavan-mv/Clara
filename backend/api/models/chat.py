from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    max_conversation_history = models.IntegerField(default=10)

class ChatMessage(models.Model):
    sender_choices = [
        ('user', 'USER'),
        ('ai', 'AI')
    ]

    sender = models.CharField(
        max_length=10,
        choices=sender_choices,
        default='user'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    response_time = models.FloatField(null=True, blank=True)
