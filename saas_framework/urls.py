from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('saas_framework.auth.urls')),
    path('common/', include('saas_framework.common.urls')),
    path('admin/', include('saas_framework.admin.urls')),
]