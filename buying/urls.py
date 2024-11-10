from django.urls import path

from buying.views.checkout_view import CheckoutView

from buying.views.cart_view import CartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='view-cart'),

    path('cart/add/', CartView.as_view(), name='add-to-cart'),

    path('cart/clear/', CartView.as_view(), name='clear-cart'),

    path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
]
