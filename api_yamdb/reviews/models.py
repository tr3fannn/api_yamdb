from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

USER_NAME_LENGTH = 150
EMAIL_LENGTH = 254
NAME_LENGTH = 256
SLUG_LENGTH = 50
CURRENT_YEAR = date.today().year


class User(AbstractUser):
    """Модель, которая описывает пользователя."""

    class Roles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        unique=True,
        max_length=USER_NAME_LENGTH,
        validators=(RegexValidator(regex=r'^[\w.@+-]+\Z'),),
        verbose_name='Имя Пользователя',
        help_text='Имя Пользователя',
    )
    email = models.EmailField(
        unique=True,
        max_length=EMAIL_LENGTH,
        verbose_name='Электронная Почта',
        help_text='Электронная Почта',
    )
    first_name = models.CharField(
        max_length=USER_NAME_LENGTH,
        null=True,
        default=None,
        verbose_name='Имя',
        help_text='Имя Пользователя',
    )
    second_name = models.CharField(
        max_length=USER_NAME_LENGTH,
        null=True,
        default=None,
        verbose_name='Фамилия',
        help_text='Фамилия Пользователя',
    )
    bio = models.TextField(
        null=True,
        default=None,
        verbose_name='О себе',
        help_text='О себе Пользователя',
    )
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name='Роль',
        help_text='Роль Пользователя',
    )
    code = models.CharField(
        max_length=SLUG_LENGTH,
        null=True,
        default=None,
        verbose_name='Код',
        help_text='Код для регистрации пользователя',
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель, которая описывает категорию произведения."""

    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название',
        help_text='Название категории произведения',
    )
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        verbose_name='Слаг',
        validators=(RegexValidator(regex=r'^[-a-zA-Z0-9_]+$'),),
        help_text='Слаг категории произведения',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель, которая описывает произведение."""

    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название',
        help_text='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(CURRENT_YEAR),
        ],
        help_text='Год выпуска произведения',
    )
    rating = models.IntegerField(
        null=True,
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        help_text='Оценка произведения от 0 до 10',
    )
    description = models.TextField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Описание',
        help_text='Описание произведения',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        help_text='Категория произведения',
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='titles',
        verbose_name='Жанр',
        help_text='Жанр произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель, которая описывает жанр произведения."""

    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название',
        help_text='Название жанра произведения',
    )
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        verbose_name='Слаг',
        validators=(RegexValidator(regex=r'^[-a-zA-Z0-9_]+$'),),
        help_text='Слаг жанра произведения',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель, которая описывает обзор произведения."""

    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст обзора произведения',
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        verbose_name='Оценка',
        help_text='Оценка произведения от 1 до 10',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата Публикации',
        help_text='Дата публикации обзора произведения',
    )
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Автор обзора произведения',
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Произведение, оцениваемое обзором',
    )

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    """Модель, которая описывает комментарий к обзору."""

    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата Публикации',
        help_text='Дата публикации комментария',
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Обзор',
        help_text='Обзор, комментируемый комментарий',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:10]
