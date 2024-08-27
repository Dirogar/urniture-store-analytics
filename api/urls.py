from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import StoreProductUpsertView


router = DefaultRouter()
router.register(r'storeproduct', StoreProductUpsertView,
                basename='storeproduct')

urlpatterns = [
    path('', include(router.urls)),
]