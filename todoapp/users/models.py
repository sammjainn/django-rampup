from __future__ import unicode_literals
from email.policy import default
from multiprocessing.sharedctypes import Value

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """
    Add manager methods here to create user and super user
    """

    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **other_fields)

        user.set_password(make_password(password))
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        user = self.create_user(
            email,
            password=password,
            **other_fields
        )
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Needed fields
    - password (already inherited from AbstractBaseUser; encrypt password before saving to database)
    - last_login (already inherited from AbstractBaseUser)
    - is_superuser
    - first_name (max_length=30)
    - email (should be unique)
    - is_staff
    - date_joined (default should be time of object creation)
    - last_name (max_length=150)
    """

    email = models.EmailField(unique=True, max_length=255)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        default=timezone.now, null=True)
    last_name = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
