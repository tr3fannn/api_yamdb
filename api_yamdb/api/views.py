from secrets import token_hex

from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    views,
    viewsets,
)
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .permissions import AdminOnlyExceptUpdateDestroy, IsOwnerOrModerOrAdmin
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    UserSerializer,
)
from .utils import (
    check_admin_permission,
    check_authentication,
    check_self_action,
)

User = get_user_model()


class CreateUserView(views.APIView):
    """Класс для регистрации пользователей в проекте."""

    def _manage_code(self, username, email):
        """Отправка кода подтверждения и привязка его к пользователю."""
        code = token_hex(16)
        user = User.objects.get(username=username, email=email)
        user.code = code
        user.save()
        send_mail('Регистрация на YamDB', f'{code}', None, [email])

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
    permission_classes = (AdminOnlyExceptUpdateDestroy,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    def get_permissions(self):
        if self.action == 'retrieve':
            if self.kwargs.get('username') == 'me':
                return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def retrieve(self, request, username):
        if username == 'me':
            me = get_object_or_404(User, pk=request.user.id)
            serializer = self.get_serializer(me)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().retrieve(request, username)

    def partial_update(self, request, username):
        if username == 'me':
            me = get_object_or_404(User, pk=request.user.id)
            data = request.data.copy()
            if 'role' in data and not request.user.is_superuser:
                data['role'] = me.role
            serializer = self.get_serializer(me, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().partial_update(request, username)

    def destroy(self, request, username):
        if username == 'me':
            return Response(
                {'error': 'Нельзя удалить себя!'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, username)


class CategoryGenreBaseViewSet(viewsets.ModelViewSet):
    """Базовый ViewSet для категорий и жанров."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        """
        Проверка прав при создании объекта.
        """
        if error_response := check_admin_permission(request):
            return error_response
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Запрещает обновление объектов.
        """
        if error_response := check_admin_permission(request):
            return error_response
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """
        Проверка прав при удалении объекта.
        """
        if error_response := check_admin_permission(request):
            return error_response
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(CategoryGenreBaseViewSet):
    """ViewSet для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'cat_slug'
    search_fields = ('name',)


class GenreViewSet(CategoryGenreBaseViewSet):
    """ViewSet для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_url_kwarg = 'gen_slug'
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    serializer_class = ReviewSerializer
    lookup_url_kwarg = 'review_id'

    def _get_special_title(self):
        """Логика получения произведения."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Логика получения отзывов."""
        return self._get_special_title().reviews.all()

    def perform_create(self, serializer):
        """
        Логика создания отзыва.
        """
        title = self._get_special_title()
        if title.reviews.filter(author=self.request.user).exists():
            raise ValidationError(
                detail='Вы уже имеете отзыв на это произведение!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(author=self.request.user, title=title)

    def create(self, request, *args, **kwargs):
        """
        Проверка прав при создании отзыва.
        """
        if error_response := check_authentication(self.request):
            return error_response
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Логика обновления отзыва.
        """
        if not (error_response := check_authentication(self.request)) is None:
            return error_response
        if (
            not (
                error_response := check_self_action(
                    self.request, self.get_object().author
                )
            )
            is None
        ):
            raise error_response
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Логика удаления отзыва.
        """
        if not (error_response := check_authentication(self.request)) is None:
            return error_response
        if (
            not (
                error_response := check_self_action(
                    self.request, self.get_object().author
                )
            )
            is None
        ):
            raise error_response
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = (IsOwnerOrModerOrAdmin,)

    def _get_special_review(self):
        """Логика получения отзыва."""
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Логика получения комментариев."""
        return self._get_special_review().comments.all()

    def perform_create(self, serializer):
        """Логика создания комментария."""
        review = self._get_special_review()
        serializer.save(author=self.request.user, review=review)

    def partial_update(self, request, *args, **kwargs):
        """
        Логика обновления комментария.
        """
        if (
            not (
                error_response := check_self_action(
                    self.request, self.get_object().author
                )
            )
            is None
        ):
            raise error_response
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Логика удаления комментария.
        """
        if (
            not (
                error_response := check_self_action(
                    self.request, self.get_object().author
                )
            )
            is None
        ):
            raise error_response
        return super().destroy(request, *args, **kwargs)


class TitleViewSetDetail(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Класс ViewSet с миксинами для получения одного произведения
    и для изменения произведения.
    """

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    lookup_url_kwarg = 'title_id'

    def update(self, request, *args, **kwargs):
        if kwargs.get('partial') is False:
            return Response(
                "Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED
            )
        if resp_error := check_admin_permission(request):
            return resp_error
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if resp_error := check_admin_permission(request):
            return resp_error
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        """Метод определяющий какой сериализатор использовать."""
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleCreateSerializer


class TitleViewSetListCreate(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Класс ViewSet с миксинами для получения списка произведений
    и для создания произведений.
    """

    queryset = Title.objects.all()
    permissions = (AdminOnlyExceptUpdateDestroy,)
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_class = TitleFilter
    search_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        """Метод определяющий какой сериализатор использовать."""
        if self.request.method == 'POST':
            return TitleCreateSerializer
        return TitleSerializer

    def create(self, request, *args, **kwargs):
        """Метод создающий произведение."""
        if resp_error := check_admin_permission(request):
            return resp_error
        return super().create(request, *args, **kwargs)
