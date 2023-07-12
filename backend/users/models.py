from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_validation


class CustomUser(AbstractUser):
    '''Custom user model'''
    email = models.EmailField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Электронная почта',
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        validators=[username_validation, ],
        verbose_name='Имя пользователя'
    )

    first_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Пароль'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_users'
            ),
        ]
