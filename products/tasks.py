# recommendations/tasks.py
import json
from datetime import timedelta

import redis
from celery import shared_task

from products.models.recpmmendation_entity import RecommendationEntity
from products.recommendation_manager import RecommendationManager
from users.models import CustomUserEntity


@shared_task
def generate_recommendations():
    r = redis.Redis(host='localhost', port=6379, db=0)
    users = CustomUserEntity.objects.all()
    similarity_matrix = RecommendationManager().get_similarity_matrix()
    for user in users:
        recommended_products_info = list()
        recommended_products_ids = RecommendationManager().get_similar_products_by_text(user=user,
                                                                                        similarity_matrix=similarity_matrix)
        for product in recommended_products_ids:
            recommend_obj = RecommendationEntity.objects.create(user=user, product=product)
            recommended_products_info.append(recommend_obj.product_info)
        r.setex(f"recommended_products:{user.id}", timedelta(hours=24), json.dumps(recommended_products_info))
    return 'Recommendation task completed'
