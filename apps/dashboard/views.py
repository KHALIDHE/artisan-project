# dashboard/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Avg
from apps.accounts.decorators import admin_required
from apps.accounts.models import User
from apps.artisans.models import ArtisanProfile
from apps.clients.models import ClientProfile
from apps.categories.models import Category
from apps.requests.models import ServiceRequest
from apps.reviews.models import Review
from apps.notifications.models import Notification

@admin_required
def admin_dashboard(request):
    """Tableau de bord administrateur"""

    # Statistiques générales
    total_users = User.objects.count()
    total_clients = User.objects.filter(user_type='client').count()
    total_artisans = User.objects.filter(user_type='artisan').count()

    # Artisans en attente de vérification
    pending_artisans = ArtisanProfile.objects.filter(
        verification_status='pending'
    ).count()

    # Statistiques des demandes
    total_requests = ServiceRequest.objects.count()
    pending_requests = ServiceRequest.objects.filter(status='pending').count()
    completed_requests = ServiceRequest.objects.filter(status='completed').count()

    # Avis
    total_reviews = Review.objects.count()
    pending_reviews = Review.objects.filter(is_verified=False).count()

    # Catégories
    total_categories = Category.objects.count()

    # Activités récentes
    recent_users = User.objects.order_by('-created_at')[:5]
    recent_requests = ServiceRequest.objects.order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'total_clients': total_clients,
        'total_artisans': total_artisans,
        'pending_artisans': pending_artisans,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'completed_requests': completed_requests,
        'total_reviews': total_reviews,
        'pending_reviews': pending_reviews,
        'total_categories': total_categories,
        'recent_users': recent_users,
        'recent_requests': recent_requests,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


@admin_required
def verify_artisans(request):
    """Liste des artisans à vérifier"""
    status_filter = request.GET.get('status', 'pending')

    artisans = ArtisanProfile.objects.select_related('user')

    if status_filter != 'all':
        artisans = artisans.filter(verification_status=status_filter)

    artisans = artisans.order_by('-created_at')

    context = {
        'artisans': artisans,
        'status_filter': status_filter,
    }

    return render(request, 'dashboard/verify_artisans.html', context)


@admin_required
def verify_artisan_detail(request, artisan_id):
    """Détails d'un artisan à vérifier"""
    artisan_profile = get_object_or_404(ArtisanProfile, id=artisan_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            artisan_profile.verification_status = 'verified'
            artisan_profile.save()

            # Notification
            Notification.objects.create(
                user=artisan_profile.user,
                type='verification',
                message='Félicitations ! Votre profil a été vérifié et approuvé.',
                link='/artisans/dashboard/',
                priority='high'
            )

            messages.success(request, f'{artisan_profile.business_name} a été vérifié avec succès!')
            return redirect('dashboard:verify_artisans')

        elif action == 'reject':
            reason = request.POST.get('reason', '')
            artisan_profile.verification_status = 'rejected'
            artisan_profile.save()

            # Notification
            Notification.objects.create(
                user=artisan_profile.user,
                type='verification',
                message=f'Votre profil a été rejeté. Raison: {reason}',
                link='/artisans/profile/edit/',
                priority='high'
            )

            messages.warning(request, f'{artisan_profile.business_name} a été rejeté.')
            return redirect('dashboard:verify_artisans')

    context = {
        'artisan_profile': artisan_profile,
    }

    return render(request, 'dashboard/verify_artisan_detail.html', context)


@admin_required
def manage_reviews(request):
    """Gérer les avis"""
    filter_type = request.GET.get('filter', 'all')

    reviews = Review.objects.select_related('client', 'artisan').order_by('-created_at')

    if filter_type == 'pending':
        reviews = reviews.filter(is_verified=False)
    elif filter_type == 'hidden':
        reviews = reviews.filter(is_visible=False)

    context = {
        'reviews': reviews,
        'filter_type': filter_type,
    }

    return render(request, 'dashboard/manage_reviews.html', context)


@admin_required
def review_action(request, review_id):
    """Actions sur un avis"""
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'verify':
            review.is_verified = True
            review.save()
            messages.success(request, 'Avis vérifié.')

        elif action == 'hide':
            review.is_visible = False
            review.save()
            messages.warning(request, 'Avis masqué.')

        elif action == 'show':
            review.is_visible = True
            review.save()
            messages.success(request, 'Avis rendu visible.')

        elif action == 'delete':
            review.delete()
            messages.success(request, 'Avis supprimé.')

    return redirect('dashboard:manage_reviews')


@admin_required
def manage_categories(request):
    """Gérer les catégories"""
    categories = Category.objects.annotate(
        artisan_count=Count('artisans')
    ).order_by('name_fr')

    context = {
        'categories': categories,
    }

    return render(request, 'dashboard/manage_categories.html', context)


@admin_required
def create_category(request):
    """Créer une nouvelle catégorie"""
    if request.method == 'POST':
        name_fr = request.POST.get('name_fr')
        name_ar = request.POST.get('name_ar')
        description = request.POST.get('description')
        icon = request.POST.get('icon')

        if name_fr and name_ar:
            Category.objects.create(
                name_fr=name_fr,
                name_ar=name_ar,
                description=description,
                icon=icon
            )
            messages.success(request, 'Catégorie créée avec succès!')
            return redirect('dashboard:manage_categories')

    return render(request, 'dashboard/create_category.html')


@admin_required
def edit_category(request, category_id):
    """Modifier une catégorie"""
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.name_fr = request.POST.get('name_fr')
        category.name_ar = request.POST.get('name_ar')
        category.description = request.POST.get('description')
        category.icon = request.POST.get('icon')
        category.is_active = request.POST.get('is_active') == 'on'
        category.save()

        messages.success(request, 'Catégorie mise à jour!')
        return redirect('dashboard:manage_categories')

    context = {
        'category': category,
    }

    return render(request, 'dashboard/edit_category.html', context)


@admin_required
def delete_category(request, category_id):
    """Supprimer une catégorie"""
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, 'Catégorie supprimée.')
    return redirect('dashboard:manage_categories')


@admin_required
def users_list(request):
    """Liste des utilisateurs"""
    user_type = request.GET.get('type', 'all')

    users = User.objects.all().order_by('-created_at')

    if user_type != 'all':
        users = users.filter(user_type=user_type)

    context = {
        'users': users,
        'user_type': user_type,
    }

    return render(request, 'dashboard/users_list.html', context)


@admin_required
def toggle_user_status(request, user_id):
    """Activer/Désactiver un utilisateur"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    status = "activé" if user.is_active else "désactivé"
    messages.success(request, f'Utilisateur {status}.')

    return redirect('dashboard:users_list')


@admin_required
def platform_statistics(request):
    """Statistiques détaillées de la plateforme"""

    # Statistiques utilisateurs
    users_by_type = User.objects.values('user_type').annotate(count=Count('id'))

    # Statistiques demandes par statut
    requests_by_status = ServiceRequest.objects.values('status').annotate(count=Count('id'))

    # Catégories les plus populaires
    popular_categories = Category.objects.annotate(
        request_count=Count('servicerequest')
    ).order_by('-request_count')[:5]

    # Artisans les mieux notés
    top_artisans = ArtisanProfile.objects.filter(
        verification_status='verified'
    ).order_by('-rating')[:5]

    # Statistiques avis
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'users_by_type': users_by_type,
        'requests_by_status': requests_by_status,
        'popular_categories': popular_categories,
        'top_artisans': top_artisans,
        'avg_rating': avg_rating,
    }

    return render(request, 'dashboard/statistics.html', context)