from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('', views.RoutesView.as_view()),
    path('auth/user/login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('auth/user/register/', views.RegisterView.as_view(), name='register'),
    path('auth/user/logout/', views.LogOutView.as_view(), name="logout"),
    path('auth/user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/', views.GetUserView.as_view()),
    path('services/', views.ServiceGetView.as_view()),
    path('cudservices/', views.ServiceCUDView.as_view())
]
