# artisans/models.py

from django.db import models
from django.conf import settings
from apps.categories.models import Category
#pour les artisans on ajout un profill comme linkedin
#il peut ausssi noter les clientes
class ArtisanProfile(models.Model):
    VERIFICATION_STATUS = (
        ('pending', 'En attente'),
        ('verified', 'Vérifié'),
        ('rejected', 'Rejeté'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artisan_profile')
    business_name = models.CharField(max_length=200, verbose_name='Nom de l\'entreprise')
    bio = models.TextField(verbose_name='Biographie')
    categories = models.ManyToManyField(Category, related_name='artisans', verbose_name='Catégories')

    # Documents et vérification
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    id_card = models.ImageField(upload_to='apps.artisans/documents/', blank=True, verbose_name='Carte d\'identité')
    business_license = models.ImageField(upload_to='artisans/documents/', blank=True, verbose_name='Licence')
    whatsapp_number = models.CharField(max_length=20, blank=True, verbose_name='Numéro WhatsApp')# un autre methode
    # Expérience et statistiques
    experience_years = models.PositiveIntegerField(default=0, verbose_name='Années d\'expérience')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, verbose_name='Note moyenne')
    total_reviews = models.PositiveIntegerField(default=0, verbose_name='Nombre d\'avis')
    total_jobs = models.PositiveIntegerField(default=0, verbose_name='Travaux complétés')

    # Disponibilité
    is_available = models.BooleanField(default=True, verbose_name='Disponible')
    availability_note = models.TextField(blank=True, verbose_name='Note de disponibilité')

    # Photos
    profile_photo = models.ImageField(upload_to='artisans/photos/', blank=True, verbose_name='Photo de profil')
    cover_photo = models.ImageField(upload_to='artisans/covers/', blank=True, verbose_name='Photo de couverture')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil Artisan'
        verbose_name_plural = 'Profils Artisans'

    def __str__(self):
        return self.business_name

    def update_rating(self):
        """Mettre à jour la note moyenne"""
        from reviews.models import Review
        reviews = Review.objects.filter(artisan=self.user, is_verified=True)
        if reviews.exists():
            self.rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.total_reviews = reviews.count()
            self.save()

class PortfolioImage(models.Model):
    artisan = models.ForeignKey(ArtisanProfile, on_delete=models.CASCADE, related_name='portfolio')
    image = models.ImageField(upload_to='artisans/portfolio/')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Image Portfolio'
        verbose_name_plural = 'Images Portfolio'
        ordering = ['-created_at']

    def __str__(self):
        return f"Portfolio - {self.artisan.business_name}"