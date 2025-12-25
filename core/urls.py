# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import dashboard, logout_page, logout_confirm, analytics_view

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),

    path("logout/", logout_page, name="logout_page"),
    path("logout/confirm/", logout_confirm, name="logout_confirm"),

    # 🔴 ONLY ONE ROOT URL
    path("", dashboard, name="dashboard"),

    path("admin/", admin.site.urls),

    path("members/", include("members.urls")),
    path("plans/", include("plans.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("attendance/", include("attendance.urls")),
    path("notifications/", include("notifications.urls")),
    path("payments/", include("payments.urls")),
    path("analytics/", analytics_view, name="analytics"),
]
