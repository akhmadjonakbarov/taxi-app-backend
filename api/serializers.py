from rest_framework import serializers, validators
from userapp.models import CustomUser
from serviceapp.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "id",
            "title",
            "description",
            "from_where",
            "to_where",
            "car_type",
            "user"
        )


class CustomUserSerializer(serializers.ModelSerializer):
    user_services = ServiceSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'user_services'
        )


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_driver'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        return user
