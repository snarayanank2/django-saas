from django.urls import include, path
from rest_framework import routers
from server.admin import views

router = routers.DefaultRouter()
router.register(r'tpas', views.ThirdPartyAppViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'schedules', views.ScheduleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls))
]
