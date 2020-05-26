from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'client_applications', views.ClientApplicationViewSet)
router.register(r'workspaces', views.WorkspaceViewSet)
router.register(r'workspace_users', views.WorkspaceUserViewSet)

router.register(r'schedules', views.ScheduleViewSet)
# router.register(r'users', views.UserViewSet)

router.register(r'tags', views.TagViewSet)
router.register(r'comments', views.CommentViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/basic/signin/', views.BasicAuthSigninView.as_view()),
    path('auth/basic/signup/', views.BasicAuthSignupView.as_view()),
    path('auth/refresh_token/', views.RefreshTokenView.as_view()),
    path('attachments/', views.AttachmentUploadView.as_view()),
    path('attachments/<int:pk>/', views.AttachmentDownloadView.as_view()),
]
