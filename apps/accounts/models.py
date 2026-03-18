# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):#This class tells Django how to create users
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('artisan', 'Artisan'),
        ('admin', 'Administrateur'),
    )

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = PhoneNumberField(blank=True, null=True, verbose_name='Téléphone')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, verbose_name='Type utilisateur')

    # Localisation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, verbose_name='Ville')
    address = models.CharField(max_length=255, blank=True, verbose_name='Adresse')

    # Statut
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.email

    def is_client(self):
        return self.user_type == 'client'

    def is_artisan(self):
        return self.user_type == 'artisan'