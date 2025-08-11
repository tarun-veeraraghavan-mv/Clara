from langchain_core.tools import tool
from api.models.membership import UserMembership, MembershipPlan # Updated import
from django.utils import timezone

@tool
def initiate_upgrade_plan(user_id: int, new_plan_name: str):
    """
    Initiates the process of upgrading a user's membership plan.
    """
    try:
        user_membership = UserMembership.objects.get(user_id=user_id, active=True)
        new_plan = MembershipPlan.objects.get(name__iexact=new_plan_name)

        if user_membership.plan.name == new_plan.name:
            return f"You are already subscribed to the {new_plan.name} plan."

        return f"Are you sure you want to upgrade to the {new_plan.name} plan for ${new_plan.price}/month? Your current plan will be deactivated. Reply with 'YES, I WANT TO UPGRADE'"

    except UserMembership.DoesNotExist:
        return f"No active membership found for user with ID: {user_id}"
    except MembershipPlan.DoesNotExist:
        return f"Plan '{new_plan_name}' not found."

@tool
def confirm_upgrade_plan(user_id: int):
    """
    Confirms and executes the membership plan upgrade.
    """
    try:
        user_membership = UserMembership.objects.get(user_id=user_id, active=True)
        current_plan_name = user_membership.plan.name
        if current_plan_name == 'Basic':
            new_plan_name = 'Standard'
        elif current_plan_name == 'Standard':
            new_plan_name = 'Premium'
        else:
            return "No further upgrades available."

        new_plan = MembershipPlan.objects.get(name__iexact=new_plan_name)

        user_membership.active = False
        user_membership.end_date = timezone.now()
        user_membership.save()

        UserMembership.objects.create(user=user_membership.user, plan=new_plan)

        return f"Successfully upgraded to the {new_plan.name} plan."

    except UserMembership.DoesNotExist:
        return f"No active membership found for user with ID: {user_id}"