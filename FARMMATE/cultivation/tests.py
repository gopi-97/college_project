from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cultivation, CurrentCultivation, Farms
from manage_account.models import Farmer
from inventory.models import FarmerInventory
class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = Farmer.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.add_product_url = reverse('add-product')
        self.add_to_inventory_url = reverse('add-to-inventory', kwargs={'pk': 1})  # Assuming pk is valid
        self.current_cultivation_detail_url = reverse('current-cultivation-details', kwargs={'pk': 1})  # Assuming pk is valid
    
    def test_add_product_view_GET(self):
        response = self.client.get(self.add_product_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cultivation/add_product.html')
    
    # Add more test cases for form submission and validation
    
    def test_add_to_inventory_view_POST(self):
        current_cultivation = CurrentCultivation.objects.create(
            user=self.user,
            product='Test Product',
            product_id='123456',
            location='Test Location',
            cultivated_area='Test Area',
            start_date='2023-01-01',
            description='Test Description'
        )
        response = self.client.post(self.add_to_inventory_url, {
            'quantity': 10,
            'images': 'test_image.jpg',  # Assuming you have a test image
            'harvested_date': '2023-02-01'
        })
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cultivation/current_cultivation_update.html')
        self.assertEquals(FarmerInventory.objects.count(), 1)  # Check if the inventory is updated
    
    def test_current_cultivation_detail_view_GET(self):
        current_cultivation = CurrentCultivation.objects.create(
            user=self.user,
            product='Test Product',
            product_id='123456',
            location='Test Location',
            cultivated_area='Test Area',
            start_date='2023-01-01',
            description='Test Description'
        )
        response = self.client.get(self.current_cultivation_detail_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cultivation/cultivation_detail.html')
