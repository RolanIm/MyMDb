from django.db.models import Avg, F

from rest_framework import serializers

import datetime as dt

from reviews.models import Author, Category, Genre, Title, Review, Comment
from reviews.validators import UnicodeUsernameValidator, validate_username

USERNAME_VALIDATORS = [UnicodeUsernameValidator, validate_username]


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=USERNAME_VALIDATORS)
    confirmation_code = serializers.CharField(max_length=255)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=USERNAME_VALIDATORS)
    email = serializers.EmailField(required=True, max_length=254)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        required_fields = ('email', 'username')
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    @staticmethod
    def validate_username(value):
        return validate_username(value)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        required_fields = ('name', 'slug')
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        required_fields = ('name', 'slug')
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Title
        required_fields = ('name', 'year', 'genre', 'category')
        fields = '__all__'

    @staticmethod
    def get_rating(obj):
        result = obj.reviews.aggregate(
            rating=Avg(F('score'), default=None))
        return result['rating']


class TitleWriteSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         many=True,
                                         slug_field='slug')
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        required_fields = ('name', 'year', 'genre', 'category')
        fields = '__all__'

    @staticmethod
    def validate_year(year):
        if not year <= dt.datetime.now().year:
            raise serializers.ValidationError(
                "year field can't be in the feature"
            )
        return year

    @staticmethod
    def get_rating(obj):
        result = obj.reviews.aggregate(
            rating=Avg(F('score'), default=None))
        return result['rating']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        required_fields = ('text', 'score')
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        required_fields = ('text',)
        fields = ('id', 'text', 'author', 'pub_date')
