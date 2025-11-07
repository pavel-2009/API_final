from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, 'categories')
router.register('genres', views.GenreViewSet, 'genres')

urlpatterns = [
    path('api/', include((router.urls, 'api'), namespace='api'))
]

