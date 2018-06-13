from django.test import TestCase

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class AuthTestCase(TestCase):

    def test_authenticate(self):
        # Test create one user
        user01 = authenticate(request=None, username='test01', groups=[], email='test01@example.com', givenname='givenname01', surname='surname01')
        user01_retrieved = User.objects.get(username='test01')
        self.assertEqual(user01_retrieved, user01)

        # Test get user info
        self.assertEqual(user01.email, 'test01@example.com')

        # Test create another user
        user02 = authenticate(request=None, username='test02', groups=[], email='test02@example.com', givenname='givenname02', surname='surname02')
        user02_retrieved = User.objects.get(username='test02')
        self.assertEqual(user02_retrieved, user02)

        # Test retrieve the first user again
        user01_retrieved = User.objects.get(username='test01')
        self.assertEqual(user01_retrieved, user01)

        # Test authenticate user already exists
        user01_authenticate = authenticate(request=None, username='test01', groups=[], email='test01@example.com', givenname='givenname01', surname='surname01')
        self.assertEqual(user01_authenticate, user01)
        self.assertEqual(len(User.objects.all()), 2)

        # Test update userinfo while authenticate the user
        user01 = authenticate(request=None, username='test01', groups=[], email='test01_new_email@example.com', givenname='givenname01', surname='surname01')
        self.assertEqual(user01.email, 'test01_new_email@example.com')
