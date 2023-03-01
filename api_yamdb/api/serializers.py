from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанра."""
    slug = serializers.SlugField(
        validators=[
            UniqueValidator(
                queryset=Genre.objects.all(),
                message=('Такое значение поле slug уже есть. '
                         'Поле должно быть уникальным.')
            ),
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message=('Ваше значение поля не соответствует требованиям.'),
            )
        ]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        # lookup_field - поле для поиска объектов отдельных экземпляров модели.
        # (По умолчанию 'pk') Должно указываться в сериаизаторе и во вьюхе
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории."""
    slug = serializers.SlugField(
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(),
                message=('Такое значение поле slug уже есть. '
                         'Поле должно быть уникальным.')
            ),
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message=('Ваше значение поля не соответствует требованиям.'),
            )
        ]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведения."""
    description = serializers.TimeField(required=False)
    

    class Meta:
        model = Title
        fields = '__all__'
