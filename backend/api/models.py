from django.db import models
from django.contrib.auth.models import User


class BotSettings(models.Model):
    greeting_message = models.TextField(default="Hello! How can I help you today?")
    fallback_reply = models.TextField(default="I'm sorry, I don't understand. Can you please rephrase?")
    max_conversation_history = models.IntegerField(default=10)
    confidence_threshold = models.FloatField(default=0.8)

class MembershipPlan(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('day_pass', 'Day Pass'),
    ]

    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.JSONField(default=list)

class UserMembership(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)

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

class CustomerFeedback(models.Model):
    rating = models.IntegerField()
    review = models.TextField()
    relevancy = models.BooleanField() 
    timestamp = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)