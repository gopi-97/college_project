from django.urls import path
from .views import *

urlpatterns=[
    path("add-product/",add_product,name='add-product'),
    path('cultivation/list/',CultivationList.as_view(),name='cultivation-list'),
    path('cultivation/ShortList/',CultivationShortList.as_view(),name='cultivation-short-list'),
    path('cultivation/Details/<int:pk>/',CultivationDetail.as_view(),name='cultivation-detail'),
    path('cultivation/Update/<int:pk>/',CultivationUpdate.as_view(),name='cultivation-update'),
    path('cultivation/current/',currentCultivation.as_view(),name='current-cultivation'),
    path('cultivation/current/details/<int:pk>/',currentCultivationDetail.as_view(),name='current-cultivation-details'),
    path('inventory/add/<int:pk>/',addToInventory.as_view(),name='add-to-inventory'),
]