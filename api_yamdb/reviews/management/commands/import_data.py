import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Reviews, Title, User, GenreTitle

TABLES = {
    User: 'users.csv',
    Genre: 'genre.csv',
    Category: 'category.csv'
}

TABLES_WITH_FIELDS = (
    (
        Title,
        'titles.csv',
        {
            'id': 'id',
            'name': 'name',
            'year': 'year',
            'category_id': 'category'
        }),
    (  
        GenreTitle,
        'genre_title.csv',
        {
            'id': 'id',
            'title_id': 'title_id',
            'genre_id': 'genre_id'   
        }),
    (
        Reviews,
        'review.csv',
        {
            'id': 'id',
            'titles_id': 'title_id',
            'text': 'text',
            'author_id': 'author',
            'score': 'score',
            'pub_date': 'pub_date'
        }),
    (
        Comment,
        'comments.csv',
        {
            'id': 'id',
            'review_id': 'review_id',
            'text': 'text',
            'author_id': 'author',
            'pub_date': 'pub_date'
        }   
    )
)


class Command(BaseCommand):
    help = 'Импорт данных из static/data'

    def handle(self, *args, **kwargs):
        print('Начинаем импорт данных:')
        # импорт данных из файлов, где имена столбцов совпадают
        for model, csv_f in TABLES.items():
            with open(
                f'{settings.BASE_DIR}\static\data\{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                model(**data) for data in reader)
            print(f'Импорт в модель {model.__name__}, из файла {csv_f} выполнен.')

        # импорт данных из файлов, где имена столбцов не совпадают
        for model, csv_f, fields in TABLES_WITH_FIELDS:
            with open(
                f'{settings.BASE_DIR}\static\data\{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data_list ={}
                    for model_field in fields:
                        row_name = fields[model_field]
                        data_list[model_field] = row[row_name]
                    model_obj = model(**data_list)
                    model_obj.save()
                print(f'Импорт в модель {model.__name__}, из файла {csv_f} выполнен.')
                    