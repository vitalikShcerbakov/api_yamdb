from rest_framework import filters, mixins, viewsets

from reviews.models import Genre
from .serializers import GenreSerializer
from .permissions import IsAdminOrReadOnly


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
