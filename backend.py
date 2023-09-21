from django.conf import settings
from .models import CustomUser as User

class AuthBackend:
    def authenticate(self, username=None, password=None):
        kwargs = {'email': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None