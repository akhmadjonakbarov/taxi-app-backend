from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import (AllowAny, )
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from carapp.models import Car
from serviceapp.models import Service
from userapp.models import CustomUser
from .serializers import (
    ServiceSerializer, CustomUserSerializer, MyTokenObtainPairSerializer,
    CustomUserSerializerWithToken, ServiceUpdatedSerializer
)
import jwt


class RoutesView(APIView):
    main_url: str = "http://127.0.0.1:8000/"

    def get(self, request):
        routes = [
            {"GET": f"{self.main_url}api/"},
            {"GET": f"{self.main_url}api/services/"},
            {"POST": f"{self.main_url}api/auth/user/login/"},
            {"POST": f"{self.main_url}api/auth/user/register/"},
        ]
        return Response(routes)


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response({"user_info": serializer.validated_data, "status": HTTP_200_OK})


class LogOutView(APIView):
    def get(self, request):
        logout(request=request)
        return Response("logout")


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        try:
            user = CustomUser.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone_number'],
                username=data['phone_number'],
                password=make_password(data['password']),
            )

            serializer = CustomUserSerializerWithToken(user, many=False)

            return Response({"user_info": serializer.data})
        except:
            message = {'detail': 'User with this email already exists'}
            return Response(message, status=HTTP_400_BAD_REQUEST)


class GetUserView(APIView):

    def get(self, request):
        token = request.headers["Authorization"]
        token = str.replace(str(token), 'Bearer ', '')
        data = jwt.decode(token, "secret", algorithms=['HS256'])
        print(data)
        user = request.user
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data)


class ServiceGetView(APIView):
    parser_classes = [AllowAny, ]

    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


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
                user=user,
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
                serializer = ServiceUpdatedSerializer(
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
