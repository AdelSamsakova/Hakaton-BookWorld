from django.contrib import admin

from books.models import Genres, Format, Book, ExtraTableForPrice

admin.site.register(Genres)
admin.site.register(Format)
admin.site.register(Book)
admin.site.register(ExtraTableForPrice)