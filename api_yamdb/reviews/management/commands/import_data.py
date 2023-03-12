import csv
import os
import sys

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)


class Command(BaseCommand):
    TABLES = (
        ('users.csv', User,
            ('id', 'username', 'email', 'role', 'bio',
             'first_name', 'last_name')),
        ('genre.csv', Genre,
            ('id', 'name', 'slug')),
        ('category.csv', Category,
            ('id', 'name', 'slug')),
        ('titles.csv', Title,
            ('id', 'name', 'year', 'category_id')),
        ('genre_title.csv', GenreTitle,
            ('id', 'title_id', 'genre_id')),
        ('review.csv', Review,
            ('id', 'title_id', 'text', 'author_id', 'score', 'pub_date')),
        ('comments.csv', Comment,
            ('id', 'review_id', 'text', 'author_id', 'pub_date'))
    )

    DIR = settings.BASE_DIR
    STATIC = 'static'
    DATA = 'data'

    help = 'Импорт данных из static/data'

    def handle(self, *args, **kwargs):
        print('--Начинаем импорт данных--')
        for csv_name, model, fields in self.TABLES:
            try:
                csv_file = open(
                    os.path.join(self.DIR, self.STATIC, self.DATA, csv_name),
                    'r',
                    encoding='utf-8'
                )
            except FileNotFoundError:
                print(f'Файл {csv_name} не найден.')
                sys.exit()
            except OSError:
                print('Произошла ошибка операционной системы '
                      f'при попытке открыть файл {csv_name}.')
                sys.exit()
            except Exception as err:
                print(f'Неожиданная ошибка при открытии файла {csv_name}: ',
                      repr(err))
                sys.exit()
            else:
                with csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)
                    data_map = {}
                    obj = []
                    for row in reader:
                        for i in range(len(fields)):
                            data_map[fields[i]] = row[i]
                        obj.append(model(**data_map))
                    model.objects.bulk_create(obj)
                    print(f'Импорт из файла {csv_name} выполнен.')
        print('--Все импорты прошли успешно--')
