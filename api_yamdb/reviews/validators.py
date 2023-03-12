import re

from django.core.exceptions import ValidationError


def validate_username(name):
    regex_username = re.compile(r'^[\w.@+-]+')
    if name == 'me':
        raise ValidationError('Недопустимое имя "me". Придумайте другое имя.')
    if not regex_username.fullmatch(name):
        raise ValidationError('Letters, digits and @/./+/-/_ only.')
