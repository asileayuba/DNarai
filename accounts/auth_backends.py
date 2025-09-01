from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import CustomUser

class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(CustomUser.USERNAME_FIELD)

        if username is None or password is None:
            return None

        # Normalize input
        username = username.strip().lower()

        try:
            user = CustomUser.objects.get(
                Q(username=username) | Q(email__iexact=username)
            )
        except CustomUser.DoesNotExist:
            return None
        except CustomUser.MultipleObjectsReturned:
            # Prefer username match over email match
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return None

        if user.check_password(password) and user.is_active:
            return user
        return None
