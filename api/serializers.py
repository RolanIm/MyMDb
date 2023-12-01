from django.db.models import Avg, F

from rest_framework import serializers

import datetime as dt

from reviews.models import Author, Category, Genre, Title
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
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.ChoiceField(choices=GENRES)

    class Meta:
        model = Genre
        required_fields = ('name', 'slug')
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Title
        required_fields = ('name', 'year', 'genre', 'category')
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')

    @staticmethod
    def get_rating(obj):
        result = obj.reviews.aggregate(
            rating=Avg(F('score'), default=0))
        return result['rating']


class TitleWriteSerializer(serializers.ModelSerializer):
    # TODO: title object is creating, but genre and category fields are not.
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
        return year <= dt.datetime.now().year
