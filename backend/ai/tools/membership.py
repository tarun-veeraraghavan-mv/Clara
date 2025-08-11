from langchain_core.tools import tool
from api.models.membership import UserMembership # Updated import

@tool
def get_user_membership(user_id: int):
    """
    Fetches the user's current membership plan based on the user ID.
    """
    if not user_id:
        raise ValueError("User ID is required.")

    try:
        user_membership = UserMembership.objects.get(user_id=user_id, active=True)
        return {
            "plan_name": user_membership.plan.name,
            "features": user_membership.plan.features,
            "start_date": user_membership.start_date.isoformat(),
            "end_date": user_membership.end_date.isoformat() if user_membership.end_date else None
        }
    except UserMembership.DoesNotExist:
        raise ValueError(f"No active membership found for user with ID: {user_id}")

@tool
def freeze_membership(user_id: int):
    """
    Freezes the user's current membership plan.
    """
    if not user_id:
        raise ValueError("User ID is required.")
    
    user_membership = UserMembership.objects.get(user_id=user_id)

    if not user_membership:
        raise ValueError(f"No membership found for user with ID: {user_id}")

    if user_membership.active == False:
        raise PermissionError(f"Your membership is already freezed, please unfreeze first")
    
    user_membership.active = False
    user_membership.save()

    return f"Your membership has been freezed"