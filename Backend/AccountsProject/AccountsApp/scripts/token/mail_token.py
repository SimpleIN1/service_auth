
from django.contrib.auth.tokens import PasswordResetTokenGenerator #as TokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):

    def __init__(self, is_pass=False):
        super().__init__()
        self.is_pass = is_pass

    def _make_hash_value(self, user, timestamp): #Override. Changed user.password to user.uuid

        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, "") or ""
        if self.is_pass:
            return f"{user.pk}{user.uuid}{user.password}{login_timestamp}{timestamp}{email}"
        else:
            return f"{user.pk}{user.uuid}{login_timestamp}{timestamp}{email}"


def create_token(
        user,
        is_password=False
):
    '''# Гененрация токена для отправки по почте #'''

    return TokenGenerator(is_password).make_token(user)


def check_token(
        user,
        getting_token: str,
        is_password=False,
) -> bool:
    '''# Проверка токена #'''

    return TokenGenerator(is_password).check_token(user, getting_token)
