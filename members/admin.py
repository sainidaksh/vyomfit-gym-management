from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'gender', 'age', 'join_date')
    search_fields = ('full_name', 'phone')
    list_filter = ('gender', 'join_date')
    ordering = ('-join_date',)
