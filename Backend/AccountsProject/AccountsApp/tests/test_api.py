# TestCase

from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase,APIClient

from AccountsApp.models import User
from AccountsApp.serializers import UserSerializer


class UserAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(
            email='user1@user.com',
            first_name='user1_first_name',
            last_name='user1_last_name',
            middle_name='user1_middle_name',
            organization_name='user1_organization_name',
        )
        self.user1.set_password('1234_Ddqw-')
        self.user1.save()

        self.user2 = User.objects.create(
            email='user2@user.com',
            first_name='user2_first_name',
            last_name='user2_last_name',
            middle_name='user2_middle_name',
            organization_name='user1_organization_name',
        )
        self.user2.set_password('1234_Ddqw-')
        self.user2.is_verify = True
        self.user2.is_active = True
        self.user2.save()

    def test_create_user(self):
        '''# Test create a user #'''

        url = reverse('user-list')

        data = {
            'email': 'user@user.com',
            'password': '1234-_Rd',
            're_password': '1234-_Rd',
            'last_name': 'user1_last_name',
            'first_name': 'user1_first_name',
            'middle_name': 'user1_middle_name',
            'organization_name': 'user1_organization_name'
        }
        request = self.client.post(url, data)
        self.assertEqual(status.HTTP_201_CREATED, request.status_code)

        # serializer_data = UserSerializer(data).data
        expected_data = {
            'user_data': {
                'email': 'user@user.com',
                'first_name': 'user1_first_name',
                'last_name': 'user1_last_name',
                'middle_name': 'user1_middle_name',
                'organization_name': 'user1_organization_name'
            },
            'user_info': '9'
        }
        self.assertEqual(expected_data, request.data)

    def test_create_user_validation_email(self):
        '''# Test the error of validation into email #'''

        url = reverse('user-list')
        data = {
            'email': 'user1@user.com',
            'password': '1234-_Rd1',
            're_password': '1234-_Rd1',
            'last_name': 'user1_last_name',
            'first_name': 'user1_first_name',
            'middle_name': 'user1_middle_name',
            'organization_name': 'user1_organization_name'
        }
        request = self.client.post(url, data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

        expected_data = {
            'fields_error': '19'
        }
        self.assertEqual(expected_data, request.data)

    def test_create_user_validation_email_and_password(self):
        '''# test the error of validation into email and password #'''

        url = reverse('user-list')
        data = {
            'email': 'user1@user.com',
            'password': '1234',
            'last_name': 'user1_last_name',
            'first_name': 'user1_first_name',
            'middle_name': 'user1_middle_name',
            'organization_name': 'user1_organization_name'
        }
        request = self.client.post(url, data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

        expected_data = {
            'fields_error': '19'
        }
        self.assertEqual(expected_data, request.data)

    def test_get_token(self):
        '''Test getting token, login '''

        url = reverse('jwt-create')

        data = {
            'email': 'user2@user.com',
            'password': '1234_Ddqw-',
        }
        response = self.client.post(url, data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        return response.data

    def test_refresh_token(self):
        url_create_jwt = reverse('jwt-create')
        data = {
            'email': f'{self.user2.email}',
            'password': '1234_Ddqw-'
        }
        response_create_jwt = self.client.post(url_create_jwt, data)
        self.assertEqual(status.HTTP_200_OK, response_create_jwt.status_code)

        url_refresh_token = reverse('jwt-refresh')
        response_refresh_token = self.client.get(url_refresh_token)
        # print(response_refresh_token.data)
        self.assertEqual(status.HTTP_200_OK, response_refresh_token.status_code)

    def test_get_user_detail(self):
        '''# Test getting data of user 2 using an access token #'''

        url = reverse('user-me')

        token = self.test_get_token()['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        received_data = UserSerializer(response.data).data
        expected_data = UserSerializer(self.user2).data

        self.assertEqual(expected_data, received_data)

    def test_put_user(self):
        '''# Test the put request on the user model #'''

        url = reverse('user-me')

        token = self.test_get_token()['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'email': 'user2@user.com',
            'password': '1323_dasdw',
            'last_name': 'user1_last_name',
            'first_name': 'user1_first_name',
            'middle_name': 'user1_middle_name',
            'organization_name': 'user1_organization_name'
        }
        response = client.put(url, data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected_data = UserSerializer(data).data
        received_data = UserSerializer(response.data['user_data']).data

        self.assertEqual(expected_data, received_data)

    def test_put_user_without_some_fields_valid(self):
        '''# Test the put request and test valid fields #'''

        url = reverse('user-me')

        token = self.test_get_token()['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'email': 'user2@user.com',
            'last_name': 'user',
            'first_name': 'user1',
            'middle_name': 'user_name'
        }
        response = client.put(url, data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        expected_data = {
            'fields_error': '18'
        }

        self.assertEqual(expected_data, response.data)

    def test_put_user_valid_email_unique(self):
        '''# Check unique email when the put request #'''

        url = reverse('user-me')

        token = self.test_get_token()['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'email': 'user1@user.com',
            'password': '1234',
            'last_name': 'user',
            'first_name': 'user1',
            'middle_name': 'user_name',
            'organization_name': 'oganization_name'
        }
        response = client.put(url, data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        expected_data = {
            'fields_error': '19'
        }

        self.assertEqual(expected_data, response.data)

    def test_destroy_user(self):
        '''# Test destroy user #'''

        url = reverse('user-me')

        token = self.test_get_token()['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # print(self.user2.is_active)
