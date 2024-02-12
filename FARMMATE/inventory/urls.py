from django.urls import path
from .views import *
urlpatterns = [
    path('inventory/graph/',graph_view,name='graph'),
    path('inventory/list/',InventoryList.as_view(),name='inventory-list'),
    path('full-inventory/list/',FullInventoryList.as_view(),name='inventory-list-full'),
    path('inventory/details/<int:pk>/',InventoryDetail.as_view(),name='inventory-detail'),
    path('inventory/update/<int:pk>/',InventoryUpdate.as_view(),name='inventory-item-update'),
    path('inventory/delete/<int:pk>/',InventoryItemDelete.as_view(),name='inventory-item-delete'),
]