from django.db import models


class ProductEntity(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    tags = models.JSONField()
    rating = models.FloatField()
    price = models.IntegerField()
