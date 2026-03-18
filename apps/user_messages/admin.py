# user_messages/admin.py

from django.contrib import admin
from .models import Conversation, ConversationMessage

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('client', 'artisan', 'created_at', 'updated_at')
    search_fields = ('client__email', 'artisan__email')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'content_preview', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'content')
    readonly_fields = ('created_at',)

    def content_preview(self, obj):
        """Show preview of message content"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Message'