import datetime

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from userapp.models import CustomUser
from serviceapp.models import Service


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = AccessToken

    @classmethod
    def get_token(cls, user: CustomUser):
        token = super().get_token(user=user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone_number'] = user.phone_number
        token['user_id'] = user.id

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = CustomUserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'phone_number', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['phone_number'],
                                              validated_data['password'])
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'services',
        )

    def get_services(self, obj: CustomUser):
        services = obj.get_services()
        serializer = ServiceSerializer(services, many=True)
        return serializer.data

    def get_name(self, obj: CustomUser):
        name = f'{obj.first_name} {obj.last_name}'
        if name == '':
            name = obj.email
        return name


class CustomUserSerializerWithSomeFields(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'phone_number',
            'first_name',
            'last_name',

        )


class ServiceSerializer(serializers.ModelSerializer):
    user = CustomUserSerializerWithSomeFields(many=False)

    class Meta:
        model = Service
        fields = (
            'id',
            'from_where',
            'to_where',
            'leaving_time',
            'service_price',
            'phone_number',
            'car_type',
            'user',
        )


class ServiceUpdatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id',
            'from_where',
            'to_where',
            'leaving_time',
            'service_price',
            'phone_number',
            'car_type',
        )


class CustomUserSerializerWithToken(CustomUserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'token',
        )

    def get_token(self, user: CustomUser):
        token = RefreshToken.for_user(user)
        return str(token.access_token)
