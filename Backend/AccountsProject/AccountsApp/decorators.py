import functools
import jwt
from django.conf import settings
from rest_framework import exceptions, status

from AccountsApp.services.token.mail_token import check_token
from AccountsApp.serializers import TokenSerializer


def exception_jwt(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed(
                {'error_token': '14'}, #settings.ERRORS['token_error']['14']
                code=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                {'error_token': '15'}, #settings.ERRORS['token_error']['15']
                code=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed(
                {'error_token': '16'}, #settings.ERRORS['token_error']['16']
                code=status.HTTP_401_UNAUTHORIZED
            )

        return result

    return wrapper


def permission_is_auth_tmp_token(is_password=False, type_request='POST', raise_exception=True):

    def decorator(func):
        from AccountsApp.services.user_view import find_or_get_user_model

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            print(args, kwargs)
            if type_request.lower() == 'post':
                data = args[1].data
            elif type_request.lower() == 'get':
                data = args[1].GET
            print(data)
            # serializer = TokenSerializer(data=args[1].data)
            serializer = TokenSerializer(data=data)
            if not raise_exception:
                serializer.is_valid()
                kwargs['result_field'] = '1'
            else:
                serializer.is_valid(raise_exception=True)

            token = serializer.data.get('token')

            user = find_or_get_user_model(
                email=serializer.data.get('email'),
                uuid=serializer.data.get('uuid'),
                # **serializer.data
                raise_exception=raise_exception
            )
            # print(user)
            # print(token)
            if not check_token(user, token, is_password):
                if not raise_exception:
                    kwargs['result_field'] = '1'
                else:
                    raise exceptions.AuthenticationFailed(
                        {'available_tmp_error': '17'},#settings.ERRORS['available_tmp_error']['17']},
                        code=status.HTTP_401_UNAUTHORIZED
                    )
            kwargs['type_user'] = user.type_user
            # print(kwargs)
            # print(zip(kwargs))
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
