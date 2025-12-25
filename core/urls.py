from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import dashboard, logout_page, logout_confirm
from . import views

urlpatterns = [
    # LOGIN
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # LOGOUT (Custom)
    path('logout/', logout_page, name='logout_page'),
    path('logout/confirm/', logout_confirm, name='logout_confirm'),

    # Dashboard
    path('', dashboard, name='dashboard'),

    # Admin
    path('admin/', admin.site.urls),

    # Apps
    path('members/', include('members.urls')),
    path('plans/', include('plans.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('attendance/', include('attendance.urls')),
    path('notifications/', include('notifications.urls')),
    path('payments/', include('payments.urls')),
    path("analytics/", views.analytics_view, name="analytics"),
    path("", views.home, name="home"),

    

]
