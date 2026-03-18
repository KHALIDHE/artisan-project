# chat/models.py

from django.db import models
from django.conf import settings

class ChatMessage(models.Model):
    conversation_id = models.CharField(max_length=100, db_index=True, verbose_name='ID Conversation')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')

    message = models.TextField(verbose_name='Message')
    is_read = models.BooleanField(default=False, verbose_name='Lu')

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message Chat'
        verbose_name_plural = 'Messages Chat'
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.email} → {self.recipient.email}"

    @staticmethod
    def get_conversation_id(user1_id, user2_id):
        """Générer un ID unique pour une conversation entre 2 utilisateurs"""
        return f"{'_'.join(map(str, sorted([user1_id, user2_id])))}"