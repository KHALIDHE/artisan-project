# reviews/models.py

from django.db import models
from django.conf import settings
from apps.requests.models import ServiceRequest

class Review(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    artisan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE, related_name='review')

    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Note')
    comment = models.TextField(verbose_name='Commentaire')

    # Photos
    photo1 = models.ImageField(upload_to='reviews/photos/', blank=True)
    photo2 = models.ImageField(upload_to='reviews/photos/', blank=True)
    photo3 = models.ImageField(upload_to='reviews/photos/', blank=True)

    is_verified = models.BooleanField(default=True, verbose_name='Vérifié')
    is_visible = models.BooleanField(default=True, verbose_name='Visible')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Avis'
        verbose_name_plural = 'Avis'
        ordering = ['-created_at']

    def __str__(self):
        return f"Avis {self.rating}★ - {self.artisan.email}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour la note de l'artisan
        if hasattr(self.artisan, 'artisan_profile'):
            self.artisan.artisan_profile.update_rating()