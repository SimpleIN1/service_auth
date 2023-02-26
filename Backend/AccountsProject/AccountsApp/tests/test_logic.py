from django.test import TestCase
from django.conf import settings


class LogicTestCase(TestCase):
    pass
    # def test_creating_token(self):
    #     uuid = 'fddfsd-fsdfw342rf-234234-rfsdf'
    #     email = 'test_user@mail.ru'
    #     id = '12'
    #     secret_key = settings.SECRET_KEY
    #     expected_token = 'be74eeb8e8affd52fff99e620463a8dc'
    #     token = create_token(id, email, uuid, secret_key)
    #
    #     self.assertEqual(expected_token, token)
    #
    # def test_check_token(self):
    #     uuid = 'fddfsd-fsdfw342rf-234234-rfsdf'
    #     email = 'test_user@mail.ru'
    #     id = '12'
    #     secret_key = settings.SECRET_KEY
    #     expected_token = 'be74eeb8e8affd52fff99e620463a8dc'
    #
    #     token = create_token(id, email, uuid, secret_key)
    #     result = check_token(expected_token, id, email, uuid, secret_key)
    #
    #     self.assertEqual(True, result)