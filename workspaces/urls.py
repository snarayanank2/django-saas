from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'workspaces', views.WorkspaceViewSet)
router.register(r'workspaceusers', views.WorkspaceUserViewSet)
router.register(r'workspaceschedules', views.WorkspaceScheduleViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'comments', views.CommentViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/basic/', views.BasicAuthSigninView.as_view()),
    path('auth/token/refresh/', views.RefreshTokenView.as_view()),
    path('attachments/', views.AttachmentUploadView.as_view()),
    path('attachments/<int:pk>/', views.AttachmentDownloadView.as_view()),
]
