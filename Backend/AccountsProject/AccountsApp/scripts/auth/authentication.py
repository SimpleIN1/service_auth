from django.contrib.auth import get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response

from AccountsApp.scripts.token.jwt_token import Jwt
from AccountsApp.scripts.user_view import find_or_get_user_model, is_not_active_user


class CSRF(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class JWTAuthentication(BaseAuthentication):
    User = get_user_model()

    def authenticate(self, request):
        token = request.headers.get('Authorization', None)

        if not token:
            return None

        try:
            token = token.split(' ')[1]
        except IndexError:
            return None

        payload = Jwt.get_payload_from_access_token(token)

        user_id = payload.get('user_id')

        # try:
        #     user = self.User.objects.get(id=user_id)
        # except self.User.DoesNotExist:
        #     raise exceptions.AuthenticationFailed(
        #         detail='User not found',
        #         code=status.HTTP_401_UNAUTHORIZED
        #     )

        user = find_or_get_user_model(id=user_id)

        # if not user.is_active:
        #     raise exceptions.AuthenticationFailed(
        #         detail='User is inactive',
        #         code=status.HTTP_401_UNAUTHORIZED
        #     )

        is_not_active_user(user)

        # if not user.is_active:
        #     return None

        # print(type(user))
        # print(user)

        csrf = CSRF(Response())
        csrf.process_request(request)
        # print('---')
        # print(request.META['CSRF_COOKIE'])
        # # print(request.META['REMOTE_USER'])
        # print(csrf.process_view(request, None, (), {}))
        # print('---')

        return (user, None)


# from django.contrib.auth.backends import RemoteUserBackend
#
# User = get_user_model()
#
#
# class CustomModelBackend(RemoteUserBackend):
#     def authenticate(self, request, remote_user):
#         print('+++')
#         print(request)
#         print(remote_user)
#         print('+++')
#
#         return User.objects.get(id=1)
