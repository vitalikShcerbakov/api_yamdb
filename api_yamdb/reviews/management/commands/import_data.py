import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Reviews, Title, User, GenreTitle

TABLES = (
    ('users.csv', User,
     ('id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name')),
    ('genre.csv', Genre,
     ('id', 'name', 'slug')),
    ('category.csv', Category,
     ('id', 'name', 'slug')),
    ('titles.csv', Title,
      ('id', 'name', 'year', 'category_id' )),
    ('genre_title.csv', GenreTitle,
     ('id', 'title_id', 'genre_id')),
    ('review.csv', Reviews,
     ('id', 'titles_id', 'text', 'author_id', 'score', 'pub_date')),
    ('comments.csv', Comment,
     ('id', 'review_id', 'text', 'author_id', 'pub_date')
    )      
)

class Command(BaseCommand):
    help = 'Импорт данных из static/data'

    def handle(self, *args, **kwargs):
        print('--Начинаем импорт данных--')
        for csv_f, model, fields in TABLES:
            # открываем файл
            with open(
                f'{settings.BASE_DIR}\static\data\{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.reader(csv_file)
                next(reader)    # Пропускаем звголовки
                data_map = {}
                obj = []
                for row in reader:
                    for i in range(len(fields)):
                        # формируем словарь имя_поля = значение
                        data_map[fields[i]] = row[i]
                    obj.append(model(**data_map))  # Добавляем в список модель
                model.objects.bulk_create(obj)
                print(f'Импорт из файла {csv_f} выполнен.')
        print('--Все импорты прошли успешно--')