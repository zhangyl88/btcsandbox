import socket
import requests

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token


# Account Manager
class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None, **other_fields):
        if not email:
            raise ValueError('Email is a required user field')

        if not username:
            raise ValueError('Username is a required user field')

        email = self.normalize_email(email)
        username = username.lower()
        
        user = self.model(
            username = username,
            email    = email, 
            **other_fields
        )

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, username, email, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_confirmed', True)

        return self.create_user(username, email, password, **other_fields)


# Account
class Account(AbstractBaseUser, PermissionsMixin):
    # basic informations
    username                = models.CharField(_('Username'), max_length=50, unique=True)
    email                   = models.EmailField(_('Email'), unique=True)
    fullname                = models.CharField(_('Full Name'), max_length=100, blank=True, null=True)


    # Auto Generated
    ip_address              = models.GenericIPAddressField(_('Ip Address'), blank=True, null=True)

    #~ Overrides
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)

    # Indicators
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_confirmed            = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)

    USERNAME_FIELD          = 'email'
    REQUIRED_FIELDS         = ['username']

    objects                 = AccountManager()

    class Meta:
        managed = True
        verbose_name        = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.username
    
    def confirm(self):
        self.is_confirmed = True
        self.save()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    

# Generates token for registered user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generator(sender, instance, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Preference.objects.create(user=instance)

        try:
            # Grabbing User IP Address
            ip_addr = requests.get('https://api.ipify.org/').text
            instance.ip_address = ip_addr
        
        except:
            instance.ip_address = socket.gethostbyname('localhost')

        instance.save()


# Account Confirmation OTP
class AccountConfirmationOTP(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code                    = models.PositiveIntegerField()
    is_used                 = models.BooleanField(default=False)

    timestamp               = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name        = 'Acccount Confirmation OTP'
        verbose_name_plural = 'Account Confirmation OTPs'

    def confirm(self):
        self.is_used = True
        self.save()

    def __str__(self):
        return f'{self.user.username}~{self.code}'


# Two Factor OTP
class TwoFactorOTP(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code                    = models.PositiveIntegerField()
    is_used                 = models.BooleanField(default=False)

    timestamp               = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Two Factor OTP'
        verbose_name_plural = 'Two Factor OTPs'

    def __str__(self):
        return f'{self.user.username}~{self.code}'


# Password OTP
class PasswordOTP(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code                    = models.PositiveIntegerField()
    is_used                 = models.BooleanField(default=False)

    timestamp               = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Password OTP'
        verbose_name_plural = 'Password OTPs'

    def __str__(self):
        return f'{self.user.uci}~{self.code}'


# Preferences
class Preference(models.Model):
    user                    = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Indicators
    two_factor_enabled      = models.BooleanField(_('2-Factor Enabled'), default=False)
    is_email_hidden         = models.BooleanField(default=True)
    private                 = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Account Preference'
        verbose_name_plural = 'Account Preferences'

    def __str__(self):
        return f'{self.user.username}'