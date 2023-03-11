from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken
# from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_username
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User

        def validate_email(self, data):
            if data == self.context['request'].user:
                raise serializers.ValidationError(
                    'Пользователь с таким email уже зарегистрирован!'
                )
            return data


class TokenSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields['confirmation_code'] = serializers.CharField(
            required=False)
        self.fields['password'] = serializers.HiddenField(default='')

    def validate(self, attrs):
        self.user = get_object_or_404(User, username=attrs['username'])
        if self.user.confirmation_code != attrs['confirmation_code']:
            raise serializers.ValidationError(
                'Неправильный код подтверждения!'
            )
        data = str(self.get_token(self.user))
        return {'token': data}


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'email')

        def validate_email(self, data):
            if data == self.context['request'].user:
                raise serializers.ValidationError(
                    'Этот email уже зарегистрирован'
                )
            return data
