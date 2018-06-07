from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import SamlUser

UserModel = get_user_model()

class SamlBackend:

    def authenticate(self, request, username, email, givenname, surname):
        try:
            user = UserModel.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username, email=email, first_name=givenname, last_name=surname)
            user.save()
            samluser = SamlUser(user=user, is_persistent=False)
            samluser.save()
        return user

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
