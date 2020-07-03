from django.urls import include, path
from rest_framework import routers
from tutorial.workspaces import views

router = routers.DefaultRouter()
router.register(r'', views.WorkspaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]