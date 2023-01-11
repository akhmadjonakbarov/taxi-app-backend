from rest_framework import serializers
from userapp.models import CustomUser
from serviceapp.models import Service


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )


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
