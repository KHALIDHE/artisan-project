
from django.db import models

class Category(models.Model):
    name_fr = models.CharField(max_length=100, verbose_name='Nom (Français)')
    name_ar = models.CharField(max_length=100, verbose_name='Nom (Arabe)')
    description = models.TextField(blank=True, verbose_name='Description')
    icon = models.CharField(max_length=50, blank=True, help_text='Nom de l\'icône (ex: fa-wrench)')
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['name_fr']

    def __str__(self):
        return self.name_fr