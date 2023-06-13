from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.views.generic.base import TemplateView


from AccountsApp.views import AccessMediaAPIView, ResultOpeningAccessClient

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('AccountsApp.urls')),

    #re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^media/(?P<path>.*)$', AccessMediaAPIView.as_view()),
    re_path(r'^static-admin/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^robots\.txt$',
        TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain')
        ),
    path('open-access/', ResultOpeningAccessClient.as_view(), name='open-access'),
]
