from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import User

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# =========================================================
# REGISTER VIEW
# =========================================================

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserRegistrationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        tokens = get_tokens_for_user(user)

        return Response(
            {
                "message": "Registration successful",
                "user": UserSerializer(user).data,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED
        )


# =========================================================
# LOGIN VIEW
# =========================================================

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        phone = request.data.get("phone")
        password = request.data.get("password")

        if not phone or not password:

            return Response(
                {
                    "error": "Phone and password are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            phone=phone,
            password=password
        )

        if user is None:

            return Response(
                {
                    "error": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:

            return Response(
                {
                    "error": "Account is disabled"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        tokens = get_tokens_for_user(user)

        return Response(
            {
                "message": "Login successful",
                "user": UserSerializer(user).data,
                "tokens": tokens,
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# PROFILE VIEW
# =========================================================

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request):

        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Profile updated successfully",
                "user": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# LOGOUT VIEW
# =========================================================

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            refresh_token = request.data.get(
                "refresh"
            )

            if not refresh_token:

                return Response(
                    {
                        "error": "Refresh token required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response(
                {
                    "message": "Logout successful"
                },
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception:

            return Response(
                {
                    "error": "Invalid token"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# =========================================================
# TOKEN REFRESH VIEW
# =========================================================

class RefreshTokenView(TokenRefreshView):
    pass