import functools

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework import status, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import AllowAny, IsAuthenticated

from .scripts.decorators import permission_is_auth_tmp_token
from .scripts.user_view import UserUpdateDestroyRetrieve, perform_confirm_verify_user, \
    perform_additional_to_reset_password, perform_reset_password, get_couple_tokens, get_access_token, \
    is_token_transferred, perform_additional_to_recovery_user, perform_recovery_user, find_or_get_user_model, \
    perform_resend_email_letter, perform_change_password
from .serializers import UserSerializer, EmailSerializer, JwtLoginSerializer, ResetPasswordSerializer, \
    ConfirmVerifyEMailSerializer, RecoveyAccount, ResendLetterSerializer, ChangePasswordSerializer
from AccountsApp.scripts.token.jwt_token import Jwt

User = get_user_model()


class UserCreateViewSet(
    CreateModelMixin,
    GenericViewSet
):
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs): # override
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'user_info': '9',#settings.ERRORS['user_info']['9']
             'user_data': serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(methods=['POST'], detail=False)
    def reset_password(self, request, *args, **kwargs):
        '''# Представление восстановления пароля. На вход принимает email, затем происходит отправка письма #'''

        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = perform_additional_to_reset_password(
            **serializer.validated_data
        )

        return Response(
            {response[0]: response[1]}, #settings.ERRORS[response[0]][response[1]]
            status=response[2]
        )#'Email is sent'

    @action(methods=['POST'], detail=False)
    @permission_is_auth_tmp_token()
    def confirm_reset_password(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = perform_reset_password(
            **serializer.validated_data
        )

        return Response(
            {response[0]: response[1]},#settings.ERRORS[response[0]][response[1]]
            status=response[2]
        )

    @action(methods=['POST'], detail=False)
    @permission_is_auth_tmp_token(is_password=True)
    def confirm_verify_email(self, request, *args, **kwargs): # Done
        '''# Представление для подтверждения почты пользователя #'''

        serializer = ConfirmVerifyEMailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = perform_confirm_verify_user(
            **serializer.validated_data
        )

        return Response(
            {response[0]: response[1]}, #settings.ERRORS[response[0]][response[1]]
            status=response[2]
        )#'you are verifying'

    @action(methods=['POST'], detail=False)
    def recovery_user(self, request, *args, **kwargs):
        '''# Представление для восстановления пользователя #'''

        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = perform_additional_to_recovery_user(
            **serializer.validated_data
        )

        return Response(
            {response[0]: response[1]}, #settings.ERRORS[response[0]][response[1]]
            status=response[2]
        )

    @action(methods=['POST'], detail=False)
    @permission_is_auth_tmp_token()
    def confirm_recovery_user(self, request, *args, **kwargs):
        '''# Представление для поддтверждения восстановления пользователя #'''

        serializer = RecoveyAccount(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = perform_recovery_user(
            **serializer.validated_data
        )
        return Response(
            {response[0]: response[1]}, #settings.ERRORS[response[0]][response[1]]
            status=response[2]
        )

    @action(methods=['POST'], detail=False)
    def resend_email_letter(self, request, *args, **kwargs):
        '''# Представление для переотправки письма пользователю при регистрации #'''

        serializer = ResendLetterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = perform_resend_email_letter(
            **serializer.validated_data
        )
        return Response(
            {response[0]: response[1]}, #settings.ERRORS[response[0]][response[1]]
            status=response[2]
        )


class UserDetailDestroyUpdateViewSet(
    RetrieveModelMixin,
    GenericViewSet,
    UserUpdateDestroyRetrieve
):

    #permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            # raise OverrideNotAuthenticated()
            raise exceptions.AuthenticationFailed(
                {'auth_error': '20'}
            )
        raise exceptions.PermissionDenied(detail=message, code=code)

    @action(methods=['GET', 'PUT', 'DELETE', 'PATCH'], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get_user(request, *args, **kwargs)
        if request.method == 'PUT':
            return self.put_user(request, *args, **kwargs)
        if request.method == 'DELETE':
            return self.destroy_user(request, *args, **kwargs)
        if request.method == 'PATCH':
            return self.patch_user(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def logout(self, request, *args, **kwargs):
        '''# Представление для выходы пользователя из системы. Удаление refresh_token из cookie #'''

        response = Response()
        response.delete_cookie('refresh_token')
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    @action(methods=['POST'], detail=False)
    def change_password(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = perform_change_password(
            request.user,
            **serializer.validated_data
        )

        return Response(
            {response[0]: response[1]}, #settings.ERRORS[response[0]][response[1]]
            status=response[2]
        )


class JwtCreateTokenAPIView(APIView):
    permission_classes = (AllowAny, )

    @method_decorator(ensure_csrf_cookie) #ensure_csrf_cookie для отправления страницы
    def post(self, request, *args, **kwargs):
        '''# Получение пары токенов (JWT) #'''

        serializer = JwtLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = get_couple_tokens(
            **serializer.validated_data
        )

        response = Response()
        response.data = token
        response.status_code = status.HTTP_200_OK
        response.set_cookie(
            key='refresh_token',
            value=token['refresh'],
            httponly=True,
            secure=True,
            samesite='strict'
        )

        return response


class JwtRefreshTokenAPIView(APIView):
    permission_classes = (AllowAny, )

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        '''#  Обновление access_token #'''

        # refresh_token = request.data.get('refresh', None)
        refresh_token = request.COOKIES.get('refresh_token', None)

        is_token_transferred(refresh_token)

        payload = Jwt.get_payload_from_refresh_token(refresh_token)

        user_id = payload.get('user_id')

        access_token = get_access_token(id=user_id)

        return Response(
            access_token,
            status=status.HTTP_200_OK
        )
