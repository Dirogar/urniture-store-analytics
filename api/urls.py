"""Маршруты для api."""
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import StoreProductUpsertView, ProductViewSet


v1_router = DefaultRouter()
v1_router.register(r'storeproduct', StoreProductUpsertView,
                   basename='storeproduct')
v1_router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
