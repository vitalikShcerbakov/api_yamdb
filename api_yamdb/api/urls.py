from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewsViewSet, TitleViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import SignUpViewSet, TokenViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
#router.register('auth/signup', SignUpViewSet, basename='signup')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenViewSet.as_view(), name='token'),
    path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
    
]
