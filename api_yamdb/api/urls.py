from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path, include

from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, 'categories')
router.register('genres', views.GenreViewSet, 'genres')
router.register('titles', views.TitleViewSet, 'titles')

nested_router = NestedSimpleRouter(router, r'titles', lookup='title')
nested_router.register('reviews', views.ReviewViewSet, basename='reviews')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(nested_router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token'),
]


