from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet

router = DefaultRouter()
router.register('genres', GenreViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
