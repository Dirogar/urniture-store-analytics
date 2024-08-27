from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import StoreProductUpsertView, ProductDetailView


router = DefaultRouter()
router.register(r'storeproduct', StoreProductUpsertView,
                basename='storeproduct')
router.register(r'product', ProductDetailView, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]