from django.urls import path, include

from .views import (
    CreateUserView,
    ObtainTokenView,
    UserViewSet,
    CategoryViewSet,
    GenreViewSet,
)

app_name = 'api_v1'

users = [
    path('auth/signup/', CreateUserView.as_view()),
    path('auth/token/', ObtainTokenView.as_view()),
    path(
        'users/',
        UserViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
    ),
    path(
        'users/<str:username>/',
        UserViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
    ),
    path(
        'users/me/',
        UserViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
            }
        ),
    ),
]

category = [
    path(
        'categories/',
        CategoryViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
    ),
    path(
        'categories/<slug:cat_slug>/',
        CategoryViewSet.as_view(
            {
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
    ),
]

genre = [
    path(
        'genres/',
        GenreViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
    ),
    path(
        'genres/<slug:gen_slug>/',
        GenreViewSet.as_view(
            {
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
    ),
]

urlpatterns = [
    path('', include(users)),
    path('', include(category)),
    path('', include(genre)),
]
