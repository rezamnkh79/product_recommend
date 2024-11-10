from rest_framework import serializers

from products.models.product_entity import ProductEntity


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductEntity
        fields = '__all__'
