import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(name):
    regex_username = re.compile(r'^[\w.@+-]+')
    if name.lower() == 'me':
        raise ValidationError('Недопустимое имя "me". Придумайте другое имя.')
    if not regex_username.fullmatch(name):
        raise ValidationError('Letters, digits and @/./+/-/_ only.')


def year_validator(value):
    if value > int(timezone.now().year):
        raise ValidationError(
            ('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
