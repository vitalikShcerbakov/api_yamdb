import uuid

from django.core.mail import send_mail

from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import IsAdmimOrSuperUser
from api_yamdb.settings import ADMIN_EMAIL
from users.models import User
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer


class TokenViewSet(TokenObtainPairView):
    """Получение токена"""
    serializer_class = TokenSerializer


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Регистрация пользователя"""
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            if ('non_field_errors' in serializer.errors
                and serializer.errors[
                    'non_field_errors'][0].code == status.HTTP_200_OK):
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)
        instance = serializer.save()
        instance.set_unusable_password()
        instance.save()
        email = serializer.validated_data['email']
        code = uuid.uuid4()
        send_mail(
            subject='Код подтверждения регистрации.'
                    'Email Confirmation Code',
            message=f'Код подтверждения email: {code}',
            from_email=ADMIN_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        instance.confirmation_code = code
        instance.save()
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
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
