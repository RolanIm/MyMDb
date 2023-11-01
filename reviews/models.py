from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .validators import UnicodeUsernameValidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]


class Author(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, "
            "digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), blank=True)
    role = models.CharField(default=USER, choices=ROLES, max_length=9)
    bio = models.TextField()
    first_name = models.CharField(_("first name"),
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField(_("last name"),
                                 max_length=150,
                                 blank=True)

    class Meta:
        ordering = ('id',)


class Category(models.Model):
    name = models.CharField(_("name"), max_length=256)
    slug = models.SlugField(_("slug"),
                            db_index=True,
                            unique=True,
                            max_length=50)


class Genre(models.Model):
    name = models.CharField(_("name"), max_length=256)
    slug = models.SlugField(_("slug"),
                            db_index=True,
                            unique=True,
                            max_length=50)


class Comment(models.Model):
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    text = models.CharField(_("text"), max_length=256)
    pub_date = models.DateTimeField(_("publication date"), auto_now_add=True)


class Review(models.Model):
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    text = models.TextField(_("text"))
    comments = models.ForeignKey(to=Comment,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)
    score = models.IntegerField(_("score"), validators=[
        MinValueValidator(1, 'Score must be >= 1'),
        MaxValueValidator(10, 'Score must be <= 10')
    ])
    pub_date = models.DateTimeField(_("publication date"), auto_now_add=True)


class Title(models.Model):
    name = models.CharField(_("name"), max_length=256)  # required
    year = models.IntegerField(_("year"))
    # average_rating = models.IntegerField() in the serializer
    description = models.TextField(_("description"),
                                   blank=True,
                                   null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(to=Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True)
    reviews = models.ForeignKey(to=Review,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)


class GenreTitle(models.Model):
    title = models.ForeignKey(to=Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(to=Genre,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
