from django.urls import path
from .views import add_user
urlpatterns=[
    path("signup/",add_user,name='add_user'),
]