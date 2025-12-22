from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("member", "notif_type", "sent_at", "is_read")
    list_filter = ("notif_type", "is_read", "sent_at")
    search_fields = ("member__full_name", "message")
    ordering = ("-sent_at",)
