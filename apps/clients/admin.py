# clients/admin.py
from django.contrib import admin
from .models import ClientProfile, FavoriteArtisan

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_requests', 'completed_requests')

@admin.register(FavoriteArtisan)
class FavoriteArtisanAdmin(admin.ModelAdmin):
    list_display = ('client', 'artisan', 'created_at')

