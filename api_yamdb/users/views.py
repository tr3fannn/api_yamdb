from rest_framework import status

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import (SignUpSerializer, TokenSerializer,
                                     UserSerializer)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def singup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="Регистрация на YamDB",
        message=f"Код для токена: {confirmation_code}",
        from_email=None,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def token_jwt(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username', ]
    lookup_field = 'username'

    @action(detail=False,
            methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated, ]) # Дописать пермишен IsAdmin
    def me(self, request):
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)
        if request.user.role == 'admin' or request.user.role == 'moderator':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=OK)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')
        return Response(serializer.data, status=OK)