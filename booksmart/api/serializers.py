from rest_framework import routers, serializers, viewsets
from booksmart.models import Book, Author
from accounts.models import Account
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets

from rest_framework.response import Response
from booksmart.models import Book, Author 
from accounts.models import Account

from rest_framework.settings import api_settings
from rest_framework.decorators import api_view
import os, requests, json, re, datetime, requests.api
from rest_framework import filters 
from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_word_filter import FullWordSearchFilter
from django_filters import rest_framework as filters
# import rest_framework_filters as filters
import django_filters
from django_filters import DateFromToRangeFilter
# from django_filters.rest_framework import FilterSet
from rest_framework import permissions, renderers
# from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny, IsAdminUser
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.forms.widgets import NumberInput
from django_filters import rest_framework as filters
from django_filters.widgets import SuffixedMultiWidget
from django_filters.rest_framework import FilterSet, AllValuesFilter, DateTimeFilter, NumberFilter, DateFilter, CharFilter, IsoDateTimeFilter
from django.forms.widgets import NumberInput
from django import forms
from django.forms import ModelForm, Form
from django.utils.html import format_html
import django_filters
from django_filters.widgets import RangeWidget
from django_filters import DateFromToRangeFilter
from booksmart.api.filters import BookFilter
from booksmart.api.permissions import IsOwnerOrReadOnly
from pygments import highlight
from rest_framework import permissions, renderers, viewsets, mixins, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.api.serializers import RegistrationSerializerApi, AccountUpdateSerializerApi, LoginSerializerApi, PasswordSerializerApi, AccountSerializer, UserDetailSerializer
from accounts.api.hyperlink import AuthorHyperlink, BookHyperlink

from accounts.api.hyperlink import OwnAuthorSerializer, OwnBookSerializer, BookHyperlink
#from django_currentuser.middleware import (
#     get_current_user, get_current_authenticated_user)

class AuthorBookSerializer(serializers.ModelSerializer):
    # url_author = serializers.URLField(read_only=True, source='get_absolute_url')
    
    class Meta:
        model = Author
        fields = ['id', 'author_name', 'date_of_birth', 'date_of_death', ] # 'url_author', 'author_wiki_link', 'author_wiki_link_d', 'first_name', 'middle_name', 'last_name'

class BookToListSerializer(serializers.HyperlinkedModelSerializer):
    
    # url_owner = serializers.HyperlinkedRelatedField(view_name='browserapi:account-detail', source='owner')
    # author_c = serializers.HyperlinkedIdentityField(view_name='browserapi:author-detail', )
    surname = serializers.CharField(read_only=True,
    style={'base_template':'textarea.html', 'rows':4})
    url_book = serializers.HyperlinkedIdentityField(
    view_name='browserapi:book-detail', read_only=True)
    # url_book = BookHyperlink()
    class Meta:
        model = Book
        # list_serializer_class = CustomListBookSerializer
        # fields = fields = ['id', 'author_c', 'title', 'author',  'summary',  'surname', 'published', 'category', 'language', 'epub', 'isbn',  'embeddable', 'imageLinks','preview_link', 'preview_link_new', 'selfLink','owner', 'user_num_b',]
        fields = ['id', 'title', 'url_book', 'author', 'author_c', 'published', 'category', 'language', 'epub', 'owner', 'surname']

class BookToEditSerializer(serializers.ModelSerializer):
    url_book = serializers.HyperlinkedIdentityField(
    view_name='browserapi:book-detail', read_only=True)
    summary = serializers.CharField(write_only=True)
    class Meta:
        model = Book
        
        fields = ['id', 'title', 'url_book', 'author',  'summary', 'published', 'category', 'language', 'epub', 'isbn',  'embeddable', 'imageLinks', 'surname' ]
        # list_serializer_class = BookToListSerializer



class BookBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book # 'book_author'
        fields = ['id', 'title', 'url', 'url_book', 'author', 'author_c', 'summary', 'published', 'category', 'language', 'epub', 'isbn',  'embeddable', 'author_seializer',] # 'imageLinks','preview_link', 'preview_link_new', 'selfLink','owner', 'user_num_b', 'author_seializer', ]

