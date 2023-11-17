from django.contrib.auth.backends import BaseBackend
from .models import Client  # Import your Client model

class ClientBackend(BaseBackend):
    def authenticate(self, request, userid=None, password=None, **kwargs):
        try:
            user = Client.objects.get(userid=userid)
            print(user.check_password(password))
            if user.check_password(password):
            
                return user
        except Client.DoesNotExist:
            return None
