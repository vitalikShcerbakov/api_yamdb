from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Category, Comment, Genre, Reviews, Title


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass


class ReviewsInline(admin.TabularInline):
    """Вложенный список отзывов к произведению."""
    model = Reviews
    classes = ['collapse']
    max_num = 0    # убирает кнопку "Добавить отзыв"


class TitleForm(forms.ModelForm):
    """Форма для жанров к произведению."""
    genre = forms.ModelMultipleChoiceField(
        label='Жанры',
        queryset=Genre.objects.all(),
        widget=FilteredSelectMultiple('жанры произведения', is_stacked=False)
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    form = TitleForm
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    empty_value_display = '-пусто-'
    list_filter = ('category', )
    search_fields = ('name',)
    list_editable = ('category',)
    inlines = (ReviewsInline,)
    list_per_page = 15


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)
