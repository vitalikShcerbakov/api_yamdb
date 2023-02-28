from django.db import models


class Category(models.Model):
    """Категории."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True, )

    class Meta:
        ordering = ['name']

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


class GenreTitle(models.Model):
    """Вспомогательная табица Жанры-Произведения."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
