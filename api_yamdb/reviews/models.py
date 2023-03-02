from django.db import models

from users.models import User


class Genre(models.Model):
    """Жанры."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug жанра'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Title(models.Model):
    """Произведения."""
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(null=True, verbose_name='Описание')
    # Одно произведение может быть привязано к _нескольким_ жанрам:
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    # Одно произведение может быть привязано _только к одной_ категории:
    сategory = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )

    def __str__(self):
        return self.name


class Reviews(models.Model):
    """Отзывы."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    titles = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарий."""
    text = models.TextField()
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    """Вспомогательная табица Жанры-Произведения."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
