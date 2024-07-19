# customFit 앱 구현 테스트용 임시 모델 입니다!

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet

router = SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
