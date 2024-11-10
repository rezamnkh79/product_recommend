from django.db import models

from buying.models.cart_entity import CartEntity
from users.models.custom_user_entity import CustomUserEntity


# class OrderEntity(models.Model):
#     user = models.ForeignKey(CustomUserEntity, on_delete=models.CASCADE)
#     cart = models.ForeignKey(CartEntity, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=50, default='pending')
#
#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"
#
#     def complete_order(self):
#         self.cart.clear_cart()
#         self.status = 'completed'
#         self.save()
