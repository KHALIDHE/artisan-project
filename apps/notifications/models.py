# notifications/models.py

from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = (
        ('request', 'Nouvelle demande'),
        ('accepted', 'Demande acceptée'),
        ('rejected', 'Demande refusée'),
        ('completed', 'Service terminé'),
        ('review', 'Nouvel avis'),
        ('message', 'Nouveau message'),
        ('verification', 'Vérification'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField(verbose_name='Message')
    link = models.CharField(max_length=255, blank=True, verbose_name='Lien')

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False, verbose_name='Lu')
    is_sent = models.BooleanField(default=False, verbose_name='Envoyé')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.type}"