from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'password',
            'is_active', 'is_staff', 'is_superuser', 'is_tailor','cnic','gender','phone_number','image'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
