from datetime import datetime

from django.core.validators import (RegexValidator, MinValueValidator,
                                    MaxValueValidator)
from django.db import models

from users.models import User


class CategoryGenreBase(models.Model):
    """Абстрактная модель для Category and Genre."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50,
                            validators=[RegexValidator(
                                regex=r'^[-a-zA-Z0-9_]+$',
                                message='Слаг содержит недопустимый символ.'
                            )])

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CategoryGenreBase):
    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBase):
    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(
            0, message='Значение не может быть отрицательным.'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Значение не может быть больше текущего года.'
            )
        ],
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True,
        related_name='titles',
        verbose_name='Жанр'

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Вспомогательная модель."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Ревью на произведение."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True
    )
    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Aвтор'
    )
    score = models.PositiveIntegerField(
        verbose_name='Oценка',
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
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review_for_title'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Коммент к определенному ревью."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='oтзыв',
    )
    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
