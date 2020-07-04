from django.contrib import admin
from django.urls import include, path
from django.conf.urls import (handler400, handler403, handler404, handler500)
from tutorial.views import error404, error500

urlpatterns = [
    path('identity/', include('tutorial.identity.urls')),
    path('auth/', include('tutorial.auth.urls')),
    path('oauth2/', include('tutorial.oauth2.urls')),
    path('workspaces/', include('tutorial.workspaces.urls')),
    path('tpas/', include('tutorial.tpas.urls')),
    path('common/', include('tutorial.common.urls')),
    path('admin/', include('tutorial.admin.urls')),
]

handler404 = error404
handler500 = error500