class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'author_c.author_name', 'author_c__author_wiki_link', 'date_of_birth', 'date_of_death']
# class BookListSerializer(serializers.ModelSerializer):




# class HyperlinkedRelatedField(view_name=None, *, read_only=False, write_only=False, required=None, default=empty, initial=empty, source=None, label=None, help_text=None, style=None, error_messages=None, validators=None, allow_null=False)

class BooksSerializer(serializers.HyperlinkedModelSerializer):
    # url_author = serializers.HyperlinkedIdentityField( view_name='browserapi:author-detail', source='autho_c', read_only=True )
    info_author = AuthorBookSerializer(source='author_c')
    # info_author = AuthorBookSerializer(many=True, source='book_author' )
    #books_author__date_of_birth = serializers.StringRelatedField()
    #books_author__date_of_death = serializers.StringRelatedField(many=True)
    
    # def author_url(*args, **kwargs):
    #     if Author.objects.filter(author_name=book_serializer['author']):
    #         author_book = Author.objects.filter(author_name=book_serializer['author'])
    #         ids = author_book.id
    #         author_url = serializers.HyperlinkedIdentityField( view_name='browserapi:author-detail', lookup_url_kwarg='pk')
    #         return ids
    author_url = serializers.HyperlinkedRelatedField(read_only=True, view_name='browserapi:author-detail', source='author_c')
    url_book = serializers.HyperlinkedIdentityField(
    view_name='browserapi:book-detail')
    owner_url = serializers.HyperlinkedIdentityField(view_name='browserapi:account-detail', source='owner', read_only=True) # source='owner', HyperlinkedRelatedField
    owner_name=serializers.CharField(source="owner.username")
    # url_author = serializers.HyperlinkedIdentityField(
    # view_name='browserapi:author-detail', source='author_c', lookup_field="books_author.id")
    # author_c = serializers.HyperlinkedIdentityField(
    # view_name='browserapi:author-detail')
    # url_read = serializers.URLField(default=f'booksmartapp/booksmart-app/read_book/{source="book.id"}', read_only=True)

    class Meta:
        model = Book # 'book_author'

        fields = ['id', 'title', 'url_book', 'summary', 'author', 'info_author', 'author_url', 'author_c', 'published', 'category', 'language', 'epub', 'isbn', 'embeddable', 'owner_name', 'owner_url'] # 'imageLinks','preview_link', 'url_read' 'author_c__date_of_birth', 'books_author__date_of_death', 

class CustomBookSerializer(serializers.HyperlinkedModelSerializer):
    url_book = serializers.HyperlinkedIdentityField(
    view_name='browserapi:book-detail')
    owner_name = serializers.CharField(source="owner.username")
    class Meta:
        model = Book
        # list_serializer_class = CustomListBookSerializer
        # fields = fields = ['id', 'author_c', 'title', 'author',  'summary',  'surname', 'published', 'category', 'language', 'epub', 'isbn',  'embeddable', 'imageLinks','preview_link', 'preview_link_new', 'selfLink','owner', 'user_num_b',]
        fields = ['title',  'published', 'category', 'language', 'epub', 'url_book', 'owner_name', 'owner', ]




class AuthorsSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    

    # book_author =  serializers.HyperlinkedRelatedField(many=True, view_name = 'browserapi:book-detail', read_only=True)

    url_author = serializers.HyperlinkedIdentityField( view_name='browserapi:author-detail' )
    url_owner = serializers.HyperlinkedIdentityField(view_name='browserapi:account-detail', source='owner', read_only=True) # HyperlinkedRelatedField
    author_wiki_link_d = serializers.CharField(label="author short info", max_length=1000,
    )
    author_wiki_link = serializers.CharField(label="author's life", max_length=1000,
    style={'base_template': 'textarea.html', 'rows':4})

    books = CustomBookSerializer(source='books_author', many=True)
    class Meta:
        model = Author
        fields = ['id', 'author_name', 'author_wiki_link_d', 'author_wiki_link', 'url_author', 'date_of_birth', 'date_of_death',  'owner', 'url_owner', 'books'] # 'book_author' 'book_author_detail' , 'highlight' 





