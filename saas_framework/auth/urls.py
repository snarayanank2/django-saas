from django.urls import include, path
from saas_framework.auth import views

urlpatterns = [
    path('token/', views.RefreshTokenView.as_view()),
    path('switch_workspace/', views.SwitchWorkspaceView.as_view()),
    path('jwt/decode/', views.JwtDecode().as_view()),
]