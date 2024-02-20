from django.urls import path
from .views import *
urlpatterns = [
    path('graph/',graph_view,name='graph'),
    path('list/',InventoryList.as_view(),name='inventory-list'),
    path('full-inventory-list/',FullInventoryList.as_view(),name='inventory-list-full'),
    path('details/<int:pk>/',InventoryDetail.as_view(),name='inventory-detail'),
    path('update/<int:pk>/',InventoryUpdate.as_view(),name='inventory-item-update'),
    path('delete/<int:pk>/',InventoryItemDelete.as_view(),name='inventory-item-delete'),
    path('gallery/',inventoryGallery,name='inventory-gallery'),
]