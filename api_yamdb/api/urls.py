from django.urls import include, path
from users.views import UserViewSet, singup, token_jwt

urlpatterns = [
    path('v1/auth/signup/', singup, name='singup'),
    path('v1/auth/token/', token_jwt, name='token')
]