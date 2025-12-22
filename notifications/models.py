from django.db import models
from gyms.models import Gym
from members.models import Member


class Notification(models.Model):
    TYPE_CHOICES = (
        ("expiry", "Expiry"),
        ("attendance", "Attendance"),
        ("general", "General"),
    )

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=100, null=True, blank=True) 
    message = models.TextField()

    notif_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="general",
    )

    sent_at = models.DateTimeField(auto_now_add=True)

    # pehle se tha – rakho (agar use nahi bhi ho raha to chalega)
    is_sent = models.BooleanField(default=False)

    # NEW: read/unread status
    is_read = models.BooleanField(default=False)

    def __str__(self):
        if self.member:
            return f"{self.member.full_name} - {self.notif_type} - {self.sent_at}"
        return f"{self.notif_type} - {self.sent_at}"
