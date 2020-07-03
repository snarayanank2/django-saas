from django.urls import include, path

urlpatterns = [
    path('', include('saas_framework.identity.urls')),
    path('', include('saas_framework.auth.urls')),
    path('', include('saas_framework.oauth2.urls'))
]
