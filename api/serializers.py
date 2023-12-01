from django.db.models import Avg, F
from rest_framework import serializers

import datetime as dt

from reviews.models import Author, Category, Genre, Title, GenreTitle
from reviews.validators import UnicodeUsernameValidator, validate_username


USERNAME_VALIDATORS = [UnicodeUsernameValidator, validate_username]

GENRES = [
    (genre, genre) for genre in ('drama', 'comedy', 'western', 'fantasy',
                                 'sci-fi', 'detective', 'thriller', 'tale',
                                 'gonzo', 'roman', 'ballad', 'rock-n-roll',
                                 'classical', 'rock', 'chanson')
]
CATEGORIES = ('movie', 'book', 'music')


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
    slug = serializers.ChoiceField(choices=CATEGORIES)

    class Meta:
        model = Category
        required_fields = ('name', 'slug')
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.ChoiceField(choices=GENRES)

    class Meta:
        model = Genre
        required_fields = ('name', 'slug')
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        required_fields = ('name', 'year', 'genre', 'category')
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')

    @staticmethod
    def get_rating(obj):
        result = obj.reviews.aggregate(
            rating=Avg(F('score'), default=0))
        return result['rating']

    def create(self, validated_data):
        title = Title.objects.create(**validated_data)
        if 'genre' in self.initial_data:
            genres = validated_data.pop('genre')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(
                    name=genre,
                    slug=genre
                )
                GenreTitle.objects.create(title=title, genre=current_genre)
        if 'category' in self.initial_data:
            categories = validated_data.pop('category')
            title = Title.objects.create(**validated_data)
            for category in categories:
                current_category, status = Category.objects.get_or_create(
                    name=category,
                    slug=category
                )
                GenreTitle.objects.create(title=title, genre=current_category)
        return title

    @staticmethod
    def validate_year(year):
        return year <= dt.datetime.now().year
