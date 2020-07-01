from django.urls import include, path

urlpatterns = [
    path('', include('saas_framework.auth.urls'))
]
