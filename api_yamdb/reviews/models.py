from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models


class User(AbstractUser):
    """Модель, которая описывает пользователя."""

    class Roles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        unique=True,
        max_length=150,
        validators=(RegexValidator(regex=r'^[\w.@+-]+\Z'),),
        verbose_name='Имя Пользователя',
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Электронная Почта',
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        default=None,
        verbose_name='Имя',
    )
    second_name = models.CharField(
        max_length=150,
        null=True,
        default=None,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        null=True,
        default=None,
        verbose_name='О себе',
    )
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name='Роль',
    )
    code = models.CharField(
        max_length=150,
        null=True,
        default=None,
        verbose_name='Код',
    )



class Category(models.Model):
    """Модель, которая описывает категорию произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг',
        validators=(RegexValidator(regex=r'^[-a-zA-Z0-9_]+$'),),
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель, которая описывает жанр произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг',
        validators=(RegexValidator(regex=r'^[-a-zA-Z0-9_]+$'),),
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель, которая описывает произведение."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.IntegerField(
        verbose_name='Год',
    )
    rating = models.IntegerField(
        default=0,
        verbose_name='Рейтинг',
    )
    description = models.TextField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Описание',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель, которая описывает обзор произведения."""

    text = models.TextField(
        verbose_name='Текст',
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата Публикации',
    )
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    """Модель, которая описывает комментарий к обзору."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата Публикации',
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Обзор',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:10]
