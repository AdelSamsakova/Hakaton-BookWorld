from rest_framework import serializers

from books.models import Genres, Format, Book, Review, ExtraTableForPrice


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('title', )


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraTableForPrice
        fields = ('formats', 'price', )


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ('title', )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        formats = validated_data.pop('format', [])
        book = Book.objects.create(**validated_data)
        book.format.add(*formats)
        return book

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = GenresSerializer(instance.genre, context=self.context).data
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['orders_count'] = instance.orders.count()
        representation['price'] = PriceSerializer(instance.books_price.all(), many=True).data
        return representation


class BookListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='book-detail', lookup_field='slug')

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'cover', 'details']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('user', 'book', 'text', 'rating', 'created_time')

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise(serializers.ValidationError('Оценка от 1 до 5'))
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        review = Review.objects.create(user=user, **validated_data)
        return review
