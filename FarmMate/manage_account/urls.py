from django.urls import path
from .views import *
urlpatterns=[
    path('',loginForm,name='userlogin'),
    path('registration/',registrationForm,name='signup'),
    path('home/',home,name='home'),
    path('logout/', logoutUser, name='logout')
]