from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .viewsets import UserViewSet, NewsViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token, name='api-token'),
]
