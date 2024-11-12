from rest_framework import serializers
from rest_framework.serializers import ValidationError

from reports.models import (StoreProduct, Comment, Store, Product, Warehouse,
                            WarehouseProduct, ProductMutableData)


class StoreProductSerializer(serializers.ModelSerializer):
    product_article = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )
    store = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all()
    )

    class Meta:
        model = StoreProduct
        fields = 'product_article', 'store', 'plan_exhibition'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ('name',)


class WarehouseProductSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)

    class Meta:
        model = WarehouseProduct
        fields = ('warehouse',)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ('id',)


class StoreProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)

    class Meta:
        model = StoreProduct
        exclude = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('store', 'author', 'id')


class ProductSerializer(serializers.ModelSerializer):
    warehouses = serializers.SerializerMethodField()
    stores = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    room_class = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['article', 'name', 'model', 'manufacturer',
                            'square',
                            'segment', 'matrix', 'category', 'warehouses']

    def get_warehouses(self, obj):
        warehouse_products = WarehouseProduct.objects.filter(product=obj)
        return {wp.warehouse.name: {
            'id': wp.warehouse_id,
            'stock': wp.stock}
            for wp in warehouse_products}

    def get_stores(self, obj):
        store_products = StoreProduct.objects.filter(product=obj)
        return {
            sp.store.name: {
                'id': sp.store_id,
                'plan_exibition': sp.plan_exhibition,
                'fact_exhibition': sp.fact_exhibition
            } for sp in store_products}

    def get_comments_count(self, obj):
        """Получение кол-ва комментариев."""
        comments = Comment.objects.filter(product=obj)
        return comments.count()

    def get_room_class(self, obj):
        """Получает данные из связанной таблицы ProductMutable по артикулу."""
        mutable_data = ProductMutableData.objects.filter(article=obj).first()
        return mutable_data.room_class if mutable_data else "Нет класса"



class StoreProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreProduct
        fields = ('plan_exhibition',)


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ('city',)
