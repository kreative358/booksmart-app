from booksmart.models import Book, Author 
from rest_framework.reverse import reverse
from rest_framework import routers, serializers, viewsets


from django.utils.encoding import smart_text
from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)

# class OwnAuthorBook(serializers.HyperlinkedModelSerializer):
    # url_book = serializers.HyperlinkedRelatedField( view_name='browserapi:book-detail' )
    #     class Meta:
        # model = Author
        # fields = ['url_author', 'author_name', 'created_at']

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

class OwnAuthorField(serializers.RelatedField):
    def to_representation(self, value):
        url_author = serializers.HyperlinkedIdentityField( view_name='browserapi:author-detail' )
        return 'Author: {}, link: {}'.format(value.author_name, url_author)

class OwnBookField(serializers.RelatedField):
    def to_representation(self, value):
        url_book = serializers.HyperlinkedIdentityField( view_name='browserapi:book-detail' )
        return 'Title: {}, author: {}, link: {}'.format(value.title, value.author, url_book)



# many=True
class AuthorHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'browserapi:author-detail'
    queryset = Author.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            # 'author_name': obj.author_name.replace(' ', '_'),
            'author_pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           # 'author__slug': view_kwargs['author_slug'],
           'id': view_kwargs['author_id']
        }
        return self.get_queryset().get(**lookup_kwargs)

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