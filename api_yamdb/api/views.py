import datetime as dt

from rest_framework import filters, mixins, viewsets

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import IsAdminOrReadOnly


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Представление для жанра."""
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


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Представление для категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # permission_classes = (IsAdminOrReadOnly,)

class TitleViewSet(viewsets.ModelViewSet):
    """Представление для произведения."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def validate_year(self, value):
        year = dt.datetime.now().year()
