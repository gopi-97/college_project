from datetime import timedelta
from django.utils import timezone
import random
import os
import sys
import django

# Add the path to your Django project
sys.path.append('C:/Users/aspire/Documents/college_project/FARMMATE')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmMate.settings')
django.setup()

# Now you should be able to import the necessary modules
from manage_account.models import Client
# Import your models
from dashboard.models import Farms, Cultivation, Inventory


# Assuming you have already created user1 and user2 instances with the provided user IDs
user1 = Client.objects.get(userid='d1ec6zOXOx')
user2 = Client.objects.get(userid='wYTDDpdCPv')

# Create Farms
farm1 = Farms.objects.create(user=user1, location='Kochi', status='Active')
farm2 = Farms.objects.create(user=user2, location='Trivandrum', status='Inactive')
farm3 = Farms.objects.create(user=user1, location='Kottayam', status='Active')

# Create Cultivations
rice_types = ['Basmati', 'Jasmine', 'Arborio']
for i in range(5):
    Cultivation.objects.create(
        user=user1,
        product=random.choice(rice_types),
        status='In progress',
        location='Kerala',
        cultivated_area='10 acres',
        start_date=timezone.now() - timedelta(days=60 * i),
        harvested_date=timezone.now() - timedelta(days=60 * i) + timedelta(days=120)
    )

for i in range(5):
    Cultivation.objects.create(
        user=user2,
        product=random.choice(rice_types),
        status='In progress',
        location='Kerala',
        cultivated_area='8 acres',
        start_date=timezone.now() - timedelta(days=60 * i),
        harvested_date=timezone.now() - timedelta(days=60 * i) + timedelta(days=130)
    )

# Create Inventory
for i in range(2):
    Inventory.objects.create(user=user1, product=f"Rice Type {i+1}", quantity=50)

for i in range(2):
    Inventory.objects.create(user=user2, product=f"Rice Type {i+1}", quantity=40)
