from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка Категорий."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка Жанров."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка Произведений."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
    )
    list_filter = ('name',)
    search_fields = ('name', 'year')
