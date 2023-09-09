from django.urls import path
from . import views
urlpatterns=[
    path("signup/",views.add_user,name='add_user'),
    path("generate_unique_userid/",views.generate_unique_userid,name='generate_unique_userid')
]