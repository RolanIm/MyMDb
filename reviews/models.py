from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

ROLES = [
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
]


class Author(models.Model):
    bio = models.TextField()
    role = models.CharField(default='user', choices=ROLES, max_length=9)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.CharField(max_length=64)
    pub_date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[
        MinValueValidator(1, 'Score must be >= 1'),
        MaxValueValidator(10, 'Score must be <= 10')
    ])
    pub_date = models.DateTimeField(auto_now_add=True)


class Title(models.Model):
    name = models.CharField(max_length=45)  # required
    year = models.IntegerField()
    # average_rating = models.IntegerField() in the serializer
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE)


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
