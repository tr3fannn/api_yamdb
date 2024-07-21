# Generated by Django 3.2 on 2024-07-21 12:53

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(help_text='Имя Пользователя', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(regex='^[\\w.@+-]+\\Z')], verbose_name='Имя Пользователя')),
                ('email', models.EmailField(help_text='Электронная Почта', max_length=254, unique=True, verbose_name='Электронная Почта')),
                ('first_name', models.CharField(default=None, help_text='Имя Пользователя', max_length=150, null=True, verbose_name='Имя')),
                ('second_name', models.CharField(default=None, help_text='Фамилия Пользователя', max_length=150, null=True, verbose_name='Фамилия')),
                ('bio', models.TextField(default=None, help_text='О себе Пользователя', null=True, verbose_name='О себе')),
                ('role', models.CharField(choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', help_text='Роль Пользователя', max_length=9, verbose_name='Роль')),
                ('code', models.CharField(default=None, help_text='Код для регистрации пользователя', max_length=50, null=True, verbose_name='Код')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название категории произведения', max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(help_text='Слаг категории произведения', unique=True, validators=[django.core.validators.RegexValidator(regex='^[-a-zA-Z0-9_]+$')], verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название жанра произведения', max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(help_text='Слаг жанра произведения', unique=True, validators=[django.core.validators.RegexValidator(regex='^[-a-zA-Z0-9_]+$')], verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название произведения', max_length=256, verbose_name='Название')),
                ('year', models.IntegerField(help_text='Год выпуска произведения', verbose_name='Год')),
                ('description', models.TextField(blank=True, default=None, help_text='Описание произведения', null=True, verbose_name='Описание')),
                ('category', models.ForeignKey(help_text='Категория произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(help_text='Жанр произведения', related_name='titles', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Текст обзора произведения', verbose_name='Текст')),
                ('score', models.PositiveSmallIntegerField(help_text='Оценка произведения от 1 до 10', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата публикации обзора произведения', verbose_name='Дата Публикации')),
                ('author', models.ForeignKey(help_text='Автор обзора произведения', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('title', models.ForeignKey(help_text='Произведение, оцениваемое обзором', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'Обзор',
                'verbose_name_plural': 'Обзоры',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Текст комментария', verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата публикации комментария', verbose_name='Дата Публикации')),
                ('author', models.ForeignKey(help_text='Автор комментария', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('review', models.ForeignKey(help_text='Обзор, комментируемый комментарий', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Обзор')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_review'),
        ),
    ]