# recommendations/models.py

from django.db import models
from users.models.custom_user_entity import CustomUserEntity
from products.models.product_entity import ProductEntity
from datetime import timedelta
from django.utils import timezone


class RecommendationEntity(models.Model):
    user = models.ForeignKey(CustomUserEntity, on_delete=models.CASCADE, related_name='recommended_products')
    product = models.ForeignKey(ProductEntity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(hours=24))
    source = models.CharField(max_length=50,
                              choices=[('viewed', 'Viewed'), ('purchased', 'Purchased'), ('popular', 'Popular'),
                                       ('seasonal', 'Seasonal')], default='viewed')

    def __str__(self):
        return f"Recommended {self.product.name} for {self.user.username}"

    def is_valid(self):
        return timezone.now() < self.expires_at

    @property
    def product_info(self):
        return {
            "id": self.product.id,
            "name": self.product.name,
            "price": self.product.price,
            "category": self.product.category,
            "rating": self.product.rating,
        }
