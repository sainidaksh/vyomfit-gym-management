from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'time')
    list_filter = ('date',)
    search_fields = ('member__full_name',)
    ordering = ('-date',)
