from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import (
    ServiceSerializer, CustomUserSerializer)
from serviceapp.models import Service


class RoutesView(APIView):
    def get(self, request):
        routes = [
            {"GET": "api/"},
            {"GET": "api/services/"},
            {"POST": "api/auth/login/"},
            {"POST": "api/auth/register/"},
        ]
        return Response(routes)


class GetUserView(APIView):
    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, many=True)
        return Response(serializer.data)


class ServiceCRUDView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        user_services = []
        services = Service.objects.all()
        # for service in services:
        #     if user.id == service.user.id:
        #         user_services.append(service)
        # if user_services is not None:
        #     serializer = ServiceSerializer(user_services, many=True)
        #     return Response(serializer.data)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data
        if user.is_authenticated:
            data['user'] = user.id
            serializer = ServiceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"Serializer did not pass valid"})
        return Response({"data": "access denied"})

    def patch(self, request):
        user = request.user
        if user.is_authenticated:
            data = request.data
            service = Service.objects.get(id=data['id'])
            if service.user == user:
                serializer = ServiceSerializer(service, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            return Response({"data": "service is not your"})
        return Response({"data": "access denied"})

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
