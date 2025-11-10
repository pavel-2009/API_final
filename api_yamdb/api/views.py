from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import MethodNotAllowed

from yamdb import models
from . import serializers


class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed()


class GenreViewSet(ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)    


class TitleViewSet(ModelViewSet):
    queryset = models.Titles.objects.all()
    serializer_class = serializers.TitleSerializer
