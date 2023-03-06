from django.contrib import admin

from .models import Comment, Reviews, Title


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass
