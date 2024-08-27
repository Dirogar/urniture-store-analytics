from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
import json

from reports.models import StoreProduct, Product, Store
from .serializers import StoreProductSerializer, ProductSerializer


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class ProductDetailView(CreateRetrieveViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'article'



class StoreProductUpsertView(viewsets.ModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer

    def create(self, request, *args, **kwargs):
        """
        Создает новую запись или обновляет существующую в таблице `StoreProduct`.

        Метод выполняет поиск записи в таблице `StoreProduct` на основе полей `product` и `store`.
        Если запись существует, она обновляется с новыми значениями. Если запись не найдена, создается новая.

        :param request: HTTP запрос, содержащий данные в формате JSON. Ожидаемые ключи:
            - product_article (str): Артикул продукта, используемый для поиска объекта `Product`.
            - store (int): Идентификатор магазина, используемый для поиска объекта `Store`.
            - plan_exhibition (int): Новое значение для поля `plan_exhibition`.
        :param args: Дополнительные позиционные аргументы.
        :param kwargs: Дополнительные именованные аргументы.
        :return: HTTP Response с сериализованными данными обновленной или созданной записи, и соответствующим статусом:
            - HTTP 200 OK: если запись была обновлена.
            - HTTP 201 Created: если запись была создана.
            - HTTP 404 Not Found: если объекты `Product` или `Store` не были найдены.
            - HTTP 400 Bad Request: в случае других ошибок.
        """
        product_article: str = request.data.get('product_article')
        store_id: int = request.data.get('store')
        plan_exhibition: int = request.data.get('plan_exhibition')

        try:
            product: object = Product.objects.get(article=product_article)
            store: object = Store.objects.get(id=store_id)
            try:
                storeproduct = StoreProduct.objects.get(product=product,
                                                        store=store)
                storeproduct.plan_exhibition = plan_exhibition
                storeproduct.save()
                return Response(status=status.HTTP_200_OK)
            except StoreProduct.DoesNotExist:
                storeproduct = StoreProduct.objects.create(
                    store=store,
                    product=product,
                    plan_exhibition=plan_exhibition
                )
                return Response(StoreProductSerializer(storeproduct).data,
                                status=status.HTTP_201_CREATED)

        except (Product.DoesNotExist, Store.DoesNotExist) as e:
            return Response({'error': str(e)},
                            status=status.HTTP_404_NOT_FOUND)

