# notifications/admin.py

from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'message', 'is_read', 'priority', 'created_at')
    list_filter = ('type', 'is_read', 'priority', 'created_at')
    search_fields = ('user__email', 'message')