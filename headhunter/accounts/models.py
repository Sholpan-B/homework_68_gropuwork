from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission, AbstractUser
from django.db import models
from django.db.models import TextChoices


class RoleChoice(TextChoices):
    CANDIDATE = 'CANDIDATE', 'CANDIDATE'
    EMPLOYER = 'EMPLOYER', 'EMPLOYER'


class CustomUser(AbstractUser):
    username = models.CharField(verbose_name='Username', unique=True, null=False, blank=False)
    email = models.EmailField(verbose_name='Email', unique=True, null=False, blank=False)
    role = models.CharField(
        choices=RoleChoice.choices,
        verbose_name='Role',
        max_length=10,
        null=False,
        blank=False,
        default=RoleChoice.CANDIDATE
    )
    profile_photo = models.ImageField(
        null=True,
        blank=True,
        upload_to='profile_photos',
        verbose_name='Profile photo',
        default='default_photo.jpg'
    )
    phone = models.CharField(verbose_name='Phone number', max_length=20, null=False, blank=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


