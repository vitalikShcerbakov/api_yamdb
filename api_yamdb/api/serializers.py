import datetime as dt

from django.core.validators import RegexValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Reviews, Title
from users.models import User


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
        model = Genre,
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        user = self.context['requests'].user
        title = self.context['requests'].title
        if Reviews.objects.filter(author=user, titles=title).exists():
            raise serializers.ValidationError('Пользователь может оставить только один отзыв на произведение.')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

        def validete_email(self, data):
            if data == self.context['request'].user:
                raise serializers.ValidationError(
                    'Пользователь с таким email уже зарегистрирован!'
                )
            return data


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('username','email', 'role')


class TokenSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields['confirmation_code'] = serializers.CharField(required=False)
        self.fields['password'] = serializers.HiddenField(default='')

    def validate(self, attrs):
        self.user = get_object_or_404(User, username=attrs['username'])
        if self.user.confirmation_code != attrs['confirmation_code']:
            raise serializers.ValidationError('Неправильный код подтверждения!')
        data = str(self.get_token(self.user))
        return {'token': data}


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

        def validate_email(self, data):
            if data == self.context['request'].user:
                raise serializers.ValidationError(
                    'Этот email уже зарегистрирован'
                )
            return data

        def validate_username(self, data):
            if data == 'me':
                raise serializers.ValidationError(
                    'Имя "me" запрещено. Дайте другое имя.'
                )
            return data
        

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
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        # Возвращает среднюю оценку по отзывам
        return (Reviews.objects.filter(titles__id=obj.id).
                aggregate(Avg('score'))).get('score__avg')


class TitleWrightSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и изменения произведения."""

    description = serializers.TimeField(required=False)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        # Проверяет год выпуска произведения
        year = dt.datetime.now().date().year
        if not (0 < value <= year):
            raise serializers.ValidationError('Проверьте год выпуска')
        return value
