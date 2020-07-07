from django.contrib import admin
from django.urls import include, path
from django.conf.urls import (handler400, handler403, handler404, handler500)
from server.views import error404, error500

urlpatterns = [
    path('auth/', include('server.auth.urls')),
    path('common/', include('server.common.urls')),
    path('admin/', include('server.admin.urls')),
]

handler404 = error404
handler500 = error500
