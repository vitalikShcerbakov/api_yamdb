from django.utils import timezone

from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
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
                regex='^[-a-zA-Z0-9_]{1,50}$',
                message=('Ваше значение поля не соответствует требованиям. '
                         'Поле должно содержать до 50 знаков, состоящих из '
                         'букв латинского алфавита, цифр, '
                         'подчеркивания или дефиса.'),
            )
        ]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        user = self.context['request'].user
        title = self.context.get(
            'request').parser_context.get('kwargs').get('title_id')
        if Review.objects.filter(author=user, title=title).exists():
            raise serializers.ValidationError(
                'Пользователь может оставить только'
                'один отзыв на произведение.')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


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
                regex='^[-a-zA-Z0-9_]{1,50}$',
                message=('Ваше значение поля не соответствует требованиям. '
                         'Поле должно содержать до 50 знаков, состоящих из '
                         'букв латинского алфавита, цифр, '
                         'подчеркивания или дефиса.'),
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
    rating = serializers.IntegerField()
    rating = serializers.IntegerField()
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleWrightSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и изменения произведения."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category', )

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'Проверьте год выпуска, '
                'он не может быть больше текущего года.')
        return value
    
    def to_representation(self, instance):
        instance.rating = 0
        serializer =  TitleReadSerializer(instance)
        return serializer.data
