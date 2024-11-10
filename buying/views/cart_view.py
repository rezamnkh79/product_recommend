from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from buying.models import CartEntity, CartItemEntity
from buying.serializers.cart_serializers import CartItemSerializer
from products.models.product_entity import ProductEntity


class CartView(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        self.permission_classes = (AllowAny,)
        super().__init__()

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def get(self, request):
        cart = CartEntity.objects.filter(user_id=request.user.id, is_deleted=False).first()
        if not cart:
            return render(request, template_name='buy/cart.html')
        cart_items = CartItemEntity.objects.filter(cart_id=cart.id)
        response = render(request, template_name='buy/cart.html',
                          context={'cart_items': cart_items, 'total_price': cart.total_price})
        return response

    def post(self, request):
        cart, created = CartEntity.objects.get_or_create(user_id=request.user.id, is_deleted=False)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(ProductEntity, id=product_id)

        cart_item, created = CartItemEntity.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def delete(self, request):

        cart = CartEntity.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
            return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
