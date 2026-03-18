# artisans/urls.py

from django.urls import path
from . import views

app_name = 'artisans'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Profil
    path('profile/complete/', views.complete_profile, name='complete_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile_detail, name='profile_detail'),

    # Portfolio
    path('portfolio/', views.manage_portfolio, name='manage_portfolio'),
    path('portfolio/delete/<int:image_id>/', views.delete_portfolio_image, name='delete_portfolio_image'),

    # Demandes de service
    path('requests/', views.service_requests_list, name='service_requests_list'),
    path('requests/<int:request_id>/', views.service_request_detail, name='service_request_detail'),
    path('requests/<int:request_id>/update-status/', views.update_request_status, name='update_request_status'),

    # Carte pour artisans

 
    path('requests/<int:request_id>/map/', views.view_request_map, name='view_request_map'),

]