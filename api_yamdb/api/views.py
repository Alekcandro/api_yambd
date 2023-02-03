from django.shortcuts import render

# Create your views here.
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title, Genre, Category
from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, GetTitleSerializer,
                          GenreSerializer, TitleSerializer)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'get':
            return GetTitleSerializer
        return TitleSerializer
