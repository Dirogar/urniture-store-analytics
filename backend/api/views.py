"""
Представления для работы api.

Возвращает данные о продуктах, магазинах и комментариях.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from backend.reports.models import Store, Product, Warehouse, StoreProduct

from .serializers import ProductSerializer, WarehouseSerializer, \
    StoreSerializer, StoreProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Возвращает информацию о продуктах."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'article'
    http_method_names = ['get', 'patch']


class StoreProductViewSet(viewsets.ModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer

    def get_object(self):
        store_id = self.kwargs.get('store_id')
        product_article = self.kwargs.get('product_article')
        return get_object_or_404(StoreProduct, store_id=store_id,
                                 product__article=product_article)


class WarehouseViewSet(viewsets.ModelViewSet):
    """Возвращает информацию о складах."""

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    http_method_names = ['get']


class StoreViewSet(viewsets.ModelViewSet):
    """Возвращает информацию о магазинах."""

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    http_method_names = ['get']
