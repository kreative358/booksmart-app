from booksmart.models import Book, Author 
from rest_framework.reverse import reverse

from rest_framework import routers, serializers, viewsets, generics
from booksmart.models import Book
from booksmart.api.serializer import BookToEditSerializer

class FilterList(generics.ListAPIView):
    """
    Return a list of all the products that the authenticated
    user has ever purchased, with optional filtering.
    """
    model = Book
    serializer_class = BookToEditSerializer

    def get_queryset(self):
        user = self.request.user
        user_query = Book.objects.filter(owner=user)
        return user_query
        # return user.purchase_set.all()

class OwnBookSerializer(serializers.HyperlinkedModelSerializer):
    url_book = serializers.HyperlinkedIdentityField( view_name='browserapi:book-detail' )
    class Meta:
        model = Book
        fields = ['url_book', 'title', 'author', 'created_at']

class OwnAuthorSerializer(serializers.HyperlinkedModelSerializer):
    url_author = serializers.HyperlinkedIdentityField( view_name='browserapi:author-detail' )
    class Meta:
        model = Author
        fields = ['url_author', 'author_name', 'created_at']


class BookHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'browserapi:book-detail'
    queryset = Book.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            # 'title_slug': obj.title.slug,
            # 'organization_slug': obj.organization.slug,
            'book_id': obj.id
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            # 'organization__slug': view_kwargs['organization_slug'],
            'id': view_kwargs['book_id']
        }
        return self.get_queryset().get(**lookup_kwargs)
# class AutorOfBook(serializers.HyperlinkedModelSerializer):
#     pass HyperlinkedRelatedField

# class OwnAuthorField(serializers.RelatedField):
#     def to_representation(self, value):
#         url_author = serializers.HyperlinkedIdentityField( view_name='browserapi:author-detail' )
#         return 'Author: {}, link: {}'.format(value.author_name, url_author)

# class OwnBookField(serializers.RelatedField):
#     def to_representation(self, value):
#         url_book = serializers.HyperlinkedIdentityField( view_name='browserapi:book-detail' )
#         return 'Title: {}, author: {}, link: {}'.format(value.title, value.author, url_book)