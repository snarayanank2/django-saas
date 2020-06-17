from django.urls import include, path
from rest_framework import routers
from tutorial.common import views

router = routers.DefaultRouter()
router.register(r'workspaces', views.WorkspaceViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'tpas', views.ThirdPartyAppViewSet)
router.register(r'attachments', views.AttachmentViewSet)

urlpatterns = [
    # path('attachments/', views.AttachmentUploadView.as_view()),
    # path('attachments/<int:pk>/', views.AttachmentDownloadView.as_view()),

    path('', include(router.urls)),
]