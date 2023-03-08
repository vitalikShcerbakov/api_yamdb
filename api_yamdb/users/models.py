from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import validate_username


class User(AbstractUser):
    """Модель Пользователя"""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    REQUIRED_FIELDS = ['email', 'password']

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail',
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография",
    )
    role = models.CharField(
        max_length=25,
        choices=ROLE,
        default=USER,
        verbose_name="Роль пользователя",
    )
    confirmation_code = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Код потдверждения",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]



