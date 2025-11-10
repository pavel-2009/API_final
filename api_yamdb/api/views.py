from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import MethodNotAllowed

from yamdb import models
from . import serializers


class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class GenreViewSet(ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)    


class TitleViewSet(ModelViewSet):
    queryset = models.Titles.objects.all()
    serializer_class = serializers.TitleSerializer

#TODO: доделать: сделать нормальный срок токена, настроить поля и все такое
class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        title = self.kwargs.get('title')
        objects = get_object_or_404(models.Review, pk=title)
        return objects
    
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title')
        title = get_object_or_404(models.Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)