from rest_framework import routers, serializers, viewsets, generics

from booksmart.models import Book

class BookToEditSerializer(serializers.ModelSerializer):
    url_book = serializers.HyperlinkedIdentityField(
    view_name='browserapi:book-detail', read_only=True)
    summary = serializers.CharField(write_only=True)
    class Meta:
        model = Book
        
        fields = ['id', 'title', 'url_book', 'author',  'summary', 'published', 'category', 'language', 'epub', 'isbn',  'embeddable', 'imageLinks' ]

