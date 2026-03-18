# clients/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from apps.accounts.decorators import client_required
from .models import ClientProfile, FavoriteArtisan
from .forms import ServiceRequestForm, ReviewForm, ArtisanSearchForm
from apps.artisans.models import ArtisanProfile
from apps.requests.models import ServiceRequest
from apps.reviews.models import Review
from apps.categories.models import Category
from apps.notifications.models import Notification

@client_required
def dashboard(request):
    """Tableau de bord client"""
    client_profile = request.user.client_profile

    # Statistiques
    pending_requests = ServiceRequest.objects.filter(
        client=request.user,
        status='pending'
    ).count()

    active_requests = ServiceRequest.objects.filter(
        client=request.user,
        status__in=['accepted', 'in_progress']
    ).count()

    completed_requests = ServiceRequest.objects.filter(
        client=request.user,
        status='completed'
    ).count()

    # Demandes récentes
    recent_requests = ServiceRequest.objects.filter(
        client=request.user
    ).order_by('-created_at')[:5]

    # Notifications non lues
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    # Artisans favoris
    favorites = FavoriteArtisan.objects.filter(client=request.user).select_related('artisan__artisan_profile')[:3]

    context = {
        'client_profile': client_profile,
        'pending_requests': pending_requests,
        'active_requests': active_requests,
        'completed_requests': completed_requests,
        'recent_requests': recent_requests,
        'unread_notifications': unread_notifications,
        'favorites': favorites,
    }

    return render(request, 'clients/dashboard.html', context)


def search_artisans(request):
    """Recherche d'artisans (accessible sans connexion)"""
    form = ArtisanSearchForm(request.GET or None)

    # Tous les artisans vérifiés
    artisans = ArtisanProfile.objects.filter(
        verification_status='verified'
    ).select_related('user')

    # Filtres
    if form.is_valid():
        category = form.cleaned_data.get('category')
        city = form.cleaned_data.get('city')
        min_rating = form.cleaned_data.get('min_rating')
        available_only = form.cleaned_data.get('available_only')

        if category:
            artisans = artisans.filter(categories=category)

        if city:
            artisans = artisans.filter(user__city__icontains=city)

        if min_rating:
            artisans = artisans.filter(rating__gte=float(min_rating))

        if available_only:
            artisans = artisans.filter(is_available=True)

    # Récupérer les catégories pour l'affichage
    categories = Category.objects.filter(is_active=True)

    context = {
        'form': form,
        'artisans': artisans,
        'categories': categories,
    }

    return render(request, 'clients/search_artisans.html', context)


def artisan_detail(request, artisan_id):
    """Détails d'un artisan (accessible sans connexion)"""
    artisan_profile = get_object_or_404(
        ArtisanProfile.objects.select_related('user'),
        id=artisan_id,
        verification_status='verified'
    )

    # Portfolio
    portfolio_images = artisan_profile.portfolio.all()[:6]

    # Avis
    reviews = Review.objects.filter(
        artisan=artisan_profile.user,
        is_visible=True
    ).order_by('-created_at')[:10]

    # Vérifier si l'utilisateur a mis en favori
    is_favorite = False
    if request.user.is_authenticated and request.user.is_client():
        is_favorite = FavoriteArtisan.objects.filter(
            client=request.user,
            artisan=artisan_profile.user
        ).exists()

    context = {
        'artisan_profile': artisan_profile,
        'portfolio_images': portfolio_images,
        'reviews': reviews,
        'is_favorite': is_favorite,
    }

    return render(request, 'clients/artisan_detail.html', context)


@client_required
def create_service_request(request, artisan_id=None):
    """Créer une demande de service"""
    artisan = None
    if artisan_id:
        artisan = get_object_or_404(ArtisanProfile, id=artisan_id).user

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.client = request.user
            if artisan:
                service_request.artisan = artisan
            service_request.save()

            # Créer notification pour l'artisan
            if artisan:
                Notification.objects.create(
                    user=artisan,
                    type='request',
                    message=f'Nouvelle demande de service: {service_request.title}',
                    link=f'/artisans/requests/{service_request.id}/',
                    priority='high'
                )

            # Mettre à jour le profil client
            request.user.client_profile.total_requests += 1
            request.user.client_profile.save()

            messages.success(request, 'Votre demande a été envoyée avec succès!')
            return redirect('clients:my_requests')
    else:
        form = ServiceRequestForm()

    context = {
        'form': form,
        'artisan': artisan,
    }

    return render(request, 'clients/create_service_request.html', context)


