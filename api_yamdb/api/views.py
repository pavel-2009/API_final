from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
import rest_framework.serializers as serializers_rest

from yamdb import models
from . import serializers, permissions as custom_permissions


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


class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        title = self.kwargs.get('title_pk')
        objects = get_object_or_404(models.Titles, pk=title)
        return objects.reviews.all()
    
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_pk')
        title = get_object_or_404(models.Titles, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        review = self.kwargs.get('review_pk')
        objects = get_object_or_404(models.Review, pk=review)
        return objects.comments.all()
    
    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_pk')
        review = get_object_or_404(models.Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all().order_by('id')
    permission_classes = (custom_permissions.IsAdmin,)
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class RegisterView(APIView):
    permission_classes = tuple()

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  
        return Response({'username': user.username, 'email': user.email}, status=status.HTTP_200_OK)

class TokenByCodeView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')

        if not username:
            raise serializers_rest.ValidationError({"username": "Это поле обязательно."})
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise NotFound("Пользователь не найден")

        serializer = serializers.TokenSerializer(
            data=request.data,
            context={"user": user}
        )
        serializer.is_valid(raise_exception=True)

        tokens = serializer.create_token()
        return Response(tokens, status=status.HTTP_200_OK)
