from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('individual/', include('workspaces.individual.urls')),
    path('admin/', include('workspaces.admin.urls')),
]