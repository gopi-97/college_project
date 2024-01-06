from django.urls import path
from .views import *

urlpatterns=[
    # path('home/',loadHome,name='home'),
    path("dashboard/",load_dash,name='dashboard'),
    path("add-product/",add_product,name='add-product'),
    path("add-field/",add_field,name='add-field'),
    path('graph/', graph_view,name='graph'),
    path('cultivationlist/',CultivationList.as_view(),name='cultivation-list'),
    path('cultivationDetails/<int:pk>/',CultivationDetail.as_view(),name='cultivation-detail'),
    path('cultivationUpdate/<int:pk>/',CultivationUpdate.as_view(),name='cultivation-update'),
]