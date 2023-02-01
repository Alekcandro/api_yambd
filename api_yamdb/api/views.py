from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title
from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import AdminOrReadOnly
from .serializers import TitleSerializer, GetTitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


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
