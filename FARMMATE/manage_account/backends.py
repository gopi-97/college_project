from django.contrib.auth.backends import BaseBackend
from .models import Client

class ClientBackend(BaseBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = Client.objects.get(userid=username)
            if user.check_password(password):
                return user
            else:
                None     
        
        except Client.DoesNotExist:
            return None

