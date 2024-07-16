from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'year')

    def get_queryset(self):
        queryset = Title.objects.all()
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        if category:
            queryset = queryset.filter(category__slug=category)
        if genre:
            queryset = queryset.filter(genre__slug=genre)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def _get_special_title(self):
        return Title.objects.get(pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self._get_special_title().reviews.all()

    def perform_create(self, serializer):
        title = self._get_special_title()
        serializer.save(author=self.request.user, title=title)


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
