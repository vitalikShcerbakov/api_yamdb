from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GenreViewSet


router = DefaultRouter()
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
router.register('genres', GenreViewSet, basename='genres')    

urlpatterns = [
    path('v1/', include(router.urls)),
]
