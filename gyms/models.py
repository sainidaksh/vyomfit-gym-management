from django.db import models
from django.conf import settings

class Gym(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='gym_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
