from rest_framework.generics import ListAPIView

from users.models.custom_user_entity import CustomUserEntity
from users.serializers.user_serializers import UserSerializer


class UserView(ListAPIView):
    queryset = CustomUserEntity.objects.all()
    serializer_class = UserSerializer
