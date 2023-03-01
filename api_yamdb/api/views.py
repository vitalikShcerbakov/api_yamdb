from rest_framework import filters, mixins, viewsets

from reviews.models import Comment, Genre
from .permissions import AuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import CommentSerializer, GenreSerializer


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
