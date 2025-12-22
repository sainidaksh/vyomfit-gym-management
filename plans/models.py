from django.db import models
from gyms.models import Gym

class Plan(models.Model):
    DURATION_TYPES = (
        ("days", "Days"),
        ("weeks", "Weeks"),
        ("months", "Months"),
    )

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    duration_type = models.CharField(max_length=10, choices=DURATION_TYPES, default="months")
    duration_value = models.PositiveIntegerField(default=1)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.duration_value} {self.duration_type})"
