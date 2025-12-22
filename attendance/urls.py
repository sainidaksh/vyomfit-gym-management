from django.urls import path
from . import views

urlpatterns = [
    path("", views.attendance_list, name="attendance_list"),
    path("mark/", views.mark_attendance_page, name="mark_attendance_page"),
    path("mark/<int:member_id>/", views.mark_attendance, name="mark_attendance"),
    path("analytics/", views.attendance_analytics, name="attendance_analytics"),
]
