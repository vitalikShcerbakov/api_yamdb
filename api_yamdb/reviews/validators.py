import re

from django.core.exceptions import ValidationError


def validate_username(name):
    REGEX_USERNAME = re.compile(r'^[\w.@+-]+')

    if name == 'me':
        raise ValidationError('Недопустимое имя "me". Придумайте другое имя.')
    if not REGEX_USERNAME.fullmatch(name):
        raise ValidationError('Letters, digits and @/./+/-/_ only.')
