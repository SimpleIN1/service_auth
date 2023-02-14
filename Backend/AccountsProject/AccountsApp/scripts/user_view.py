from typing import Tuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import status, exceptions
from rest_framework.response import Response

from .jwt_token import Jwt
from .mail_send import EmailResetPassword, EmailVerify, RecoveryAccount

User = get_user_model()


class UserUpdateDestroyRetrieve:
    '''# RUD(read, update, delete) операции над пользователем #'''

    def __check_email(self, old_email, new_email, uuid):

        if old_email != new_email:
            token = Jwt.create_tmp_access_token(new_email)
            EmailVerify(email=new_email, context={
                'protocol': 'https',
                'site_name': 'fire-activity-map.com',
                'url': f'url?email={new_email}&'
                       f'token={token}&'
                       f'uuid={uuid}',
            }).send()
            return '9'
        return '11'

    def put_user(self, request, *args, **kwargs) -> Response:
        data = request.data
        user = request.user

        serializer = self.serializer_class(data=data, instance=user)
        serializer.is_valid(raise_exception=True)

        # password = request.data.get('password')
        # re_password = request.data.get('re_password')
        #

        code = self.__check_email(user.email, data.get('email'), user.uuid)


        serializer.save()
        return Response({'user_info': settings.ERRORS['user_info'][code],
                        'user_data': serializer.data},
                        status=status.HTTP_200_OK)

    def destroy_user(self, request, *args, **kwargs) -> Response:
        instance = request.user
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_user(self, request, *args, **kwargs) -> Response:
        data = self.serializer_class(request.user).data
        return Response(data, status=status.HTTP_200_OK)

    def patch_user(self, request, *args, **kwargs) -> Response:
        data = request.data
        user = request.user

        serializer = self.serializer_class(data=data, instance=user, partial=True)
        serializer.is_valid(raise_exception=True)

        code = self.__check_email(user.email, data.get('email'), user.uuid)

        serializer.save()

        return Response({'user_info': settings.ERRORS['user_info'][code],
                        'user_data': serializer.data},
                        status=status.HTTP_200_OK)


def find_or_get_user_model(**kwargs) -> User:
    '''# Проверка пользователя на то, что пользователь существует #'''

    try:
        user = User.objects.get(**kwargs)
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed(
            {'user_error': settings.ERRORS['user_error']['1']},
            code=status.HTTP_401_UNAUTHORIZED
        )
    return user


def is_not_verify_user(user: User) -> None:
    if not user.is_verify:
        raise exceptions.AuthenticationFailed(
            {'user_error': settings.ERRORS['user_error']['3']},
            code=status.HTTP_401_UNAUTHORIZED
        )


def is_not_active_user(user: User) -> None:
    if not user.is_active:
        raise exceptions.AuthenticationFailed(
            {'user_error': settings.ERRORS['user_error']['4']},
            code=status.HTTP_401_UNAUTHORIZED
        )


def check_password_user(user: User, password: str) -> None:
    if not user.check_password(password):
        raise exceptions.APIException(
            {'user_error': settings.ERRORS['user_error']['2']},
            code=status.HTTP_400_BAD_REQUEST
        )


def perform_confirm_verify_user(**kwargs):
    '''# Верификация почты пользователя по email и uuid #'''

    email = kwargs.pop('email')
    # token = kwargs.pop('token')
    user = find_or_get_user_model(**kwargs)

    if not user.email == email:
        user.email = email

    if not user.is_verify:
        user.is_verify = True
    if not user.is_active:
        user.is_active = True

    user.save()

    return ('user_info', '8', status.HTTP_200_OK)


def perform_additional_to_recovery_password(**kwargs) -> Tuple[str, str, int]:
    user = find_or_get_user_model(**kwargs)

    if not user.is_reset_password:
        user.is_reset_password = True
        user.save()

    email = user.email
    token = Jwt.create_tmp_access_token(email)

    EmailResetPassword(kwargs.get('email'), context={
        'protocol': 'https',
        'site_name': 'fire-activity-map.com',
        'url': f'url?email={email}&'
               f'token={token}&'
               f'uuid={user.uuid}',
    }).send()

    return ('user_info', '10', status.HTTP_200_OK)


def perform_reset_password(**kwargs) -> Tuple[str, str, int]:
    # print(kwargs)
    password = kwargs.pop('password')
    # token = kwargs.pop('token')
    # print(kwargs)
    user = find_or_get_user_model(**kwargs)

    if not user.is_reset_password:
        return ('user_info', '5', status.HTTP_200_OK)

    is_not_active_user(user)
    is_not_verify_user(user)

    user.set_password(password)
    user.is_reset_password = False
    user.save()

    return ('user_info', '7', status.HTTP_200_OK)


def perform_additional_to_recovery_account(**kwargs) -> Tuple[str, str, int]:
    user = find_or_get_user_model(**kwargs)
    is_not_verify_user(user)
    if user.is_active:
        return ('user_info', '12', status.HTTP_200_OK)

    email = user.email
    token = Jwt.create_tmp_access_token(email)

    RecoveryAccount(kwargs.get('email'), context={
        'protocol': 'https',
        'site_name': 'fire-activity-map.com',
        'url': f'url?email={email}&'
               f'token={token}&'
               f'uuid={user.uuid}',
    }).send()

    return ('user_info', '13', status.HTTP_200_OK)


def perform_recovery_account(**kwargs) -> Tuple[str, str, int]:
    user = find_or_get_user_model(**kwargs)

    user.is_active = True
    user.save()

    return ('user_info', '12', status.HTTP_200_OK)


def is_token_transferred(refresh_token) -> None:
    if refresh_token is None:
        raise exceptions.APIException(
            {'refresh_token': settings.ERRORS['15']},#{'error_token': 'Refresh field is required'},
            code=status.HTTP_400_BAD_REQUEST
        )


def get_couple_tokens(**kwargs) -> dict:
    password = kwargs.pop('password')

    user = find_or_get_user_model(**kwargs)


    is_not_verify_user(user)

    # if not user.is_active:
    #     EmailResetPassword(kwargs.get('email'), context={
    #         'protocol': 'https',
    #         'site_name': 'fire-activity-map.com',
    #         'url': f'url?email={email}&'
    #                f'token={token}&'
    #                f'uuid={user.uuid}',
    #     }).send()
    is_not_active_user(user)

    check_password_user(user, password)

    token = {
        'refresh': Jwt.create_refresh_token(user_id=user.id),
        'access': Jwt.create_access_token(user_id=user.id),
    }

    return token


def get_access_token(**kwargs) -> dict:
    user = find_or_get_user_model(**kwargs)

    is_not_verify_user(user)

    access_token = {
        'access': Jwt.create_access_token(user_id=kwargs.get('id'))
    }

    return access_token



