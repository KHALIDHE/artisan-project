# categories/admin.py

from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_fr', 'name_ar', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name_fr', 'name_ar')