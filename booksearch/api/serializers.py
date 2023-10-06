from rest_framework import serializers
from booksmart.models import Book, Author

class NewBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['google_id', 'title', 'author', 'category', 'summary', 'published', 'preview_link', 'language', 'imageLinks', 'selfLink', 'isbn', 'epub', 'embeddable', 'preview_link_new', 'user_num_b', 'surname', 'owner']

class NewAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['author_wiki_link_d', 'author_wiki_link', 'first_name', 'middle_name', 'last_name', 'author_name', 'date_of_birth', 'date_of_death', 'wiki_idx', 'author_wiki_img', 'user_num_a', 'owner']


