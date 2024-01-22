from django.db import models
from core import settings
# from manage_account.models import Farmer

# Create your models here.
class Tasks(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=100,null=True)
    description=models.TextField(null=True)
    complete=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering=['complete']