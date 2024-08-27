from rest_framework import serializers

from reports.models import StoreProduct, Comment, Store, Product


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


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('article', 'room_class',)
