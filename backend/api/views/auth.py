from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ..serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

# user views
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user=user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@api_view(["POST"])
def register_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"error": "Username, email, and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, email=email, password=password)
    tokens = get_tokens_for_user(user=user)

    serializer = UserSerializer(user)
    return Response(
        {"message": "User created", "user": serializer.data, "tokens": tokens},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # Now authenticate with username and password
    user = authenticate(username=user.username, password=password)
    serializer = UserSerializer(user)
    if user is not None:
        tokens = get_tokens_for_user(user)
        return Response(
            {"message": "Login successful", "user": serializer.data, "tokens": tokens},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_me(request):
    user = request.user
    return Response({"id": user.id, "username": user.username, "email": user.email})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_me(request):
    user = request.user
    user.delete()
    return Response(
        {"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )
