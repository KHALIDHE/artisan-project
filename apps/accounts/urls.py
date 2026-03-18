# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/client/', views.register_client, name='register_client'),
    path('register/artisan/', views.register_artisan, name='register_artisan'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]