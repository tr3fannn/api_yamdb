from django.urls import include, path

from .views import (
    CategoryViewSet,
    CommentViewSet,
    CreateUserView,
    GenreViewSet,
    ObtainTokenView,
    ReviewViewSet,
    TitleViewSetDetail,
    TitleViewSetListCreate,
    UserViewSet,
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

comment = [
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/',
        CommentViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
    ),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/<int:comment_id>/',
        CommentViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
    ),
]

review = [
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
        'titles/<int:title_id>/reviews/<int:review_id>/',
        ReviewViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
    ),
]

title = [
    path(
        'titles/',
        TitleViewSetListCreate.as_view(
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
    path('', include(comment)),
    path('', include(review)),
    path('', include(title)),
]
