from django.urls import include, path
from saas_framework.auth.views import RefreshTokenView, JwtDecode
from saas_framework.identity.views import BasicAuthSigninView, BasicAuthSignupView
from saas_framework.oauth2.views import OAuth2Authorize, OAuth2Token
from saas_framework.tpas.views import ThirdPartyAppViewSet
from server.auth.views import WorkspaceViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'o/tpas', ThirdPartyAppViewSet)
router.register(r'workspaces', WorkspaceViewSet)


urlpatterns = [
    path('token/', RefreshTokenView.as_view()),
    path('jwt/decode/', JwtDecode.as_view()),
    path('basic/signin/', BasicAuthSigninView.as_view()),
    path('basic/signup/', BasicAuthSignupView.as_view()),
    path('o/authorize/', OAuth2Authorize.as_view()),
    path('o/token/', OAuth2Token.as_view()),
    path('', include(router.urls)),
]
