from django.test import TestCase
from django.shortcuts import resolve_url

from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.conf import settings

from ecsswebauth.models import EcsswebUserGroup, SamlUser
from ecsswebauth.views import _clean_next_url, _get_user_info_from_attributes

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


class CleanNextUrlTestCase(TestCase):

    def test__clean_next_url(self):
        default_url = resolve_url(settings.LOGIN_REDIRECT_URL)
        url1 = '/auth/'
        self.assertEqual(_clean_next_url(url1), url1)
        url2 = 'https://example.com'
        self.assertEqual(_clean_next_url(url2), default_url)
        url3 = 'https://{}/auth/'.format(settings.ALLOWED_HOSTS[0])
        self.assertEqual(_clean_next_url(url3), url3)
        url4 = 'http://{}/auth/'.format(settings.ALLOWED_HOSTS[0])
        self.assertEqual(_clean_next_url(url4), url4)
        url5 = 'ftp://{}/auth/'.format(settings.ALLOWED_HOSTS[0])
        self.assertEqual(_clean_next_url(url5), default_url)
        url6 = 'javascript:alert("alert!");'.format(settings.ALLOWED_HOSTS[0])
        self.assertEqual(_clean_next_url(url6), default_url)


class AttributesTestCase(TestCase):

    def test__get_user_info_from_attributes(self):
        attributes = {
            'http://schemas.microsoft.com/ws/2008/06/identity/claims/windowsaccountname': ['username1'],
            'http://schemas.xmlsoap.org/claims/Group': [
                'group1',
                'group2',
            ],
            'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress': ['example@example.com'],
            'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname': ['givenname1'],
            'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname': ['surname1'],
        }
        userinfo = {
            'username': 'username1',
            'groups': [
                'group1',
                'group2',
            ],
            'email': 'example@example.com',
            'givenname': 'givenname1',
            'surname': 'surname1',
        }
        self.assertEqual(_get_user_info_from_attributes(attributes), userinfo)
