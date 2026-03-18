# dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard principal
    path('', views.admin_dashboard, name='admin_dashboard'),

    # Vérification artisans
    path('artisans/verify/', views.verify_artisans, name='verify_artisans'),
    path('artisans/verify/<int:artisan_id>/', views.verify_artisan_detail, name='verify_artisan_detail'),

    # Gestion avis
    path('reviews/', views.manage_reviews, name='manage_reviews'),
    path('reviews/<int:review_id>/action/', views.review_action, name='review_action'),

    # Gestion catégories
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),

    # Gestion utilisateurs
    path('users/', views.users_list, name='users_list'),
    path('users/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),

    # Statistiques
    path('statistics/', views.platform_statistics, name='statistics'),
]