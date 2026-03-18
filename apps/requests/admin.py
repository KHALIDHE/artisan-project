from django.contrib import admin
from .models import ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'artisan', 'status', 'created_at')
    list_filter = ('status', 'urgency', 'created_at')
    search_fields = ('title', 'description', 'client__email')
