import functools

import jwt
from django.conf import settings
from django.core.validators import validate_email
from django.http import Http404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from rest_framework import status, exceptions, mixins
from rest_framework.decorators import action, permission_classes as permission_classes_decor
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin)
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime

from .scripts.mail_send import EmailVerify, EmailResetPassword
from .scripts.user_view import UserUpdateDestroyRetrieve, find_or_get_user_model, perform_confirm_verify_user, \
    perform_additional_to_recovery_password, perform_reset_password, get_couple_tokens, get_access_token, \
    is_token_transferred, perform_additional_to_recovery_account, perform_recovery_account
from .scripts.verify import Verify
from .serializers import UserSerializer, EmailSerializer, JwtLoginSerializer, ResetPasswordSerializer, \
    ConfirmVerifyEMailSerializer
from .scripts.jwt_token import Jwt
from .permissions import IsVerifyEmailAndActive
from .tasks import send_email

User = get_user_model()


def permission_is_auth_tmp_token(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        email = args[1].data.get('email', None)
        uuid = args[1].data.get('uuid', None)
        token = args[1].data.get('token', None)

        if uuid is None or email is None or token is None:
            raise exceptions.AuthenticationFailed(
                {'available_tmp_error': settings.ERRORS['available_tmp_error']['14']},
                code=status.HTTP_401_UNAUTHORIZED
            )
        payload = Jwt.get_payload_from_tmp_access_token(token, email)
        result = func(*args, **kwargs)
        return result

    return inner_func


class UserCreateViewSet(
    CreateModelMixin,
    GenericViewSet
):
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'user_info': settings.ERRORS['user_info']['9'],
             'user_data': serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(methods=['POST'], detail=False)
    def recovery_password(self, request, *args, **kwargs):
        '''# Представление восстановления пароля. На вход принимает email, затем происходит отправка письма #'''

        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')

        response = perform_additional_to_recovery_password(email=email)

        return Response({response[0]: settings.ERRORS[response[0]][response[1]]}, status=response[2])#'Email is sent'

    @action(methods=['POST'], detail=False)
    @permission_is_auth_tmp_token
    def confirm_verify_email(self, request, *args, **kwargs): # Done
        '''# Представление подтверждения почты пользователя #'''

        serializer = ConfirmVerifyEMailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uuid = request.data.get('uuid')
        email = request.data.get('email')
        response = perform_confirm_verify_user(uuid=uuid, email=email)

        return Response(
            {response[0]: settings.ERRORS[response[0]][response[1]]},
            status=response[2]
        )#'you are verifying'

    @action(methods=['POST'], detail=False)
    @permission_is_auth_tmp_token
    def reset_password(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = perform_reset_password(
            uuid=serializer.validated_data.get('uuid'),
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password')
        )

        return Response(
            {response[0]: settings.ERRORS[response[0]][response[1]]},
            status=response[2]
        )

    @action(methods=['POST'], detail=False)
    def recovery_user(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')

        response = perform_additional_to_recovery_account(email=email)

        return Response(
            {response[0]: settings.ERRORS[response[0]][response[1]]},
            status=response[2]
        )

    @action(methods=['POST'], detail=False)
    @permission_is_auth_tmp_token
    def confirm_recovery_user(self, request, *args, **kwargs):

        response = perform_recovery_account(
            email=request.data.get('email'),
            uuid=request.data.get('uuid'),
        )
        return Response(
            {response[0]: settings.ERRORS[response[0]][response[1]]},
            status=response[2]
        )


class UserDetailDestroyUpdateViewSet(
    RetrieveModelMixin,
    GenericViewSet,
    UserUpdateDestroyRetrieve
):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
        response = Response()
        response.delete_cookie('refresh_token')
        response.status_code = status.HTTP_204_NO_CONTENT
        return response


class JwtCreateTokenAPIView(APIView):
    permission_classes = (AllowAny, )

    @method_decorator(ensure_csrf_cookie) #ensure_csrf_cookie для отправления страницы
    def post(self, request, *args, **kwargs):
        serializer = JwtLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')
        password = serializer.data.get('password')
        # print(password)

        token = get_couple_tokens(email=email, password=password)

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
