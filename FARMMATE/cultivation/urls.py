from django.urls import path
from .views import *

urlpatterns=[
    path("add-product/",add_product,name='add-product'),
    path('list/',CultivationList.as_view(),name='cultivation-list'),
    path('shortList/',CultivationShortList.as_view(),name='cultivation-short-list'),
    path('details/<int:pk>/',CultivationDetail.as_view(),name='cultivation-detail'),
    path('update/<int:pk>/',CultivationUpdate.as_view(),name='cultivation-update'),
    path('current/',currentCultivation.as_view(),name='current-cultivation'),
    path('current/details/<int:pk>/',currentCultivationDetail.as_view(),name='current-cultivation-details'),
    path('inventory-add/<int:pk>/',addToInventory.as_view(),name='add-to-inventory'),
]