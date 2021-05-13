from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from books.models import Genres, Format, Book, Review, Order
from books.permission import IsAdminPermission
from books.serializers import GenresSerializer, FormatSerializer, BookListSerializer, ReviewSerializer, BookSerializer


class GenresListView(ListAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class FormatListView(ListAPIView):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = 'slug'
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['format__slug', 'genre', 'author']
    search_fields = ['title', 'author', 'genre__title', 'description']
    ordering_fields = ['title', ]

    @action(['GET'], detail=True)
    def review(self, request, slug=None):
        book = self.get_object()
        reviews = book.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def order(self, request, slug=None):
        print(request)
        book = self.get_object()
        user = request.user
        try:
            order = Order.objects.get(book=book, user=user)
            order.is_ordered = not order.is_ordered
            order.save()
            message = 'Вы заказали книгу' if order.is_ordered else 'Вы отменили заказ'
        except Order.DoesNotExist:
            Order.objects.create(book=book, user=user, is_ordered=True)
            message = 'Вы заказали книгу'
        return Response(message, status=200)

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminPermission]
        elif self.action == 'like':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [perm() for perm in permissions]


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'books': reverse('book-list', request=request, format=format),
        'genres': reverse('genres-list', request=request, format=format),
        'formats': reverse('formats-list', request=request, format=format),
    })


class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.none()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ]
