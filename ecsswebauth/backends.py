from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.backends import ModelBackend

from django.conf import settings

from .models import SamlUser, EcsswebUserGroup

UserModel = get_user_model()

class SamlBackend(ModelBackend):

    def _create_saml_user(self, username):
        user = User(username=username)
        user.save()
        samluser = SamlUser(user=user, is_persistent=False)
        samluser.save()
        return user

    def _update_saml_info(self, user, groups, email, givenname, surname):
        user.email = email
        user.first_name = givenname
        user.last_name = surname
        user.save()

        # Update saml groups for the user, remove user from all saml groups and then add the user to saml groups
        current_groups = user.groups.all()

        for current_group in current_groups:
            try:
                if current_group.ecsswebusergroup.is_saml:
                    user.groups.remove(current_group)
            except EcsswebUserGroup.DoesNotExist:
                pass

        for group_name in groups:
            group_name = settings.SAML_GROUP_PREFIX + group_name
            group, created = Group.objects.get_or_create(name=group_name)
            group.save()
            if created:
                ecssweb_user_group = EcsswebUserGroup(group=group, is_saml=True)
                ecssweb_user_group.save()
            user.groups.add(group)

    def authenticate(self, request, username, groups, email, givenname, surname):
        # Try to get user from database, create user if does not exists
        try:
            user = UserModel.objects.get(username=username)
        except User.DoesNotExist:
            user = self._create_saml_user(username=username)
        # Update the users information from saml
        self._update_saml_info(user=user, groups=groups, email=email, givenname=givenname, surname=surname)
        return user

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
