from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name', 'bio', 'role')
    search_fields = ('username', 'email',)
    list_editable = ('role',)
    empty_value_display = 'Пусто'