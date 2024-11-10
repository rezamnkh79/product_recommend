from django.db import models

from buying.models.cart_entity import CartEntity
from products.models.product_entity import ProductEntity


class CartItemEntity(models.Model):
    cart = models.ForeignKey(CartEntity, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(ProductEntity, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
