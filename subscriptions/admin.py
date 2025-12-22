from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('member', 'plan', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('member__full_name', 'plan__name')
    ordering = ('-start_date',)
