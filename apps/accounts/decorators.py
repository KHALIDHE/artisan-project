# accounts/decorators.py
"""
===========================================================
 Custom Role-Based Access Decorators for the Accounts App
===========================================================

This file defines three custom decorators used to restrict
access to certain views based on the type of user currently
logged in. They centralize all permission logic to keep
views clean, readable, and secure.

Why this file exists:
---------------------
In this project, users can have different roles:
    - Client
    - Artisan
    - Administrator (Django staff)

Each role has access to different pages. Instead of manually
checking permissions inside every view, we use decorators
to automatically enforce access control.

General behavior of each decorator:
-----------------------------------
1. Check if the user is authenticated.
    - If NOT authenticated → redirect to the login page
      and display a warning message.

2. Check if the user has the required role.
    - Client pages require: user.is_client()
    - Artisan pages require: user.is_artisan()
    - Admin pages require: user.is_staff
    - If role is incorrect → redirect to homepage
      and show an error message.

3. If all checks pass, the original view function is executed.

Benefits of using decorators:
-----------------------------
• Keeps views much shorter and easier to maintain
• Avoids repeating the same permission checks everywhere
• Provides centralized and consistent access control
• Makes the project more secure and easier to scale

Usage example:
--------------
    from accounts.decorators import client_required

    @client_required
    def client_dashboard(request):
        return render(request, "client/dashboard.html")

Each decorator wraps the target view using @wraps to
preserve its metadata (name, docstrings, etc.).

===========================================================
"""

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def client_required(view_func):
    """
    Decorator pour les vues réservées aux clients
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Vous devez être connecté pour accéder à cette page.')
            return redirect('accounts:login')

        if not request.user.is_client():
            messages.error(request, 'Cette page est réservée aux clients.')
            return redirect('accounts:home')

        return view_func(request, *args, **kwargs)
    return wrapper


def artisan_required(view_func):
    """
    Decorator pour les vues réservées aux artisans
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Vous devez être connecté pour accéder à cette page.')
            return redirect('accounts:login')

        if not request.user.is_artisan():
            messages.error(request, 'Cette page est réservée aux artisans.')
            return redirect('accounts:home')

        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Decorator pour les vues réservées aux administrateurs
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Vous devez être connecté pour accéder à cette page.')
            return redirect('accounts:login')

        if not request.user.is_staff:
            messages.error(request, 'Cette page est réservée aux administrateurs.')
            return redirect('accounts:home')

        return view_func(request, *args, **kwargs)
    return wrapper