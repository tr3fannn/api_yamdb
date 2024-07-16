from django.db.models import Avg
from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def update(self, request, *args, **kwargs):
        return Response(
            "Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            "Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED
        )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSetListCreate(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TitleCreateSerializer
        return TitleSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        name = self.request.query_params.get('name')
        year = self.request.query_params.get('year')
        if category:
            queryset = queryset.filter(category__slug=category)
        if genre:
            queryset = queryset.filter(genre__slug=genre)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if year:
            queryset = queryset.filter(year=year)
        return queryset


class TitleViewSetDetail(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Title.objects.all()
    lookup_url_kwarg = 'title_id'
    serializer_class = TitleSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'PATCH':
    #         return TitleSerializer
    #     return TitleCreateSerializer

    def perform_update(self, request, *args, **kwargs):
        return Response(
            "Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def dispatch(self, request, *args, **kwargs):
        # if request.method not in SAFE_METHODS:
        #     if Review.objects.filter(author=self.request.user):
        #         return Response(
        #             "User already has a review", status.HTTP_400_BAD_REQUEST
        #         )
        return super().dispatch(request, *args, **kwargs)

    def _get_special_title(self):
        return Title.objects.get(pk=self.kwargs.get('title_id'))

    def _update_title_rating(self):
        title = self._get_special_title()
        title.rating = title.reviews.aggregate(Avg('score')).get('score__avg')
        title.save()
        return title

    def get_queryset(self):
        return self._get_special_title().reviews.all()

    def perform_create(self, serializer):
        title = self._update_title_rating()
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title = self._update_title_rating()
        serializer.save(title=title)

    def perform_destroy(self, instance):
        self._update_title_rating()
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    model = Comment
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def _get_special_review(self):
        return Review.objects.get(pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self._get_special_review().comments.all()

    def perform_create(self, serializer):
        review = self._get_special_review()
        serializer.save(author=self.request.user, review=review)
