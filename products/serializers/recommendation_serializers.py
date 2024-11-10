from rest_framework import serializers

from products.models.recpmmendation_entity import RecommendationEntity


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationEntity
        fields = ['product_info']