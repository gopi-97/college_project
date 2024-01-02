from django.urls import path
from .views import *

urlpatterns=[
    # path('home/',loadHome,name='home'),
    path("dashboard/",load_dash,name='dashboard'),
    path("add-product/",add_product,name='add-product'),
    path("add-field/",add_field,name='add-field'),
    path('graph/', graph_view,name='graph'),

]