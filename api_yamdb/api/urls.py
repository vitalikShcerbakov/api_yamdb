from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, ReviewsViewSet

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'/titles/(?P<titles_id>\d+)/reviews/',
    ReviewsViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
