from datetime import datetime, timedelta
from django.conf import settings
import jwt
from uuid import uuid4

from AccountsApp.decorators import exception_jwt


class Jwt:

    @staticmethod
    def create_access_token(user_id):
        payload = {
            'token_type': 'access',
            'exp': datetime.utcnow() + timedelta(days=0, minutes=10),
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
            'exp': datetime.utcnow() + timedelta(days=2),
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

