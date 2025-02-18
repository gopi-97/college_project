from django.db import models
from manage_account.models import Farmer

# Create your models here.

def user_directory(instance,filename):
    return f'inventory/{instance.user_id}/Productimages/{filename}'

class FarmerInventory(models.Model):
    user = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50,blank=True)
    quantity = models.CharField(max_length=20)
    image = models.ImageField(upload_to=user_directory)
    class Meta:
        db_table = 'inventory'

    def __str__(self):
        return f"{self.product} - {self.quantity}"
    
