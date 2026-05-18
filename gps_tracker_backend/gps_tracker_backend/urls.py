"""
URL configuration for gps_tracker_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("apps.accounts.urls")),
    # path("api/v1/tracking/", include("apps.tracking.urls")),
    # path("api/v1/devices/", include("apps.devices.urls")),
    # path("api/v1/alerts/", include("apps.alerts.urls")),
]


# Invoke-RestMethod `
#   -Uri "http://127.0.0.1:8000/api/v1/accounts/register/" `
#   -Method POST `
#   -ContentType "application/json" `
#   -Body '{
#     "phone": "+919999999999",
#     "full_name": "Test User",
#     "email": "test@example.com",
#     "password": "StrongPassword123"
# }'