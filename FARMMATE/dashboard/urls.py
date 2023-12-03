from django.urls import path
from .views import *

urlpatterns=[
    path('',loadHome,name='home'),
    path("dashboard/",load_dash,name='dashboard'),
    path("add-product/",add_product,name='add-product'),
]