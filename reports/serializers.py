from rest_framework import serializers

from models import StoreProduct, Comment, Store


class StoreProductSerializer(serializers.ModelSerializer):
    product_article = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StoreProduct
        fields = ('plan_exhibition', 'store_id', 'product_article')
