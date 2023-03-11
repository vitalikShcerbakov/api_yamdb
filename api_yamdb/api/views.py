from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from api.serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWrightSerializer)
from .permissions import (IsAdmimOrSuperUser, IsAdminOrSuperUserOrReadOnly,
                          IsModerator)



class CommentViewSet(viewsets.ModelViewSet):
    """Представление для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsModerator)

    def get_review_id(self):
        return self.kwargs.get('review_id')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.get_review_id()))

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
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Представление для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsModerator)

    def get_title_id(self):
        return self.kwargs.get('title_id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.get_title_id())
        serializer.save(
            author=self.request.user,
            title=title)

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title_id())


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Представление для категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)


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
