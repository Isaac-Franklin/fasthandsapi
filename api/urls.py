from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    # MyTokenObtainPairSerializer,
    TokenRefreshView,
)

from .views import MyTokenObtainPairView

urlpatterns = [
    path('', views.Welcome_Page, name='Welcome_Page'),
    path('allartisans/', views.All_Users, name='All_Users'),
    path('register/', views.Register_User, name='Register_User'),
    path('userlogin/', views.Login_User, name='Login_User'),
    path('artisan/<str:email>/', views.Aritisan, name='Aritisan'),
    path('deleteartisan/<str:email>/', views.Delete_Aritisan, name='Delete_Aritisan'),
    path('searchlocation/<str:location>/', views.FindLocation, name='FindLocation'),
    # JWT
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


