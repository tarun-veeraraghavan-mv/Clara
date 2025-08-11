from ..models.membership import MembershipPlan # Updated import
from ..serializers import MembershipPlanSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def get_all_plans(request):
    plans = MembershipPlan.objects.all()
    serializer = MembershipPlanSerializer(plans, many=True)
    return Response({"plans": serializer.data})