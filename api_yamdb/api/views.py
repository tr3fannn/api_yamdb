from secrets import token_hex

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import permissions
from rest_framework import views
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import (
    Category,
    Genre,
)
from .serializers import (
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
)

User = get_user_model()


class CreateUserView(views.APIView):
    """Класс для регистрации пользователей в проекте."""

    def _manage_code(self, username, email):
        """Отправка кода подтверждения и привязка его к пользователю."""
        code = token_hex(16)
        send_mail(
            'Регистрация на YamDB',
            f'{code}',
            'YamDB@ya.ru',
            [email]
        )
        user = User.objects.get(username=username, email=email)
        user.code = code
        user.save()

    def post(self, request):
        """Логика регистрации нового пользователя."""
        username = request.data.get('username')
        email = request.data.get('email')
        if username == 'me':
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

        response = Response(data={'email': email, 'username': username})

        if User.objects.filter(username=username, email=email).exists():
            return response

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self._manage_code(username, email)
            return response
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ObtainTokenView(views.APIView):
    """Класс для получения JWT токена."""

    def post(self, request):
        """Логика получения токена."""
        username = request.data.get('username')
        code = request.data.get('confirmation_code')
        if username is None or code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        obj = get_object_or_404(User, username=username)
        if obj.code != code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken.for_user(obj)
        return Response(
            data={
                'token': str(token.access_token),
            },
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer


class CategoryGenreBaseViewSet(viewsets.ModelViewSet):
    """Базовый ViewSet для категорий и жанров."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        """Проверка прав POST при запросе."""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role in ('user', 'moderator'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Проверка прав PATCH при запросе."""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role in ('user', 'moderator'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """Проверка прав DELETE при запросе."""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role in ('user', 'moderator'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(CategoryGenreBaseViewSet):
    """ViewSet для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'cat_slug'


class GenreViewSet(CategoryGenreBaseViewSet):
    """ViewSet для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_url_kwarg = 'gen_slug'
