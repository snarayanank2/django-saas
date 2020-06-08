from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('tutorial.auth.urls')),
    path('common/', include('tutorial.common.urls')),
    path('admin/', include('tutorial.admin.urls')),
]