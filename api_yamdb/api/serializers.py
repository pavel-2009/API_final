from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound
from django.core.mail import send_mail
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
        extra_kwargs = {
            'text': {'required': True},
            'score': {'required': True},
            'author': {'read_only': True},  
            'title': {'read_only': True},   
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in representation.items():
            if value is None and isinstance(value, (int, float)):
                representation[key] = 0
        return representation



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field = 'username',
        read_only = True
    )

    class Meta:
        model = models.Comment
        fields = ['id', 'text', 'author', 'pub_date']
        extra_kwargs = {
            'text': {'required': True},
            'author': {'read_only': True},  
            'title': {'read_only': True},   
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in representation.items():
            if value is None and isinstance(value, (int, float)):
                representation[key] = 0
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username','email']

    def create(self, validated_data):
        if validated_data['username'] == 'me':
            raise serializers.ValidationError("Использование 'me' в качестве username запрещено.")
        user = models.User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_unusable_password()
        user.save()

        code = models.EmailCode.get_code()
        models.EmailCode.objects.create(user=user, code=code)

        send_mail(
            "Your confirmation code",
            f"Your code: {str(code)}",
            "noreply@example.com",
            [user.email],
        )

        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        username = attrs.get("username")
        code = attrs.get("code")

        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        try:
            user_code = models.EmailCode.objects.get(user=user)
        except models.EmailCode.DoesNotExist:
            raise serializers.ValidationError("Код для пользователя не найден")

        if user_code.code != code:
            raise serializers.ValidationError("Неверный код")


        self.user = user
        return attrs

    def create_token(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }