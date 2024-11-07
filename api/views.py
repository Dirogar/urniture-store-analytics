"""
Представления для работы api.

Возвращает данные о продуктах, магазинах и комментариях.
"""
from rest_framework import viewsets

from reports.models import Store, Product, Warehouse

from .serializers import ProductSerializer, WarehouseSerializer, StoreSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Возвращает информацию о продуктах."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'article'
    http_method_names = ['get', 'post']


class WarehouseViewSet(viewsets.ModelViewSet):
    """Возвращает информацию о складах."""

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    http_method_names = ['get']


class StoreViewSet(viewsets.ModelViewSet):
    """Возвращает информацию о магазинах."""

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
