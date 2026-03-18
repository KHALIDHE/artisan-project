# artisans/forms.py

from django import forms
from .models import ArtisanProfile, PortfolioImage
from apps.categories.models import Category

class ArtisanProfileForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Catégories de services'
    )

    class Meta:
        model = ArtisanProfile
        fields = [
            'business_name', 'bio', 'categories', 'experience_years',
            'profile_photo', 'cover_photo', 'id_card', 'business_license',
            'is_available', 'availability_note'
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de votre entreprise'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Décrivez vos services, votre expérience...'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 50
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'cover_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'id_card': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'business_license': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'availability_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ex: Disponible du lundi au vendredi, 9h-18h'
            }),
        }
        labels = {
            'business_name': 'Nom de l\'entreprise',
            'bio': 'Biographie / Présentation',
            'experience_years': 'Années d\'expérience',
            'profile_photo': 'Photo de profil',
            'cover_photo': 'Photo de couverture',
            'id_card': 'Carte d\'identité',
            'business_license': 'Licence professionnelle',
            'is_available': 'Je suis disponible',
            'availability_note': 'Note de disponibilité',
        }


class PortfolioImageForm(forms.ModelForm):
    class Meta:
        model = PortfolioImage
        fields = ['image', 'title', 'description']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'image'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Description du travail réalisé'
            }),
        }
        labels = {
            'image': 'Image',
            'title': 'Titre',
            'description': 'Description',
        }


class ServiceRequestResponseForm(forms.Form):
    ACTION_CHOICES = (
        ('accept', 'Accepter'),
        ('reject', 'Rejeter'),
    )

    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    estimated_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Prix estimé (DH)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00'
        })
    )
    response_message = forms.CharField(
        required=False,
        label='Message pour le client',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ajoutez un message...'
        })
    )