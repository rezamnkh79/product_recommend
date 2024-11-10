from rest_framework import serializers

from buying.models import CartItemEntity, CartEntity
from products.serializers.product_serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItemEntity
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartEntity
        fields = ['id', 'user', 'cart_items', 'total_price']
