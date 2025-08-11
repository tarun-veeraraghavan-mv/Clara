from django.urls import path
from .views.bot_settings import create_bot_settings, get_current_bot_settings 
from .views.customer_service_agent import create_session, get_session_messages, get_user_sessions, load_faq, simple_ai
from .views.customer_feedback import analyse_customer_feedback
from .views.analytics import get_analytics
from .views.plans import get_all_plans

urlpatterns = [
    path("ai/", simple_ai, name="simple_ai"),
    path("load-faq/", load_faq, name="load_faq"),
    path("create-session/", create_session, name="create_session"),
    path("analyze-feedback/", analyse_customer_feedback, name="analyze_customer_feedback"),
    path("plans/", get_all_plans, name="get_all_plans"),
    path("user-sessions/", get_user_sessions, name="get_user_sessions"),
    path("session-messages/<int:session_id>/", get_session_messages, name="get_session_messages"),
    path("bot-settings/", create_bot_settings, name="create_bot_settings"),
    path("analytics/", get_analytics, name="get_analytics"),
    path("bot-settings/current/", get_current_bot_settings, name="get_current_bot_settings"), 
]