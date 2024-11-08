"""Маршруты для api."""
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, WarehouseViewSet, StoreViewSet


v1_router = DefaultRouter()
v1_router.register(r'products', ProductViewSet, basename='products')
v1_router.register(r'warehouses', WarehouseViewSet, basename='warehouses')
v1_router.register(r'stores', StoreViewSet, basename='stores')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
