from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Category(models.Model):
    """Категории."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug категории'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категоря'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


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
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения')
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание')
    year = models.IntegerField(verbose_name='Год выпуска')
    # Одно произведение может быть привязано к _нескольким_ жанрам:
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    # Одно произведение может быть привязано _только к одной_ категории:
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Вспомогательная табица Жанры-Произведения."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name='Жанр')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Произведение')
    constraints = (
        UniqueConstraint(
            fields=('genre', 'title'),
            name='title_genre_unique',
        )
    )

    def __str__(self):
        return f'{""}'


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
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                10,
                message='Введенная оценка выше допустимой'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    
    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['titles', 'author'],
                name='unique_titles_author')
        ]

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

    class Meta:
        ordering = ('-pub_date',)
