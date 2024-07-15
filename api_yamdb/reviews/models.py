from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.model):
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Genre(models.model):
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Title(models.model):
    name = models.CharField(
        max_length=256,
    )
    year = models.IntegerField()
    description = models.TextField(
        blank=True,
        null=True,
        default=None,
    )
    category = models.OneToOneField(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name


class Review(models.model):
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.text[:10]


class Comment(models.model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.text[:10]
