from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    RefreshTokenView,
)

app_name = "accounts"

urlpatterns = [

    # Authentication
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # JWT Token Refresh
    path(
        "token/refresh/",
        RefreshTokenView.as_view(),
        name="token_refresh",
    ),

    # User Profile
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),
]