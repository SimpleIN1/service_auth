import functools
import jwt
from django.conf import settings
from rest_framework import exceptions, status


def exception_jwt(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed(
                {'error_token': settings.ERRORS['token_error']['11']},
                code=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                {'error_token': settings.ERRORS['token_error']['12']},
                code=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed(
                {'error_token': settings.ERRORS['token_error']['13']},
                code=status.HTTP_401_UNAUTHORIZED
            )

        return result

    return inner_func



