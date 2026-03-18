# user_messages/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as flash_messages
from django.db.models import Q
from .models import Conversation, ConversationMessage
from apps.accounts.models import User

@login_required
def inbox(request):
    """Boîte de réception - liste des conversations"""
    if request.user.is_client():
        conversations = Conversation.objects.filter(client=request.user)
    elif request.user.is_artisan():
        conversations = Conversation.objects.filter(artisan=request.user)
    else:
        conversations = Conversation.objects.none()

    context = {
        'conversations': conversations,
    }

    return render(request, 'user_messages/inbox.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """Afficher une conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Vérifier que l'utilisateur fait partie de la conversation
    if request.user not in [conversation.client, conversation.artisan]:
        flash_messages.error(request, "Vous n'avez pas accès à cette conversation.")
        return redirect('messages:inbox')

    # Envoyer un message (avant de récupérer les messages pour que le nouveau apparaisse)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            new_message = ConversationMessage.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            print(f"Message créé: {new_message}")  # Debug
            flash_messages.success(request, "Message envoyé!")
            return redirect('messages:conversation_detail', conversation_id=conversation_id)

    # Marquer les messages comme lus
    ConversationMessage.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    # Récupérer les messages (du plus ancien au plus récent)
    conversation_messages = conversation.user_messages.order_by('created_at')
    print(f"Nombre de messages: {conversation_messages.count()}")  # Debug
    print(f"Messages: {list(conversation_messages)}")  # Debug

    # Déterminer l'autre utilisateur
    other_user = conversation.artisan if request.user == conversation.client else conversation.client

    context = {
        'conversation': conversation,
        'conversation_messages': conversation_messages,
        'other_user': other_user,
    }

    return render(request, 'user_messages/conversation_detail.html', context)


@login_required
def start_conversation(request, user_id):
    """Démarrer une nouvelle conversation"""
    other_user = get_object_or_404(User, id=user_id)

    # Vérifier qu'on ne démarre pas une conversation avec soi-même
    if other_user == request.user:
        flash_messages.error(request, "Vous ne pouvez pas démarrer une conversation avec vous-même.")
        return redirect('messages:inbox')

    # Déterminer qui est le client et qui est l'artisan
    if request.user.is_client() and other_user.is_artisan():
        client = request.user
        artisan = other_user
    elif request.user.is_artisan() and other_user.is_client():
        client = other_user
        artisan = request.user
    else:
        flash_messages.error(request, "Conversation impossible entre ces utilisateurs.")
        return redirect('messages:inbox')

    # Créer ou récupérer la conversation
    conversation, created = Conversation.objects.get_or_create(
        client=client,
        artisan=artisan
    )

    if created:
        flash_messages.success(request, "Conversation créée!")

    return redirect('messages:conversation_detail', conversation_id=conversation.id)