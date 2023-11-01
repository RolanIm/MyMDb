from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Author, Comment, Title, Category, Review, GenreTitle, Genre

admin.site.register(Author, UserAdmin)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Comment)
