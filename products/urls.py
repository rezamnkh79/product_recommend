from django.urls import path

from products.views.product_views import ProductView
from products.views.search_purchase_view import track_browsing_history, search_products

urlpatterns = [
    path('<int:id>/', ProductView.as_view(), name='get_product_with_id'),
    path('', ProductView.as_view(), name='product_list'),
    path('search/', search_products, name='search_products'),
    path('browsing/history/', track_browsing_history, name='track_browsing_history'),
]
