from django.contrib.auth import login
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.views import APIView
from rest_framework.serializers import DateTimeField
from knox.models import AuthToken
from knox.settings import knox_settings
from knox.views import LoginView as KnoxLoginView
from carapp.models import Car
from serviceapp.models import Service
from .serializers import (
    ServiceSerializer, CustomUserSerializer,
    RegisterSerializer
)


class RoutesView(APIView):
    permission_classes = (AllowAny,)
    main_url: str = "http://127.0.0.1:8000/"

    def get(self, request):
        routes = [
            {"GET": f"{self.main_url}api/"},
            {"GET": f"{self.main_url}api/services/"},
            {"POST": f"{self.main_url}api/auth/user/login/"},
            {"POST": f"{self.main_url}api/auth/user/register/"},
        ]
        return Response(routes)


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class RegisterView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def get_post_response_data(self, request, token, instance):
        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        return data

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer = CustomUserSerializer(user, many=False)
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(user, token_ttl)
        token = self.get_post_response_data(request, token, instance)

        return Response(
            {
                "user": serializer.data,
                "token": token
            }
        )


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def get_post_response_data(self, request, token, instance):
        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        return data

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, many=False)
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(user, token_ttl)
        token = self.get_post_response_data(request, token, instance)
        return Response({"user":serializer.data, "token":token})


class ServiceGetView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def get_queryset(self):
        return super().get_queryset()


class ServiceCUDView(APIView):
    # permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        data = request.data
        if user.is_authenticated:
            service = Service.objects.create(
                from_where=data['from_where'],
                to_where=data['to_where'],
                leaving_time=data['leaving_time'],
                phone_number=data['phone_number'],
                car_type=data['car_type'],
                service_price=data['service_price'],
                user_id=user.id,
            )
            serializer = ServiceSerializer(service, many=False)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response({"data": "access denied", "status": HTTP_400_BAD_REQUEST})

    def patch(self, request):
        user = request.user
        data = request.data
        if user.is_authenticated:
            service: Service = Service.objects.get(id=data['id'])
            if service.user.id == user.id:
                serializer = ServiceSerializer(
                    service, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=HTTP_200_OK)
                return Response(serializer.errors)
            return Response({"data": "service is not your"}, status=HTTP_400_BAD_REQUEST)
        return Response({"data": "access denied"}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if user.is_authenticated:
            deleteId = self.request.query_params.get("deleteId")
            service = Service.objects.get(id=deleteId)
            if service is not None:
                if service.user == user:
                    service.delete()
                    return Response({"data": "success"})
                return Response({"data": "user does not equal"})
            return Response({"data": "service is unavailable"})
        return Response({"data": "access denied"})


class CarsCUDView(APIView):
    def post(self):
        pass

    def patch(self):
        pass

    def delete(self, request):
        user = request.user
        if user.is_authenticated:
            deleteId = self.request.query_params.get("deleteId")
            car = Car.objects.get(id=deleteId)
            if car.user == user:
                car.delete()
            return Response({""})
