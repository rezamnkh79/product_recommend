from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from products.models import ProductEntity, BrowsingHistory
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q


@csrf_exempt
def search_products(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({"message": "Search query is empty!"}, status=400)

    # Search for products by name or description
    products = ProductEntity.objects.filter(
        Q(name__icontains=query) | Q(category__icontains=query) | Q(tags__icontains=query)
    )

    # Prepare the response
    product_list = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
        }
        for product in products
    ]

    return JsonResponse({"products": product_list})


@csrf_exempt
def track_browsing_history(request):
    user_id = request.user.id  # Assuming the user is logged in
    product_id = request.POST.get('product_id')
    device_type = request.POST.get('device_type', 'desktop')  # Default to desktop if not provided
    duration = int(request.POST.get('duration', 0))  # Duration in seconds

    if not product_id:
        return JsonResponse({"message": "Product ID is required."}, status=400)

    # Record browsing history
    product = get_object_or_404(ProductEntity, id=product_id)

    # Store the browsing history
    browsing_history = BrowsingHistory.objects.create(
        user_id=user_id,
        product=product,
        duration=duration,
        device_type=device_type,
        viewed_at=timezone.now()
    )

    return JsonResponse({"message": "Browsing history saved."})
