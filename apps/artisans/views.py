# artisans/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from apps.accounts.decorators import artisan_required
from .models import ArtisanProfile, PortfolioImage
from .forms import ArtisanProfileForm, PortfolioImageForm, ServiceRequestResponseForm
from apps.requests.models import ServiceRequest
from apps.notifications.models import Notification

@artisan_required
def dashboard(request):
    """Tableau de bord artisan"""
    artisan_profile = request.user.artisan_profile

    # Statistiques
    pending_requests = ServiceRequest.objects.filter(
        artisan=request.user,
        status='pending'
    ).count()

    active_requests = ServiceRequest.objects.filter(
        artisan=request.user,
        status__in=['accepted', 'in_progress']
    ).count()

    completed_requests = ServiceRequest.objects.filter(
        artisan=request.user,
        status='completed'
    ).count()

    # Demandes récentes
    recent_requests = ServiceRequest.objects.filter(
        artisan=request.user
    ).order_by('-created_at')[:5]

    # Notifications non lues
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    context = {
        'artisan_profile': artisan_profile,
        'pending_requests': pending_requests,
        'active_requests': active_requests,
        'completed_requests': completed_requests,
        'recent_requests': recent_requests,
        'unread_notifications': unread_notifications,
    }

    return render(request, 'artisans/dashboard.html', context)


