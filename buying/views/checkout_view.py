from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from buying.models import CartEntity


class CheckoutView(CreateAPIView, ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartEntity.objects.all()

    def get(self, request, *args, **kwargs):
        history = CartEntity.objects.filter(user_id=request.user.id).order_by('-created_at')

        return render(request, 'buy/checkout_history.html', {'history': history})

    def create(self, request, *args, **kwargs):
        cart: CartEntity = CartEntity.objects.filter(user_id=request.user.id, is_deleted=False).first()
        if not cart:
            return Response({"error": "No items in cart"}, status=status.HTTP_400_BAD_REQUEST)
        cart_items = cart.cart_items.all()
        total_price = sum(item.total_price for item in cart_items)
        cart.status = "paid"
        cart.is_deleted = True
        cart.save()
        return Response({"message": "Checkout successful", "total_price": total_price}, status=status.HTTP_200_OK)
