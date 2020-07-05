from django.contrib import admin
from django.urls import include, path
from django.conf.urls import (handler400, handler403, handler404, handler500)
from server.views import error404, error500

urlpatterns = [
    path('identity/', include('server.identity.urls')),
    path('auth/', include('server.auth.urls')),
    path('oauth2/', include('server.oauth2.urls')),
    path('workspaces/', include('server.workspaces.urls')),
    path('tpas/', include('server.tpas.urls')),
    path('common/', include('server.common.urls')),
    path('admin/', include('server.admin.urls')),
]

handler404 = error404
handler500 = error500
