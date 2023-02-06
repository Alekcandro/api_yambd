from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import  api_view
from reviews.models import Category, Genre, Title

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, CreateUserSerializer,
                          GenreSerializer, ReadTitleSerializer,
                          TitleSerializer)

User = get_user_model()


@api_view(['POST'])
def user_create_view(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    serializer.save()
    confirmation_code = default_token_generator.make_token(
        User.objects.get(email=email, username=username)
    )
    MESSAGE = (f'Здравствуйте, {username}! '
               f'Ваш код подтверждения: {confirmation_code}')
    send_mail(message=MESSAGE,
              subject='Confirmation code',
              recipient_list=[email],
              from_email=None)
    return Response(serializer.data, status=HTTPStatus.OK)

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
    # queryset = Title.objects.all().annotate(
    #     rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadTitleSerializer
        return TitleSerializer
