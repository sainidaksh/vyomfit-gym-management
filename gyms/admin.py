from django.contrib import admin
from .models import Gym

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'owner', 'created_at')
    search_fields = ('name', 'city', 'owner__username')
    ordering = ('-created_at',)