# class AuthorSerializer(serializers.HyperlinkedModelSerializer):
#     # owner = serializers.ReadOnlyField(source='owner.username')
#     user_num_a = serializers.HiddenField(default=1)
#     date_of_birth = serializers.DateField(label="Date of birth", style={'input_type': 'date'})
#     date_of_death = serializers.DateField(label="Date of death", style={'input_type': 'date'})
#     class Meta:
#         model = Author
#         fields = ['url', 'author_name', 'author_wiki_link', 'author_wiki_link_d', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'date_of_death', 'user_num_a']
        
        

# class BookSerializer(serializers.HyperlinkedModelSerializer):
#     # owner = serializers.ReadOnlyField(source='owner.username')
#     # custom_user = serializers.CurrentUserDefault()
#     # user_num_b = HiddenFields(default=serializers.CurrentUserDefault())
    
#     user_num_b = serializers.HiddenField(default=1)
#     published = serializers.DateField(label="Date of published book", style={'input_type': 'date'}) # input_formats="date"
#     # published = serializers.DateField(format=api_settings.DATE_FORMAT, input_formats=None)
#     class Meta:
#         model = Book
#         fields = ['url', 'title', 'author', 'surname', 'published', 'category', 'user_num_b', 'user_recs_b']
#         # read_only_fields = ['user_num_b']




# class AuthorSerializer(serializers.HyperlinkedModelSerializer):
#     #created_by = serializers.ReadOnlyField(source='created_by')
#     #print('created author', created_by.instance)
#     book_author =  serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name = 'Book-detail', lookup_url_kwarg ='title')
#     owner = serializers.ReadOnlyField(source='owner.id')
#     current_user = serializers.ListField(default=serializers.CurrentUserDefault())
#     current_user_in = serializers.ListField(initial=serializers.CurrentUserDefault())
#     # owner = serializers.HiddenField(default=CurrentUserDefault())
#     # owner_id = owner.instance
#     # print('owner_id author', owner_id)
#     # owner = serializers.CharField(source='owner.username', read_only=True)
#     # user_num_a = serializers.HiddenField(default=1)
#     date_of_birth = serializers.DateField(label="Date of birth", style={'input_type': 'date'})
#     date_of_death = serializers.DateField(label="Date of death", style={'input_type': 'date'})
#     class Meta:
#         model = Author
#         fields = ['url', 'author_name', 'author_wiki_link', 'author_wiki_link_d', 'created_by','first_name', 'middle_name', 'last_name', 'date_of_birth', 'date_of_death', 'owner', 'current_user', 'current_user_in']

#     # https://www.django-rest-framework.org/api-guide/fields/# serializermethodfield  
#     # serializer = RangeSerializer(data={'ranges': {'lower': datetime.date(2015, 1, 1), 'upper': datetime.date(2015, 2, 1)}})   

# class BookSerializer(serializers.HyperlinkedModelSerializer):   
#     #print('created author', created_by.instance)
#     owner = serializers.ReadOnlyField(source='owner.id')
#     current_user = serializers.ListField(default=serializers.CurrentUserDefault())
#     current_user_in = serializers.ListField(initial=serializers.CurrentUserDefault())
#     published = serializers.DateField(label="Date of published book", style={'input_type': 'date'}) # input_formats="date"
#     # published = serializers.DateField(format=api_settings.DATE_FORMAT, input_formats=None)
#     days_since_created_at = serializers.SerializerMethodField()
#     username = serializers.SerializerMethodField('get_username_from_created_by')
#     # ranges = DateRangeField()
#     # url = serializers.CharField(source='get_absolute_url', read_only=True)
#     class Meta:
#         model = Book
#         fields = ['url', 'title', 'author', 'surname', 'published', 'category', 'owner', 'created_by', 'current_user', 'current_user_in']
#         # read_only_fields = ['user_num_b']
#         def get_days_since_joined(self, book):
#             return (now() - obj.created_at).days

#         def get_username_from_created_by(self, book):
#             username = book.created_by.username

#         def get_current_user(self, request):
#             user = request.user
#             return user.name

