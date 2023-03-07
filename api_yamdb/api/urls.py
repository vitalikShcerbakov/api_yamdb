from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewsViewSet, SignUpViewSet, TitleViewSet,
                    TokenViewSet, UserViewSet, UserViewEditProfile)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<titles_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router.register('auth/signup', SignUpViewSet)

urlpatterns = [
    path('v1/users/me/', UserViewEditProfile.as_view(), name='get_profile'),
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenViewSet.as_view(), name='token'),
]
