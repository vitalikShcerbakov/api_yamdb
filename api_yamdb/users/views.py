import uuid

from api.permissions import IsAdmimOrSuperUser
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer

from reviews.validators import validate_username
from rest_framework.views import APIView
class TokenViewSet(TokenObtainPairView):
    """Получение токена"""
    serializer_class = TokenSerializer


class SignUpViewSet(APIView):
    """Регистрация пользователя"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        try:
            username = validate_username(serializer.data['username'])
            print(username)
            print('*' * 100)
        except ValidationError as e:
             return Response(e, status=status.HTTP_400_BAD_REQUEST)

        user, _ = User.objects.get_or_create(username=username, email=email)

        email = serializer.validated_data['email']
        code = uuid.uuid4()
        send_mail(
            subject='Код подтверждения регистрации.'
                    'Email Confirmation Code',
            message=f'Код подтверждения email: {code}',
            from_email='noreply@yamdb.com',
            recipient_list=[email],
            fail_silently=False,
        )
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Cписок всех пользователей. Права доступа: Администратор"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsAdmimOrSuperUser,)
    http_method_names = ('head', 'get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer)
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
