from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
class EmailBackend(ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email = username)
            if user.check_password(password):
                return user
            else:
                return None
        except ObjectDoesNotExist:
            return None

    def get_user(self,user_id):
        User = get_user_model()
        try:
            user = User.objects.get(id = user_id)
            return user
        except ObjectDoesNotExist:
            return None