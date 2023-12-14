from django.contrib.auth.backends import BaseBackend
from skelbiameAPI.models import User
from django.core.exceptions import ObjectDoesNotExist
from hashlib import sha256

class UserBackend(BaseBackend):
    def authenticate(self, request, username = None, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        else:
            if user.password == sha256(password.encode("utf-8")).hexdigest():
                return user
        return None

    def get_user(self, user_pk):
        try:
            return User.objects.get(pk=user_pk)
        except:
            return None