from django.urls import include, path
from rest_framework import routers
from server.tpas import views

router = routers.DefaultRouter()
router.register(r'', views.ThirdPartyAppViewSet)

urlpatterns = [
    path('', include(router.urls)),
]