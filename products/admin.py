from django.contrib import admin

from products.models import ProductEntity
from products.models import BrowsingHistory
from products.models import PurchaseHistory

# Register your models here.
admin.site.register(ProductEntity)
admin.site.register(BrowsingHistory)
admin.site.register(PurchaseHistory)
