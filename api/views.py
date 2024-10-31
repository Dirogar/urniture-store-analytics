"""
Представления для работы api.

Возвращает данные о продуктах, магазинах и комментариях.
"""
from rest_framework import viewsets

from reports.models import Store, Product

from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Возвращает информацию о продуктах."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'article'
    http_method_names = ['get', 'post']


class StoreViewSet(viewsets.ModelViewSet):
    """Возвращает информацию о магазинах."""

    queryset = Store.objects.all()
