from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, GenreViewSet, UserViewSet, SignUpViewSet, ReviewsViewSet,
                    TokenViewSet)


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
router.register('genres', GenreViewSet, basename='genres')

router.register(
    r'titles/(?P<titles_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router.register('auth/signup', SignUpViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenViewSet.as_view(), name='token'),
]
