from rest_framework.response import Response
from rest_framework.views import APIView

from userapp.models import CustomUser
from serviceapp.models import Service

from .serializers import (CustomUserSerializer, ServiceSerializer)


class RoutesView(APIView):
    def get(self, request):
        routes = [
            {"GET": "api/"},
            {"GET": "api/users/"},
            {"GET": "api/services/"}
        ]
        return Response(routes)


class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass

    def patch(self, request):
        pass

    def delete(self, request):
        deleteId = self.request.query_params("deleteId")
        service = Service.objects.get(id=deleteId)
        service.delete()

