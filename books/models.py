from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint
from pytils.translit import slugify

User = get_user_model()


class Genres(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from pytils.translit import slugify
            self.slug = slugify(self.title)
        super().save()


class Format(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(primary_key=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Book(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=100, primary_key=True)
    author = models.CharField(max_length=200)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, related_name='books')
    format = models.ManyToManyField(Format)
    cover = models.ImageField(upload_to='books_cover/')
    description = models.TextField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=1)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']
        constraints =[
            CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='rating_range'
            )
        ]


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    is_ordered = models.BooleanField(default=False)





