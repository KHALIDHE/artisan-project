# clients/forms.py

from django import forms
from apps.requests.models import ServiceRequest
from apps.reviews.models import Review
from apps.categories.models import Category

class ServiceRequestForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        empty_label="Sélectionnez une catégorie",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Catégorie de service'
    )

    class Meta:
        model = ServiceRequest
        fields = [
            'title', 'description', 'category', 'urgency',
            'address', 'city', 'preferred_date', 'photos'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Réparation fuite robinet cuisine'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Décrivez en détail votre besoin...'
            }),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse complète',
                'id': 'address-input'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville'
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'photos': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'title': 'Titre de la demande',
            'description': 'Description détaillée',
            'urgency': 'Urgence',
            'address': 'Adresse',
            'city': 'Ville',
            'preferred_date': 'Date souhaitée',
            'photos': 'Photos (optionnel)',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'photo1', 'photo2', 'photo3']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, f'{i} étoile{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-check-input'}
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Partagez votre expérience avec cet artisan...'
            }),
            'photo1': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'photo2': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'photo3': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'rating': 'Note',
            'comment': 'Votre avis',
            'photo1': 'Photo 1 (optionnel)',
            'photo2': 'Photo 2 (optionnel)',
            'photo3': 'Photo 3 (optionnel)',
        }


class ArtisanSearchForm(forms.Form):
    DISTANCE_CHOICES = (
        ('5', 'Dans un rayon de 5 km'),
        ('10', 'Dans un rayon de 10 km'),
        ('20', 'Dans un rayon de 20 km'),
        ('50', 'Dans un rayon de 50 km'),
        ('100', 'Dans un rayon de 100 km'),
    )

    RATING_CHOICES = (
        ('', 'Toutes les notes'),
        ('4', '4+ étoiles'),
        ('3', '3+ étoiles'),
        ('2', '2+ étoiles'),
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ville'
        })
    )

    distance = forms.ChoiceField(
        choices=DISTANCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    min_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Note minimale'
    )

    available_only = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Disponibles uniquement'
    )