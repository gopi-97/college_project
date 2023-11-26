from django.urls import path
from .views import *
urlpatterns=[

    path('',loadHome,name='home')
]