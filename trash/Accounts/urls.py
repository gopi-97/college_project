from django.urls import path
from .views import *
urlpatterns=[
    path("login/",loginForm,name='login'),
    path("registration/",registrationForm,name='register')
]