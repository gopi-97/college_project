from django.urls import path
from .views import *
urlpatterns=[
    path("dashboard/",load_dash,name='dashboard')
]