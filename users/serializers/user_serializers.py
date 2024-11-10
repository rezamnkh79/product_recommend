from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models.custom_user_entity import CustomUserEntity


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserEntity
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'user': UserSerializer(self.user).data})
        return data
