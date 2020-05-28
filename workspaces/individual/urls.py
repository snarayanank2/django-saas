from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'workspaces', views.WorkspaceViewSet)
router.register(r'accounts', views.AccountViewSet)

urlpatterns = [
    path('auth/basic/signin/', views.BasicAuthSigninView.as_view()),
    path('auth/basic/signup/', views.BasicAuthSignupView.as_view()),
    path('auth/refresh_token/', views.RefreshTokenView.as_view()),
    path('', include(router.urls)),
]