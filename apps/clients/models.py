# clients/models.py

from django.db import models
from django.conf import settings

class ClientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')

    # Préférences
    preferred_categories = models.JSONField(default=list, blank=True, verbose_name='Catégories préférées')
    budget_range = models.CharField(max_length=50, blank=True, verbose_name='Budget habituel')

    # Statistiques
    total_requests = models.PositiveIntegerField(default=0, verbose_name='Demandes envoyées')
    completed_requests = models.PositiveIntegerField(default=0, verbose_name='Demandes complétées')

    # Photo
    profile_photo = models.ImageField(upload_to='clients/photos/', blank=True, verbose_name='Photo de profil')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil Client'
        verbose_name_plural = 'Profils Clients'

    def __str__(self):
        return f"Client - {self.user.email}"

class FavoriteArtisan(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    artisan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'artisan')
        verbose_name = 'Artisan Favori'
        verbose_name_plural = 'Artisans Favoris'
