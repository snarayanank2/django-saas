from django.urls import include, path
from rest_framework import routers
from tutorial.common import views

router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'attachments', views.AttachmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]