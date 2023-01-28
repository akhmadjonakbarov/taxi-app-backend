from django.urls import path
from . import views

urlpatterns = [
    path('', views.RoutesView.as_view()),
    path('auth/user/login/', views.LoginView.as_view(), name='login'),
    path('auth/user/register/', views.RegisterView.as_view(), name='register'),
    path('services/', views.ServiceGetView.as_view()),
    path('cudservices/', views.ServiceCUDView.as_view())
]
