from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMINISTRATOR = 'admin', 'Администратор'

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(validate_username, UnicodeUsernameValidator()),
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Укажите электронную почту',
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    role = models.CharField(
        max_length=50,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name='Роль',
        help_text='Выберите роль пользователя из списка',
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография',
        help_text='Напишите о себе',
    )