@client_required
def my_requests(request):
    """Mes demandes de service"""
    status_filter = request.GET.get('status', 'all')

    requests_queryset = ServiceRequest.objects.filter(client=request.user)

    if status_filter != 'all':
        requests_queryset = requests_queryset.filter(status=status_filter)

    requests_queryset = requests_queryset.order_by('-created_at')

    context = {
        'service_requests': requests_queryset,
        'status_filter': status_filter,
    }

    return render(request, 'clients/my_requests.html', context)


@client_required
def request_detail(request, request_id):
    """Détails d'une demande"""
    service_request = get_object_or_404(ServiceRequest, id=request_id, client=request.user)

    context = {
        'service_request': service_request,
    }

    return render(request, 'clients/request_detail.html', context)


@client_required
def create_review(request, request_id):
    """Créer un avis après un service"""
    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id,
        client=request.user,
        status='completed'
    )

    # Vérifier si un avis existe déjà
    if hasattr(service_request, 'review'):
        messages.warning(request, 'Vous avez déjà laissé un avis pour ce service.')
        return redirect('clients:request_detail', request_id=request_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = request.user
            review.artisan = service_request.artisan
            review.service_request = service_request
            review.save()

            # Mettre à jour la note de l'artisan
            service_request.artisan.artisan_profile.update_rating()

            # Notification pour l'artisan
            Notification.objects.create(
                user=service_request.artisan,
                type='review',
                message=f'Nouvel avis {review.rating}★ de {request.user.email}',
                link=f'/artisans/profile/'
            )

            messages.success(request, 'Merci pour votre avis!')
            return redirect('clients:request_detail', request_id=request_id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'service_request': service_request,
    }

    return render(request, 'clients/create_review.html', context)


@client_required
def toggle_favorite(request, artisan_id):
    """Ajouter/Retirer des favoris"""
    artisan = get_object_or_404(ArtisanProfile, id=artisan_id).user

    favorite, created = FavoriteArtisan.objects.get_or_create(
        client=request.user,
        artisan=artisan
    )

    if not created:
        favorite.delete()
        messages.info(request, 'Artisan retiré des favoris.')
    else:
        messages.success(request, 'Artisan ajouté aux favoris!')

    return redirect('clients:artisan_detail', artisan_id=artisan_id)


@client_required
def my_favorites(request):
    """Mes artisans favoris"""
    favorites = FavoriteArtisan.objects.filter(
        client=request.user
    ).select_related('artisan__artisan_profile')

    context = {
        'favorites': favorites,
    }

    return render(request, 'clients/my_favorites.html', context)

from django.http import JsonResponse
import json

# Dans clients/views.py
from django.conf import settings

# clients/views.py

# clients/views.py

def search_artisans_map(request):
    """Recherche d'artisans avec carte interactive - Style LinkedIn"""
    form = ArtisanSearchForm(request.GET or None)

    artisans = ArtisanProfile.objects.filter(
        verification_status='verified',
        is_available=True
    ).select_related('user')

    categories = Category.objects.filter(is_active=True)

    context = {
        'form': form,
        'artisans': artisans,
        'categories': categories,
    }

    return render(request, 'clients/search_map_enhanced.html', context)

def get_artisans_json(request):
    """API pour obtenir les artisans en JSON"""
    category_id = request.GET.get('category')
    city = request.GET.get('city')
    min_rating = request.GET.get('min_rating')

    artisans = ArtisanProfile.objects.filter(
        verification_status='verified',
        is_available=True
    ).select_related('user')

    if category_id:
        artisans = artisans.filter(categories__id=category_id)
    if city:
        artisans = artisans.filter(user__city__icontains=city)
    if min_rating:
        artisans = artisans.filter(rating__gte=float(min_rating))

    artisans_data = []
    for artisan in artisans:
        if artisan.user.latitude and artisan.user.longitude:
            artisans_data.append({
                'id': artisan.id,
                'user_id': artisan.user.id,  # AJOUTEZ CETTE LIGNE
                'business_name': artisan.business_name,
                'rating': float(artisan.rating),
                'total_reviews': artisan.total_reviews,
                'latitude': float(artisan.user.latitude),
                'longitude': float(artisan.user.longitude),
                'city': artisan.user.city,
                'phone': str(artisan.user.phone) if artisan.user.phone else '',
                'categories': [cat.name_fr for cat in artisan.categories.all()],
                'profile_photo': artisan.profile_photo.url if artisan.profile_photo else None,
                'url': f'/clients/artisan/{artisan.id}/',
            })

    return JsonResponse({'artisans': artisans_data})