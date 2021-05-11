from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from books.models import Genres, Format, Book, Review
from books.serializers import GenresSerializer, FormatSerializer, BookListSerializer, ReviewSerializer


class GenresListView(ListAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class FormatListView(ListAPIView):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer


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
