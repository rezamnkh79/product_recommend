from django.db import models

from users.models.custom_user_entity import CustomUserEntity


class CartEntity(models.Model):
    user = models.ForeignKey(CustomUserEntity, on_delete=models.CASCADE, related_name='cart')
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.cart_items.all())

    def clear_cart(self):
        self.cart_items.all().delete()
