"""Маршруты для api."""
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, WarehouseViewSet


v1_router = DefaultRouter()
v1_router.register(r'product', ProductViewSet, basename='product')
v1_router.register(r'warehouses', WarehouseViewSet, basename='warehouses')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
