# reviews/admin.py
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'artisan', 'rating', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'created_at')