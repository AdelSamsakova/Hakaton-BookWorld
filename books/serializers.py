from rest_framework import serializers

from books.models import Genres, Format, Book, Review


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('title', )


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ('title', )


# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         formats = validated_data.pop('formats', [])
#         book = Book.objects.create(author=user, **validated_data)
#         book.formats.add(*formats)
#         return book
class BookListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='book-detail', lookup_field='slug')

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'cover',]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise(serializers.ValidationError('Оценка от 1 до 5'))
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        review = Review.objects.create(user=user, **validated_data)
        return review
