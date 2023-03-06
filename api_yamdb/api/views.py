import uuid

from django.core.mail import send_mail
from rest_framework import filters, mixins, status,viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Comment, Genre
from .permissions import AuthorOrReadOnly, IsAdminOrReadOnly, IsAdmimOrSuperUser
from .serializers import (CommentSerializer, EditProfileSerializer,
                          GenreSerializer, SignupSerializer,
                          TokenSerializer, UserSerializer)

from users.models import User


class TokenViewSet(TokenObtainPairView):
    """Получение токена"""
    serializer_class = TokenSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review=review_id)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Жанры."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # lookup_field - поле для поиска объектов отдельных экземпляров модели.
    # (По умолчанию 'pk')
    lookup_field = 'slug'
    # Разрешает создавать и удалять только админу:
    # Пока закомментировала, не очень понимаю,
    # что там у юзера будет в свойствах
    # permission_classes = (IsAdminOrReadOnly,)


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Регистрация пользователя"""

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        username = serializer.initial_data.get('username')
        email = serializer.initial_data.get('email')

        if User.objects.filter(username=username).exists():
            instance = User.objects.get(username=username)
            if instance.email != email:
                raise ValidationError('Неправильная почта пользователя!')
            serializer.is_valid(raise_exception=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.set_unusable_password()
        instance.save()
        email = serializer.validated_data['email']

        code = uuid.uuid4()
        send_mail(
            subject='Код подтверждения регистрации. Email Confirmation Code',
            message=f'Код подтверждения email: {code}',
            from_email='noreply@yamdb.com',
            recipient_list=[email],
            fail_silently=False,
        )
        instance.confirmation_code = code
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Cписок всех пользователей. Права доступа: Администратор"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)  # ТЗ: Поиск по имени пользователя (username)
    lookup_field = 'username'
    permission_classes = (IsAdmimOrSuperUser,)
