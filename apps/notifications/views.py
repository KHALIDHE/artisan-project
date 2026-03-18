# notifications/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notifications_list(request):
    """Liste de toutes les notifications"""
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # Marquer comme lues si demandé
    if request.GET.get('mark_read'):
        notifications.filter(is_read=False).update(is_read=True)

    context = {
        'notifications': notifications,
    }

    return render(request, 'notifications/list.html', context)


@login_required
def mark_as_read(request, notification_id):
    """Marquer une notification comme lue"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()

    # Rediriger vers le lien de la notification
    if notification.link:
        return redirect(notification.link)
    return redirect('notifications:list')


@login_required
def mark_all_as_read(request):
    """Marquer toutes les notifications comme lues"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:list')


@login_required
def delete_notification(request, notification_id):
    """Supprimer une notification"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('notifications:list')


@login_required
def get_unread_count(request):
    """API pour obtenir le nombre de notifications non lues"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})


@login_required
def get_recent_notifications(request):
    """API pour obtenir les notifications récentes (pour le dropdown)"""
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    data = [{
        'id': notif.id,
        'type': notif.type,
        'message': notif.message,
        'link': notif.link,
        'is_read': notif.is_read,
        'created_at': notif.created_at.strftime('%d/%m/%Y %H:%M'),
        'priority': notif.priority,
    } for notif in notifications]

    return JsonResponse({'notifications': data})