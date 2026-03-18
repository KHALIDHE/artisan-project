# user_messages/models.py

from django.db import models
from django.conf import settings

class Conversation(models.Model):
    """Conversation entre un client et un artisan"""
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_conversations'
    )
    artisan = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artisan_conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('client', 'artisan')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.client.email} - {self.artisan.email}"

    def get_last_message(self):
        return self.user_messages.first()

    def get_unread_count(self, user):
        return self.user_messages.filter(is_read=False).exclude(sender=user).count()


class ConversationMessage(models.Model):
    """Message dans une conversation"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='user_messages'  # CHANGED FROM 'messages' TO 'user_messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_conversation_messages'
    )
    content = models.TextField(verbose_name='Message')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message de conversation'
        verbose_name_plural = 'Messages de conversation'

    def __str__(self):
        return f"{self.sender.email}: {self.content[:50]}"