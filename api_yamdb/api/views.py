import uuid

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Comment, Genre, Reviews, Title
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, IsAdmimOrSuperUser, IsModerator
from .serializers import (CommentSerializer, EditProfileSerializer,
                          ReviewSerializer, GenreSerializer, SignupSerializer,)
from .serializers import (CategorySerializer, CommentSerializer,
                          EditProfileSerializer, GenreSerializer,
                          ReviewSerializer, SignupSerializer,
                          TitleReadSerializer, TitleWrightSerializer,
                          TokenSerializer, UserSerializer)

from users.models import User


class TokenViewSet(TokenObtainPairView):
    """Получение токена"""
    serializer_class = TokenSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsModerator,)

    def get_review_id(self):
        return self.kwargs.get('review_id')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=Reviews.objects.get(pk=self.get_review_id()))

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review_id())


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Представление для жанра."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdmimOrSuperUser,)

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return super().get_permissions()


class ReviewsViewSet(viewsets.ModelViewSet):
    """Представление для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsModerator,)

    def get_title_id(self):
        return self.kwargs.get('titles_id')

    def perform_create(self, serializer):
        title = Title.objects.get(pk=self.get_title_id())
        serializer.save(
            author=self.request.user,
            titles=title)

    def get_queryset(self):
        return Reviews.objects.filter(titles=self.get_title_id())


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


class UserViewEditProfile(APIView):
    """Просмотр и редактирование своего профиля"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = EditProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        instance = User.objects.get(username=request.user)
        serializer = EditProfileSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Cписок всех пользователей. Права доступа: Администратор"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)  # ТЗ: Поиск по имени пользователя (username)
    lookup_field = 'username'
    permission_classes = (IsAdmimOrSuperUser,)

    def update(self, request, *args, **kwargs):
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Представление для категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdmimOrSuperUser,)

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для произведения."""
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdmimOrSuperUser,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWrightSerializer
    
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        return super().get_permissions()