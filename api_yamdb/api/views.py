from rest_framework import filters, mixins, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Comment, Genre, Reviews
from .permissions import AuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import CommentSerializer, GenreSerializer, ReviewSerializer
from .serializers import (CommentSerializer, GenreSerializer, TokenSerializer,
                          UserSerializer)

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
    lookup_field = 'slug'
    # permission_classes = (IsAdminOrReadOnly,)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        titles_id = self.kwargs.get('titles_id')
        return Reviews.objects.filter(titles=titles_id)

    
class UserViewSet(viewsets.ModelViewSet):
    """Cписок всех пользователей. Права доступа: Администратор"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)  #ТЗ: Поиск по имени пользователя (username)
    lookup_field = 'username'
    # permission_classes = (IsAdminOrSuperUser,)

