from django.db import models
from manage_account.models import Farmer
from django.utils import timezone
import random

class Farms(models.Model):
    user = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    location = models.CharField(max_length=300)
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'farms'

class Cultivation(models.Model):
    user = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50, unique=True)  # Make the product_id unique
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=300)
    cultivated_area = models.CharField(max_length=30)
    start_date = models.DateTimeField(default=timezone.now)  # Set default value to the current time
    harvested_date = models.DateTimeField(null=True, blank=True)  # Allow null and blank for harvested_date
    description = models.TextField()

    class Meta:
        db_table = 'cultivation'


    def __str__(self):
        return f"{self.user} - {self.product} ({self.product_id})"

class CurrentCultivation(models.Model):
    user = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50, unique=True)  # Make the product_id unique
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=300)
    cultivated_area = models.CharField(max_length=30)
    start_date = models.DateTimeField(default=timezone.now)  # Set default value to the current time
    harvested_date = models.DateTimeField(null=True, blank=True)  # Allow null and blank for harvested_date
    description = models.TextField()

    class Meta:
        db_table = 'current_cultivation'


    def __str__(self):
        return f"{self.user} - {self.product} ({self.product_id})"
