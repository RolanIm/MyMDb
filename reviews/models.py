from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from .validators import UnicodeUsernameValidator, validate_username

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]


class Author(AbstractUser):
    username_validators = [UnicodeUsernameValidator, validate_username]

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, "
            "digits and @/./+/-/_ only."
        ),
        validators=username_validators,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"),
                              unique=True,
                              max_length=254)
    role = models.CharField(default=USER, choices=ROLES, max_length=9)
    bio = models.TextField(blank=True, null=True)
    first_name = models.CharField(_("first name"),
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField(_("last name"),
                                 max_length=150,
                                 blank=True)

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.is_authenticated and self.role == MODERATOR

    @property
    def is_user(self):
        return self.is_authenticated and self.role == USER

    class Meta:
        ordering = ('id',)
        verbose_name = _('author')
        verbose_name_plural = _('authors')


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
    review = models.ForeignKey(to='Review',
                               on_delete=models.CASCADE,
                               related_name='comments')


class Review(models.Model):
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    text = models.TextField(_("text"))
    title = models.ForeignKey(to='Title',
                              on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.IntegerField(_("score"), validators=[
        MinValueValidator(1, 'Score must be >= 1'),
        MaxValueValidator(10, 'Score must be <= 10')
    ])
    pub_date = models.DateTimeField(_("publication date"), auto_now_add=True)


class Title(models.Model):
    name = models.CharField(_("name"), max_length=256)
    year = models.IntegerField(_("year"))
    description = models.TextField(_("description"),
                                   blank=True,
                                   null=True)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle')
    category = models.ForeignKey(to=Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True)


class GenreTitle(models.Model):
    title = models.ForeignKey(to=Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(to=Genre,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
