from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('workspaces.common.urls')),
    path('admin/', include('workspaces.admin.urls')),
]