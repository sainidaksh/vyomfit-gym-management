from django.urls import path
from . import views

urlpatterns = [
    path("", views.notifications_list, name="notifications_list"),

    path("read/<int:pk>/", views.mark_notification_read, name="notification_read"),
    path("read-all/", views.mark_all_read, name="notifications_read_all"),
    path("delete/<int:pk>/", views.delete_notification, name="notification_delete"),

    path("scan-low-attendance/", views.scan_low_attendance, name="scan_low_attendance"),
    path("send-expiry/", views.send_expiry_reminders, name="send_expiry_reminders"),
]
