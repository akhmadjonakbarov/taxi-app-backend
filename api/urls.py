from django.urls import path
from . import views

urlpatterns = [
    path('', views.RoutesView.as_view()),
    path('users/', views.UserListView.as_view()),
    path('services/', views.ServiceListView.as_view())
]
