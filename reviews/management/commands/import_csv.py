import os
import csv
from django.core.management.base import BaseCommand
from MyMDb.settings import BASE_DIR
from reviews.models import (Author,
                            Comment,
                            Review,
                            Category,
                            Genre,
                            Title,
                            GenreTitle)


class Command(BaseCommand):
    help = "This command writes csv data to models."

    MODELS_DICT = {
        'category.csv': Category,
        'genre.csv': Genre,
        'users.csv': Author,
        'titles.csv': Title,
        'genre_title.csv': GenreTitle,
        'review.csv': Review,
        'comments.csv': Comment,
    }

    def handle(self, *args, **options):
        csv_directory = os.path.join(BASE_DIR, 'static/data/')

        for csv_file, model in self.MODELS_DICT.items():
            with open(csv_directory + csv_file, encoding='utf-8') as csv_data:
                dict_reader = csv.DictReader(csv_data)
                model.objects.all().delete()
                model.objects.bulk_create(model(**data) for data in dict_reader)
            self.stdout.write(
                self.style.SUCCESS('Successfully import csv data.')
            )
