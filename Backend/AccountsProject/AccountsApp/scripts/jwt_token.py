from datetime import datetime, timedelta
from django.conf import settings
import jwt
from uuid import uuid4

from rest_framework import exceptions, status

from .decorators import exception_jwt


class Jwt:

    @staticmethod
    def create_tmp_access_token(email):
        payload = {
            'token_type': 'access',
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'jti': f'{uuid4()}',
            'email': email,
        }

        access_token = jwt.encode(
            payload=payload,
            key=settings.ACCESS_SECRET_KEY+email,
            algorithm='HS256'
        )

        return access_token

    @staticmethod
    def get_payload_from_tmp_access_token(token, email):
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.ACCESS_SECRET_KEY + email,
                algorithms='HS256'
            )
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed(
                {'available_tmp_error': settings.ERRORS['available_tmp_error']['14']},
                code=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                {'available_tmp_error': settings.ERRORS['available_tmp_error']['14']},
                code=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed(
                {'available_tmp_error': settings.ERRORS['available_tmp_error']['14']},
                code=status.HTTP_401_UNAUTHORIZED
            )

        return payload

    @staticmethod
    def create_access_token(user_id):
        payload = {
            'token_type': 'access',
            'exp': datetime.utcnow() + timedelta(days=0, minutes=35),
            'iat': datetime.utcnow(),
            'jti': f'{uuid4()}',
            'user_id': user_id,
        }

        access_token = jwt.encode(
            payload=payload,
            key=settings.ACCESS_SECRET_KEY,
            algorithm='HS256'
        )

        return access_token

    @staticmethod
    def create_refresh_token(user_id):
        payload = {
            'token_type': 'refresh',
            'exp': datetime.utcnow() + timedelta(days=10),
            'iat': datetime.utcnow(),
            'jti': f'{uuid4()}',
            'user_id': user_id,
        }

        refresh_token = jwt.encode(
            payload=payload,
            key=settings.REFRESH_SECRET_KEY,
            algorithm='HS256'
        )

        return refresh_token

    @staticmethod
    @exception_jwt
    def get_payload_from_refresh_token(token):

        payload = jwt.decode(
            jwt=token,
            key=settings.REFRESH_SECRET_KEY,
            algorithms='HS256'
        )

        return payload

    @staticmethod
    @exception_jwt
    def get_payload_from_access_token(token):

        payload = jwt.decode(
            jwt=token,
            key=settings.ACCESS_SECRET_KEY,
            algorithms='HS256'
        )

        return payload

