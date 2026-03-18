# requests/models.py

from django.db import models
from django.conf import settings
from apps.categories.models import Category

class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Refusée'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    )

    URGENCY_CHOICES = (
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    )

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_requests')
    artisan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artisan_requests', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=200, verbose_name='Titre')
    description = models.TextField(verbose_name='Description')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')

    # Localisation
    address = models.CharField(max_length=255, verbose_name='Adresse')
    city = models.CharField(max_length=100, verbose_name='Ville')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Prix
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Prix estimé')
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Prix final')

    # Dates
    date_requested = models.DateTimeField(auto_now_add=True)
    preferred_date = models.DateField(null=True, blank=True, verbose_name='Date souhaitée')
    date_accepted = models.DateTimeField(null=True, blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)

    # Photos
    photos = models.ImageField(upload_to='requests/photos/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Demande de Service'
        verbose_name_plural = 'Demandes de Service'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.client.email}"