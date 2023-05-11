from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from AccountsApp.views import AccessMediaAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('AccountsApp.urls')),

    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^media/(?P<path>.*)$', AccessMediaAPIView.as_view()),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
