from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path, include

from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, 'categories')
router.register('genres', views.GenreViewSet, 'genres')
router.register('titles', views.TitleViewSet, 'titles')

reviews_router = NestedSimpleRouter(router, r'titles', lookup='title')
reviews_router.register('reviews', views.ReviewViewSet, basename='reviews')

comments_router = NestedSimpleRouter(reviews_router, r'reviews', lookup='review')
comments_router.register('comments', views.CommentViewSet, basename='comments')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(reviews_router.urls)),
    path('api/', include(comments_router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token'),
]


