from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


ROLES = (
    ('USER', 'Пользователь'),
    ('MODERATOR', 'Модератор'),
    ('ADMIN', 'Администратор')
)

class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        validators=[validate_username],
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Email'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        max_length=16,
        choices=ROLES
    )

