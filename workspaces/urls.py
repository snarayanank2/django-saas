from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('workspaces.auth.urls')),
    path('common/', include('workspaces.common.urls')),
    path('admin/', include('workspaces.admin.urls')),
]