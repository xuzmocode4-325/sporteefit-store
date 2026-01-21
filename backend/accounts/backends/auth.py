from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = (
            User.objects.filter(username__iexact=username).first()
            or User.objects.filter(email__iexact=username).first()
        )
        if user and user.check_password(password):
            return user
        return None
