from rest_framework import serializers
from datetime import datetime

from yamdb import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ['name', 'slug']

class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=models.Genre.objects.all()
    )


    class Meta:
        model = models.Titles
        fields = ['id', 'name', 'year', 'rating', 'description',
                'genre', 'category']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in representation.items():
            if not value:
                representation[key] = 0
        return representation
    
    def validate(self, attrs):
        if attrs['year'] > datetime.now().year:
            attrs['year'] = datetime.now().year
        return attrs
        

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in representation.items():
            if not value:
                representation[key] = 0
        return representation
