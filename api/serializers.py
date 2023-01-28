from rest_framework import serializers
from userapp.models import CustomUser
from serviceapp.models import Service


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name','last_name', 'phone_number', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name = validated_data['first_name'], 
            last_name = validated_data['last_name'],
            username=validated_data['phone_number'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
        )
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

    def get_name(self, user: CustomUser):
        name = f'{user.first_name} {user.last_name}'
        if name == '':
            name = user.email
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


