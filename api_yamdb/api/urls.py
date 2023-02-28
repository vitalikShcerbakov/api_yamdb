from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, ReviewsViewSet

router = DefaultRouter()
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<titles_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
router.register(
    r'titles/(?P<id>\d+)/reviews/',
    ReviewsViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]