from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSetDetail,
    TitleViewSetListCreate,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSetListCreate, basename='titles')

urlpatterns = [
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/<int:pk>/',
        CommentViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
    ),
    path(
        'titles/<int:title_id>/reviews/<int:pk>/comments/',
        CommentViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
    ),
    path(
        'titles/<int:title_id>/reviews/<int:pk>/',
        ReviewViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
    ),
    path(
        'titles/<int:title_id>/reviews/',
        ReviewViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
    ),
    path(
        'titles/<int:title_id>/',
        TitleViewSetDetail.as_view(
            {
                'get': 'retrieve',
                'put': 'perform_update',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
    ),
    path('', include(router.urls)),
]
