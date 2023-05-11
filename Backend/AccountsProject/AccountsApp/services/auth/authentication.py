from django.contrib.auth import get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response

from AccountsApp.services.token.jwt_token import Jwt
from AccountsApp.services.user_view import find_or_get_user_model, is_not_active_user


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
        user = find_or_get_user_model(id=user_id)

        is_not_active_user(user)

        csrf = CSRF(Response())
        csrf.process_request(request)


        return (user, None)
