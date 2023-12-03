from django.db import models
from manage_account.models import Client
from django.utils import timezone
import random

class Farms(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    location = models.CharField(max_length=300)
    status = models.CharField(max_length=100)

class Cultivation(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50, unique=True)  # Make the product_id unique
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=300)
    cultivated_area = models.CharField(max_length=30)
    start_date = models.DateTimeField(default=timezone.now)  # Set default value to the current time
    harvested_date = models.DateTimeField(null=True, blank=True)  # Allow null and blank for harvested_date
    description = models.TextField()

    def generate_product_id(self):
        day = str(self.start_date.day)
        random_num = str(random.randint(0, 100))
        product_id = f"{self.product}{day}{random_num}"
        return product_id
    
    def save(self, *args, **kwargs):
        if not self.product_id:  # Generate product_id if not provided
            self.product_id = self.generate_product_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.product} ({self.product_id})"

class Inventory(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    images = models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.product} - {self.quantity}"
