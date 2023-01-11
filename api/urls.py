from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('', views.RoutesView.as_view()),
    path('auth/user/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('services/', views.ServiceCRUDView.as_view())
]
