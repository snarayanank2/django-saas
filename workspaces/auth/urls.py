from django.urls import include, path
from workspaces.auth import views

urlpatterns = [
    path('basic/signin/', views.BasicAuthSigninView.as_view()),
    path('basic/signup/', views.BasicAuthSignupView.as_view()),
    path('refresh_token/', views.RefreshTokenView.as_view()),
    path('switch_workspace/', views.SwitchWorkspaceView.as_view()),
]