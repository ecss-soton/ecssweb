from django.test import TestCase

from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group

from ecsswebauth.models import EcsswebUserGroup, SamlUser

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


class UserTestCase(TestCase):

    def test_ecsswebusergroup_str(self):
        group = Group.objects.create(name='test_group')
        ecsswebusergroup = EcsswebUserGroup(group=group, is_saml=False)
        self.assertEqual(str(ecsswebusergroup), 'test_group')

    def test_ecsswebusergroup_natural_key(self):
        group = Group.objects.create(name='test_group')
        ecsswebusergroup = EcsswebUserGroup(group=group, is_saml=False)
        self.assertEqual(ecsswebusergroup.natural_key(), ('test_group',))

    def test_ecsswebusergroup_get_by_natural_key(self):
        group = Group.objects.create(name='test_group')
        ecsswebusergroup = EcsswebUserGroup.objects.create(group=group, is_saml=False)
        self.assertEqual(EcsswebUserGroup.objects.get_by_natural_key('test_group'), ecsswebusergroup)

    def test_samluser_str(self):
        user = User.objects.create(username='test01', email='test01@example.com', last_name='givenname01', first_name='surname01')
        samluser = SamlUser.objects.create(user=user, is_persistent=True)
        self.assertEqual(str(samluser), 'test01')

    def test_samluser_natural_key(self):
        user = User.objects.create(username='test01', email='test01@example.com', last_name='givenname01', first_name='surname01')
        samluser = SamlUser.objects.create(user=user, is_persistent=True)
        self.assertEqual(samluser.natural_key(), ('test01',))

    def test_samluser_get_by_natural_key(self):
        user = User.objects.create(username='test01', email='test01@example.com', last_name='givenname01', first_name='surname01')
        samluser = SamlUser.objects.create(user=user, is_persistent=True)
        self.assertEqual(SamlUser.objects.get_by_natural_key('test01'), samluser)
