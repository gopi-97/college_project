from django.urls import path
from .views import *
urlpatterns=[
    path('login/',loginForm,name='userlogin'),
    path('registration/',registrationForm,name='signup'),
    path('',home,name='home'),
    path('logout/', logoutUser, name='logout')
]