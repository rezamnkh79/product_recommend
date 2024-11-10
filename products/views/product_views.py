from datetime import datetime

from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from products.models import ProductEntity, BrowsingHistory
from products.recommendation_manager import RecommendationManager
from products.serializers.product_serializers import ProductSerializer
from products.tasks import generate_recommendations


class ProductView(ListAPIView, RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = ProductEntity.objects.all()
    lookup_field = 'id'

    def __init__(self):
        super().__init__()
        self.recommendation_manager = RecommendationManager()

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            product = self.get_object()
            if product is not None:
                BrowsingHistory.objects.create(
                    user_id=request.user.id,
                    product=product,
                    duration=0,
                    device_type=request.query_params.get("device_type", ""),
                    viewed_at=datetime.now()
                )
            return render(request, 'product/product_detail.html', {'product': product})

        else:
            generate_recommendations.run()
            products = self.get_queryset()[:50]
            recommended_products = self.recommendation_manager.get_recommended_products(request.user)
            return render(request, 'product/product_list.html', {
                'products': products,
                'recommended_products': recommended_products
            })
