from django.urls import include, path
from saas_framework.oauth2 import views

urlpatterns = [
    path('o/authorize/', views.OAuth2Authorize.as_view()),
    path('o/token/', views.OAuth2Token.as_view()),
]