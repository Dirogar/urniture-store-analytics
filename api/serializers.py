from rest_framework import serializers

from reports.models import (StoreProduct, Comment, Store, Product, Warehouse,
                            WarehouseProduct)


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

    class Meta:
        model = Product
        fields = '__all__'

    def get_warehouses(self, obj):
        warehouse_products = WarehouseProduct.objects.filter(product=obj)
        return {wp.warehouse.name: {
            'stock': wp.stock}
            for wp in warehouse_products}

    def get_stores(self, obj):
        store_products = StoreProduct.objects.filter(product=obj)
        return {
            sp.store.name: {
                'plan_exibition': sp.plan_exhibition,
                'fact_exhibition': sp.fact_exhibition
            } for sp in store_products}

    def get_comments_count(self, obj):
        comments = Comment.objects.filter(product=obj)
        return comments.count()