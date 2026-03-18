# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import ClientRegistrationForm, ArtisanRegistrationForm, UserLoginForm

# Page d'accueil
def home(request):
    return render(request, 'home/index.html')

# Page de choix du type d'utilisateur
def register_choice(request):
    return render(request, 'accounts/register_choice.html')

# Inscription Client
def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Votre compte client a été créé avec succès!')
            login(request, user)
            return redirect('clients:dashboard')
    else:
        form = ClientRegistrationForm()

    return render(request, 'accounts/register_client.html', {'form': form})

# Inscription Artisan
def register_artisan(request):
    if request.method == 'POST':
        form = ArtisanRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Votre compte artisan a été créé! En attente de vérification.')
            login(request, user)
            return redirect('artisans:complete_profile')
    else:
        form = ArtisanRegistrationForm()

    return render(request, 'accounts/register_artisan.html', {'form': form})

# Connexion
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.email}!')

                # Redirection selon le type d'utilisateur
                if user.user_type == 'admin' or user.is_staff:
                    return redirect('dashboard:admin_dashboard')
                if user.is_client():
                    return redirect('clients:dashboard')
                elif user.is_artisan():
                    return redirect('artisans:dashboard')
                else:
                    return redirect('dashboard:admin_dashboard')
            else:
                messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# Déconnexion
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('accounts:login')

# Profil utilisateur
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
