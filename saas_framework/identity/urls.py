from django.urls import include, path
from saas_framework.identity import views

urlpatterns = [
    path('basic/signin/', views.BasicAuthSigninView.as_view()),
    path('basic/signup/', views.BasicAuthSignupView.as_view()),
]