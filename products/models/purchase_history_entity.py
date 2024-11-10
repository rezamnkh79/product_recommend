from django.db import models

from products.models.product_entity import ProductEntity
from users.models.custom_user_entity import CustomUserEntity


class PurchaseHistory(models.Model):
    user = models.ForeignKey(CustomUserEntity, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductEntity, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    device_type = models.CharField(max_length=50, choices=[('mobile', 'Mobile'), ('desktop', 'Desktop')])

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def day_of_week(self):
        return self.created_at.weekday()

    @property
    def hour_of_day(self):
        return self.created_at.hour

    @property
    def season(self):
        month = self.created_at.month
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'
