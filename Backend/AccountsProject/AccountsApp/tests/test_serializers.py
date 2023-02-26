from django.contrib.auth import get_user_model
from django.test import TestCase

from ..serializers import UserSerializer

User = get_user_model()


class UserSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(
            email='user1@user.com',
            first_name='user1_first_name',
            last_name='user1_last_name',
            middle_name='user1_middle_name',
            organization_name='user1_organization_name',
        )
        user1.set_password('1234')
        user1.save()

        data = UserSerializer(user1).data

        excepted_data = {
            'email': 'user1@user.com',
            'first_name': 'user1_first_name',
            'last_name': 'user1_last_name',
            'middle_name': 'user1_middle_name',
            'organization_name': 'user1_organization_name'
        }

        self.assertEqual(excepted_data, data)
