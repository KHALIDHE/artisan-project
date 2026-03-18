# clients/urls.py

from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Recherche
    path('search/', views.search_artisans, name='search_artisans'),
    path('artisan/<int:artisan_id>/', views.artisan_detail, name='artisan_detail'),

    # Demandes de service
    path('requests/create/', views.create_service_request, name='create_service_request'),
    path('requests/create/<int:artisan_id>/', views.create_service_request, name='create_service_request_for_artisan'),
    path('requests/', views.my_requests, name='my_requests'),
    path('requests/<int:request_id>/', views.request_detail, name='request_detail'),

    # Avis
    path('reviews/create/<int:request_id>/', views.create_review, name='create_review'),

    # Favoris
    path('favorites/toggle/<int:artisan_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    #map

    # Carte avec Leaflet
    path('search/map/', views.search_artisans_map, name='search_map'),

    # API pour la carte
    path('api/artisans/', views.get_artisans_json, name='api_artisans'),
]