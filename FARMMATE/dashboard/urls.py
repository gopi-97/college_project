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
    path('inventorylist/',InventoryList.as_view(),name='inventory-list'),
    path('fullInventorylist/',FullInventoryList.as_view(),name='inventory-list-full'),
    path('inventoryDetails/<int:pk>/',InventoryDetail.as_view(),name='inventory-detail'),
    path('inventoryUpdate/<int:pk>/',InventoryUpdate.as_view(),name='inventory-update'),
    path('inventoryitemDelete/<int:pk>/',InventoryItemDelete.as_view(),name='inventory-item-delete'),
]