@artisan_required
def complete_profile(request):
    """Compléter le profil artisan (première connexion)"""
    artisan_profile = request.user.artisan_profile

    if request.method == 'POST':
        form = ArtisanProfileForm(request.POST, request.FILES, instance=artisan_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été complété avec succès!')
            return redirect('artisans:dashboard')
    else:
        form = ArtisanProfileForm(instance=artisan_profile)

    return render(request, 'artisans/complete_profile.html', {'form': form})


@artisan_required
def edit_profile(request):
    """Modifier le profil artisan"""
    artisan_profile = request.user.artisan_profile

    if request.method == 'POST':
        form = ArtisanProfileForm(request.POST, request.FILES, instance=artisan_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour!')
            return redirect('artisans:profile_detail')
    else:
        form = ArtisanProfileForm(instance=artisan_profile)

    return render(request, 'artisans/edit_profile.html', {'form': form})


@artisan_required
def profile_detail(request):
    """Voir son propre profil"""
    artisan_profile = request.user.artisan_profile
    portfolio_images = PortfolioImage.objects.filter(artisan=artisan_profile)

    context = {
        'artisan_profile': artisan_profile,
        'portfolio_images': portfolio_images,
    }

    return render(request, 'artisans/profile_detail.html', context)


@artisan_required
def manage_portfolio(request):
    """Gérer le portfolio"""
    artisan_profile = request.user.artisan_profile
    portfolio_images = PortfolioImage.objects.filter(artisan=artisan_profile)

    if request.method == 'POST':
        form = PortfolioImageForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio_item = form.save(commit=False)
            portfolio_item.artisan = artisan_profile
            portfolio_item.save()
            messages.success(request, 'Image ajoutée au portfolio!')
            return redirect('artisans:manage_portfolio')
    else:
        form = PortfolioImageForm()

    context = {
        'form': form,
        'portfolio_images': portfolio_images,
    }

    return render(request, 'artisans/manage_portfolio.html', context)


@artisan_required
def delete_portfolio_image(request, image_id):
    """Supprimer une image du portfolio"""
    image = get_object_or_404(PortfolioImage, id=image_id, artisan=request.user.artisan_profile)
    image.delete()
    messages.success(request, 'Image supprimée du portfolio.')
    return redirect('artisans:manage_portfolio')


@artisan_required
def service_requests_list(request):
    """Liste de toutes les demandes"""
    status_filter = request.GET.get('status', 'all')

    requests_queryset = ServiceRequest.objects.filter(artisan=request.user)

    if status_filter != 'all':
        requests_queryset = requests_queryset.filter(status=status_filter)

    requests_queryset = requests_queryset.order_by('-created_at')

    context = {
        'service_requests': requests_queryset,
        'status_filter': status_filter,
    }

    return render(request, 'artisans/service_requests_list.html', context)


@artisan_required
def service_request_detail(request, request_id):
    """Détails d'une demande"""
    service_request = get_object_or_404(ServiceRequest, id=request_id, artisan=request.user)

    if request.method == 'POST':
        form = ServiceRequestResponseForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']

            if action == 'accept':
                service_request.status = 'accepted'
                service_request.date_accepted = timezone.now()
                if form.cleaned_data['estimated_price']:
                    service_request.estimated_price = form.cleaned_data['estimated_price']
                service_request.save()

                # Créer notification pour le client
                Notification.objects.create(
                    user=service_request.client,
                    type='accepted',
                    message=f'Votre demande "{service_request.title}" a été acceptée par {request.user.artisan_profile.business_name}',
                    link=f'/requests/{service_request.id}/'
                )

                messages.success(request, 'Demande acceptée!')
            else:
                service_request.status = 'rejected'
                service_request.save()

                # Créer notification pour le client
                Notification.objects.create(
                    user=service_request.client,
                    type='rejected',
                    message=f'Votre demande "{service_request.title}" a été refusée',
                    link=f'/requests/{service_request.id}/'
                )

                messages.info(request, 'Demande refusée.')

            return redirect('artisans:service_requests_list')
    else:
        form = ServiceRequestResponseForm()

    context = {
        'service_request': service_request,
        'form': form,
    }

    return render(request, 'artisans/service_request_detail.html', context)


@artisan_required
def update_request_status(request, request_id):
    """Mettre à jour le statut d'une demande"""
    service_request = get_object_or_404(ServiceRequest, id=request_id, artisan=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in ['in_progress', 'completed']:
            service_request.status = new_status

            if new_status == 'completed':
                service_request.date_completed = timezone.now()
                service_request.artisan.artisan_profile.total_jobs += 1
                service_request.artisan.artisan_profile.save()

                # Notification pour le client
                Notification.objects.create(
                    user=service_request.client,
                    type='completed',
                    message=f'Le service "{service_request.title}" est terminé! Laissez un avis.',
                    link=f'/reviews/create/{service_request.id}/'
                )

            service_request.save()
            messages.success(request, f'Statut mis à jour: {service_request.get_status_display()}')

    return redirect('artisans:service_request_detail', request_id=request_id)

# artisans/views.py - AJOUTEZ cette fonction

from django.http import JsonResponse
from apps.requests.models import ServiceRequest
from django.shortcuts import render, redirect, get_object_or_404
from apps.accounts.decorators import artisan_required
from apps.requests.models import ServiceRequest

@artisan_required
def view_request_map(request, request_id):
    """Carte pour voir la position du client qui a fait la demande"""
    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id,
        artisan=request.user
    )

    # Données du client
    client = service_request.client

    context = {
        'service_request': service_request,
        'client': client,
        'client_lat': float(client.latitude) if client.latitude else 33.9716,
        'client_lng': float(client.longitude) if client.longitude else -6.8498,
        'artisan_lat': float(request.user.latitude) if request.user.latitude else 33.9716,
        'artisan_lng': float(request.user.longitude) if request.user.longitude else -6.8498,
    }

    return render(request, 'artisans/request_map.html', context)

def get_requests_json(request):
    """API pour obtenir les demandes en attente (pour artisans)"""
    # Filtres
    category_id = request.GET.get('category')
    urgency = request.GET.get('urgency')

    # Demandes en attente avec coordonnées GPS
    requests = ServiceRequest.objects.filter(
        status='pending',
        client__latitude__isnull=False,
        client__longitude__isnull=False
    ).select_related('client', 'category')

    if category_id:
        requests = requests.filter(category_id=category_id)

    if urgency:
        requests = requests.filter(urgency=urgency)

    # Convertir en JSON
    requests_data = []
    for req in requests:
        requests_data.append({
            'id': req.id,
            'title': req.title,
            'description': req.description,
            'category': req.category.name_fr if req.category else '',
            'urgency': req.urgency,
            'latitude': float(req.client.latitude),
            'longitude': float(req.client.longitude),
            'city': req.client.city,
            'address': req.address,
            'created_at': req.created_at.strftime('%d/%m/%Y %H:%M'),
            'estimated_price': float(req.estimated_price) if req.estimated_price else None,
        })

    return JsonResponse({'requests': requests_data})