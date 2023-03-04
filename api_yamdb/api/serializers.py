import datetime as dt

from django.core.validators import RegexValidator
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Title, Reviews


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', )
        model = Comment


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


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для произведения (только чтение)."""

    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
    
    def get_rating(self, obj):
        # Возвращает среднюю оценку по отзывам
        return (Reviews.objects.filter(titles__id=obj.id).aggregate(Avg('score'))).get('score__avg')


class TitleWrightSerializer(serializers.ModelSerializer):
    """Сериализатор дл добавления и изменения произведения."""

    description = serializers.TimeField(required=False)
    genre = serializers.SlugRelatedField(many=True, queryset=Genre.objects.all())
    rating = serializers.SerializerMethodField()
    category = CategorySerializer()


    def validate_year(self, value):
        # Проверяет год выпуска произведения
        year = dt.datetime.now().date().year()
        if not (0 < value <= year):
            raise serializers.ValidationError('Проверьте год выпуска')
        return value
