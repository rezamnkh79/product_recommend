import pickle

import redis
from django.db.models import Count
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from buying.models import CartItemEntity
from products.models import ProductEntity, BrowsingHistory, PurchaseHistory
from products.models.recpmmendation_entity import RecommendationEntity
from products.serializers.recommendation_serializers import RecommendationSerializer
from users.models import CustomUserEntity


class RecommendationManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    @staticmethod
    def get_personalized_product_recommendations(user):
        browsing_history = BrowsingHistory.objects.filter(user=user)
        viewed_products_ids = browsing_history.values_list('product_id', flat=True)
        cart_items = CartItemEntity.objects.filter(cart__user=user, cart__status='pending', cart__is_deleted=False)
        cart_products_ids = cart_items.values_list('product_id', flat=True)
        product_in_cart = ProductEntity.objects.filter(id__in=cart_products_ids)

        # Products that the user has viewed but not in the shopping cart
        pending_viewed_products = ProductEntity.objects.filter(id__in=viewed_products_ids).exclude(
            id__in=cart_products_ids)

        # User purchase history
        purchase_history = PurchaseHistory.objects.filter(user=user)
        purchased_products_ids = purchase_history.values_list('product_id', flat=True)

        # Similar products to previous purchases
        old_bought_products = ProductEntity.objects.filter(id__in=purchased_products_ids).exclude(
            id__in=viewed_products_ids)

        # Best selling products
        popular_products = ProductEntity.objects.annotate(purchase_count=Count('purchasehistory')).filter(
            purchase_count__gt=3)

        recommended_products_ids = list(pending_viewed_products) + list(old_bought_products) + list(
            popular_products) + list(product_in_cart)
        return set(recommended_products_ids)

    def calculate_product_similarity(self):
        products = ProductEntity.objects.all()
        product_features = [f"{product.name} {product.category}" for product in products]
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(product_features)
        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.redis_client.setex('product_similarity_matrix', 86400, pickle.dumps(similarity_matrix))  # 24 hours
        return similarity_matrix

    def get_similar_products_by_text(self, user: CustomUserEntity, similarity_matrix):
        recommended_products = self.get_personalized_product_recommendations(user)
        similar_products = {}
        product_ids = [prod.id for prod in ProductEntity.objects.all()]
        product_index_map = {prod_id: idx for idx, prod_id in enumerate(product_ids)}

        for prod in recommended_products:
            if prod.id in product_index_map:
                product_index = product_index_map[prod.id]
                similar_products[prod.id] = similarity_matrix[product_index]
            else:
                print(f"Warning: Product {prod.id} not found in similarity matrix!")

        recommended_products_with_similarity = []

        for prod_id, similarities in similar_products.items():
            similar_prod_ids = similarities.argsort()[-6:][::-1]  # six most similar product
            recommended_products_with_similarity.extend(ProductEntity.objects.filter(id__in=similar_prod_ids))
        return list(set(recommended_products_with_similarity))

    def get_similarity_matrix(self):
        cached_similarity = self.redis_client.get('product_similarity_matrix')
        if cached_similarity:
            similarity_matrix = pickle.loads(cached_similarity)
        else:
            similarity_matrix = self.calculate_product_similarity()

        return similarity_matrix

    def get_recommended_products(self, user):
        r = redis.Redis(host='localhost', port=6379, db=0)
        cached_recommendations = r.get(f"recommended_products:{user.id}")

        if cached_recommendations:
            print(f"Fetching recommendations for user {user.id} from Redis")
            recommended_products = eval(cached_recommendations)
        else:
            print(f"Fetching recommendations for user {user.id} from database")
            recommended_products_objs = self.get_recommendations_from_db(user)
            recommended_products = RecommendationSerializer(recommended_products_objs, many=True).data
            r.setex(f"recommended_products:{user.id}", 86400, str(recommended_products))
        return recommended_products

    def get_recommendations_from_db(self, user):
        recommended_products = RecommendationEntity.objects.filter(user_id=user.id)
        return recommended_products
