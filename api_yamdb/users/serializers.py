from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

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
        max_length=254
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username])

    def validate(self, data):
        username = data['username']
        email = data['email']
        if User.objects.filter(username=username, email=email).exists():
            raise ValidationError(
                'Такие username и email уже зарегистрированы',
                code=status.HTTP_200_OK)
        elif User.objects.filter(username=username).exists():
            instance = User.objects.get(username=username)
            if email != instance.email:
                raise ValidationError(
                    'Неправильная почта пользователя!',
                    code=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'Пользователь с таким email уже зарегистрирован',
                code=status.HTTP_400_BAD_REQUEST)

        return data

    class Meta:
        model = User
        fields = ('username', 'email')
