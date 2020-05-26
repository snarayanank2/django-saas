from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('auth/basic/signin/', views.BasicAuthSigninView.as_view()),
    path('auth/basic/signup/', views.BasicAuthSignupView.as_view()),
    path('auth/refresh_token/', views.RefreshTokenView.as_view()),
]