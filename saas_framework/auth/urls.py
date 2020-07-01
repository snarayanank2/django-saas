from django.urls import include, path
from saas_framework.auth import views

urlpatterns = [
    path('basic/signin/', views.BasicAuthSigninView.as_view()),
    path('basic/signup/', views.BasicAuthSignupView.as_view()),
    path('token/', views.RefreshTokenView.as_view()),
    path('switch_workspace/', views.SwitchWorkspaceView.as_view()),
    path('o/authorize/', views.OAuth2Authorize.as_view()),
    path('o/token/', views.OAuth2Token.as_view()),
#    path('jwt/encode/', views.JwtEncode().as_view()),
    path('jwt/decode/', views.JwtDecode().as_view()),
]