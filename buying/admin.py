from django.contrib import admin

from buying.models import CartEntity
from buying.models import CartItemEntity
# from buying.models import OrderEntity

# Register your models here.

admin.site.register(CartEntity)
admin.site.register(CartItemEntity)
# admin.site.register(OrderEntity)