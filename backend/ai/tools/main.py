from langchain_core.tools import tool
from .inventory import check_user_inventory, refund_item, replacement_tool
from .faq import retriever_tool
from .membership import get_user_membership, freeze_membership
from .payment import initiate_upgrade_plan, confirm_upgrade_plan
from .image_analyzer import analyze_image

# === TOOL: Ask Clarifying Question ===
@tool
def ask_question(prompt: str = "What is the inventory ID?") -> str:
    """
    Returns a clarifying question to the user.
    """
    return prompt  # Return the prompt for frontend or agent to render

# Register tools
tools = [check_user_inventory, refund_item, replacement_tool, ask_question, retriever_tool, get_user_membership, initiate_upgrade_plan, confirm_upgrade_plan, analyze_image, freeze_membership]
