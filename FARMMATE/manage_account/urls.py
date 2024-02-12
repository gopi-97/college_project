from django.urls import path
from .views import *

urlpatterns=[
    path('',userLogin,name='userlogin'),
    path('registration/',register.as_view(),name='signup'),
    path('home/',home.as_view(),name='home'),
    path('logout/', UserLogout.as_view(), name='logout'),
    
]