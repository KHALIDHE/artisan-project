# artisans/admin.py

from django.contrib import admin
from .models import ArtisanProfile, PortfolioImage

@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'verification_status', 'rating', 'is_available')
    list_filter = ('verification_status', 'is_available')
    search_fields = ('business_name', 'user__email')

@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ('artisan', 'title', 'created_at')
    list_filter = ('created_at',)