from django.db import models
from members.models import Member
from gyms.models import Gym

class Attendance(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.full_name} - {self.date}"

    class Meta:
        unique_together = ('member', 'date')  # <- IMPORTANT
