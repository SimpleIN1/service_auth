
from django.urls import path, include, re_path

from rest_framework.routers import SimpleRouter

from .views import UserCreateViewSet, \
    JwtCreateTokenAPIView, \
    JwtRefreshTokenAPIView, \
    UserDetailDestroyUpdateViewSet, TestAPIView, OpeningAccessClientAPIView

router = SimpleRouter()
router.register(r'users', UserCreateViewSet)
router.register(r'user', UserDetailDestroyUpdateViewSet)

urlpatterns = [
    re_path(r'', include(router.urls), name='user'),

    re_path(r'^jwt/create/?', JwtCreateTokenAPIView.as_view(), name='jwt-create'),
    re_path(r'^jwt/refresh/?', JwtRefreshTokenAPIView.as_view(), name='jwt-refresh'),
    # re_path(r'^test_view/?', TestAPIView.as_view(), name='test-view'),
    # re_path(r'^access_client/?', OpeningAccessClientAPIView.as_view(), name='test-view'),
]
