from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.simple_hello, name="simple_hello"),
    path("ai/", views.simple_ai, name="simple_ai"),
    path("load-faq/", views.load_faq, name="load_faq"),
    path("create-session/", views.create_session, name="create_session"),
    path("analyze-feedback/", views.analyse_customer_feedback, name="analyze_customer_feedback"),
    path("plans/", views.get_all_plans, name="get_all_plans"),
    path("user-sessions/", views.get_user_sessions, name="get_user_sessions"),
    path("session-messages/<int:session_id>/", views.get_session_messages, name="get_session_messages"),
    path("run-huggingface-inference/", views.run_huggingface_inference, name="run_huggingface_inference"),
    path("bot-settings/", views.create_bot_settings, name="create_bot_settings"),
    path("analytics/", views.get_analytics, name="get_analytics"),
    path("speech-to-text/", views.speech_to_text, name="speech_to_text"),
]