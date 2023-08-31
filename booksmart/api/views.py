from rest_framework import viewsets
from booksmart.api.filters import IsOwnerFilterBackend, BookFilter
from rest_framework.response import Response
from booksmart.models import Book, Author 
from accounts.models import Account
from booksmart.api.serializers import BookToListSerializer, AuthorsSerializer, BooksSerializer, CustomBookSerializer, BookToEditSerializer
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view
import os, requests, json, re, datetime, requests.api
from rest_framework import filters as base_filters
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
from accounts.serializers import RegistrationSerializer, AccountUpdateSerializer, LoginSerializer, PasswordUpdateSerializerApi, AccountSerializer, UserDetailSerializer
from accounts.api.views import AccountViewSet, UserDetailViewSet, UserViewSet
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer
# from booksmart.api.views import BookViewSet, AuthorViewSet
# from django_filters.rest_framework.backends import DjangoFilterBackend
# from rest_framework.filters import DjangoFilterBackend

# class IsOwnerFilterBackend(base_filters.BaseFilterBackend):
#     """
#     Filter that only allows users to see their own objects.
#     """
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(owner=request.user)



class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [IsOwnerOrReadOnly,] 
    # permissions.IsAuthenticatedOrReadOnly, #
    #  permissions.IsAdminUser)
    filter_backends = [filters.DjangoFilterBackend, base_filters.OrderingFilter, base_filters.SearchFilter, FullWordSearchFilter, ]
    filterset_fields = {'author_name':['icontains', 'iexact'], 'date_of_birth':['gte', 'lte'], 'date_of_death':['gte', 'lte']}
    ordering_fields = ['last_name', 'created_at']
    search_fields = ['author_name', 'author_wiki_link_d']
    word_fields = ['author_name', 'author_wiki_link_d']

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     author = self.get_object()
    #     return Response(author.highlighted)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BooksUserViewSet(viewsets.ModelViewSet):
    # model = Book
    queryset = Book.objects.all() # .order_by('title')
    serializer_class = BookToEditSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    filterset_class =  BookFilter
    filter_backends = [filters.DjangoFilterBackend, base_filters.OrderingFilter, base_filters.SearchFilter, FullWordSearchFilter, IsOwnerFilterBackend]
    search_fields = ['title', 'author', 'summary',  'surname', 'category',] # owner__username
    ordering_fields = ['title', 'surname', 'published']
    word_fields = ['title', 'author', 'summary',  'surname', 'category',]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BooksFullViewSet(viewsets.ReadOnlyModelViewSet):
    model = Book
    queryset = Book.objects.all()
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    serializer_class = BooksSerializer
    # authentication_classes = [TokenAutentication, SessionAuthentication, BasicAuthentication]
    #permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser)
    filterset_class =  BookFilter
    filter_backends = [filters.DjangoFilterBackend, base_filters.OrderingFilter, base_filters.SearchFilter, FullWordSearchFilter,] # base_filters.SearchFilter
    
    # filterset_fields = [ 'title', 'author', 'published', ]
    # filterset_fields = {'title':['iexact', 'icontains'], 'author':['iexact'], 'category':['iexact'], 'published':[ ], 'author_c':[], }
    search_fields = ['title', 'author', 'summary',  'surname', 'category',] # owner__username
    ordering_fields = ['title', 'surname', 'published']
    word_fields = ['title', 'author', 'summary',  'surname', 'category',]

    # ordering_fields = ('author_name', 'date_of_birth', 'last_name')
    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     book = self.get_object()
    #     return Response(book.highlighted)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BookView(APIView):
    permission_classes = [IsOwnerOrReadOnly,]
    def get(self, request, **kwargs):
        book = Book.objects.get(id=kwargs['pk'])
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'books': reverse('book-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format)
    })

class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    queryset = Book.objects.all()
    serializer_class = CustomBookSerializer()

# class AuthorViewSet(viewsets.ModelViewSet):
#     queryset = Author.objects.all().order_by('last_name')
#     serializer_class = AuthorSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
#     filter_backends = [filters.DjangoFilterBackend, OrderingFilter, SearchFilter]
    
#     filterset_fields = {'author_name':['exact', 'in'], 'date_of_birth':['gte', 'lte', 'exact', ], 'last_name':['exact', 'in']}
#     #filterset_fields = {'title':['exact', 'in'], 'author':['exact'], 'category':['exact'], 'published':['gte', 'lte', 'exact', ] }
#     ordering_fields = ('author_name', 'date_of_birth', 'last_name')
#     # def user(self, request, id):
#     #     user = Account.objects.filter(pk = id)
#     #     user = user.request
#     #     return user

#     # def get_queryset(self):
#     #     # userbooks = Book.objects.filter(user_num_b=user.id)
#     #     # return userbooks
#     #     allauthors = Author.objects.all()
#     #     return allauthors
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

#     def create(self, request, *args, **kwargs):
#         user = request.user
#         if not user.is_authenticated:
#             return redirect('api')

#         serializer_author = self.get_serializer(data=request.data)
#         serializer_author.is_valid(raise_exception=True)
#         serializer_obj = serializer_author.save(commit=False)
#         created_by = Account.objects.filter(id=user.id).first()
#         serializer_obj.created_by = created_by
#         serializer = serializer_obj.save(commit=False)
#         # serializer = serializer_book.save(commit=False)
#         user_num_b = user.id
#         serializer.user_num_a = user.id
#         serializer.save()

#         try:
#             return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#         except (TypeError, KeyError):
#             return {}
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     # def retrieve(self, request, *args, **kwargs):
#     #     params = kwargs
#     #     print(params['pk'])
#     #     params_list = params['pk'].split('-')
#     #     cars = CarSpecs.objects.filter(
#     #         car_brand=params_list[0], car_model=params_list[1])
#     #     serializer = CarSpecsSerializer(cars, many=True)
#     #     return Response(serializer.data)

#     # def list(self, request, *args, **kwargs):
#     #     queryset = self.filter_queryset(self.get_queryset())

#     #     page = self.paginate_queryset(queryset)
#     #     if page is not None:
#     #         serializer = self.get_serializer(page, many=True)
#     #         return self.get_paginated_response(serializer.data)

#     #     serializer = self.get_serializer(queryset, many=True)
#     #     return Response(serializer.data)
    
#     #def retrieve(self, request, pk=None):
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     #def update(self, request, pk=None):
#     def update(self, request, *args, **kwargs):
#         user = request.user
#         if not user.is_authenticated :
#             return redirect('api')

#         elif user.is_authenticated:
#             partial = kwargs.pop('partial', False)
#             instance = self.get_object()
#             print('instance', instance)
#             serializer = self.get_serializer(instance, data=request.data, partial=partial)
#             print('serializer', serializer)
#             if user.id != instance.user_num_a:
                
#                 return Response({"message": "You are not owner this record, you can't change it"})

#             elif user.id == instance.user_num_a:
#                 serializer.is_valid(raise_exception=True)
#                 serializer.save()
#             return Response(serializer.data)
#         elif getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#     # def partial_update(self, request, pk=None):
#     def partial_update(self, request, *args, **kwargs):
#         user = request.user
#         if not user.is_authenticated :
#             pass

#         elif user.is_authenticated:
#             if user.id == user_num_a:
#                 kwargs['partial'] = True
#                 return self.update(request, *args, **kwargs)
#             else:
#                 pass

#     #def destroy(self, request, pk=None):
#     def destroy(self, request, *args, **kwargs):
#         user = request.user
#         if not user.is_authenticated :
#             return redirect('api')
#         elif user.is_authenticated:
#             instance = self.get_object()
#             if user == instance.created_by:
#                 instance.delete()
#             else:
#                 return Response({"message": "You are not owner this record, you can't delete it"})
#         return Response(status=status.HTTP_204_NO_CONTENT)



# # class BookFilter(FilterSet):
     
# #     title =  CharFilter(field_name='title', lookup_expr='icontains')
# #     author = CharFilter(field_name='author', lookup_expr='icontains')
# #     start_published = DateTimeFilter(field_name='published', label='start date published',
# #                                              lookup_expr='gte') # DateTimeFilter
# #     end_published = DateTimeFilter(field_name='published', label='end date published',
# #                                              lookup_expr='lte') 
# #     published = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))                                           

# #     class Meta:
# #         model = Book
# #         fields = ('title', 'author',  'category', 'start_published', 'end_published', 'published') 

# # class RangeWidget(SuffixedMultiWidget):
# #     min = 
# #     class Meta:
# #         model = Book
# #         suffixes = ['min', 'max']

# # class BookViewSet(viewsets.ModelViewSet):
# #     queryset = Book.objects.all().order_by('title')
# #     serializer_class = BookSerializer
# #     permission_classes = [permissions.IsAuthenticated]
# #     # filterset_class =  BookFilterPub
# #     name='book-list'
# #      # format_html('<input type="date" value={}', published)
     
# #     filter_backends = (filters.DjangoFilterBackend, OrderingFilter, FullWordSearchFilter) 
# #     filterset_class = BookFilter
# #     #filterset_fields = {'title':['exact', 'in'], 'author':['exact'], 'category':['exact'], 'published':['gte', 'lte', 'exact', ] } #FullWordSearchFilter,] #SearchFilter,
# #     ordering_fields = ('title', 'surname', 'published' )
# #     # filterset_class = BookFilter
# #     # filterset_fields = (
# #     #     '^title',)
# #     filterset_fields = ('title', 'author', 'category', 'published', 'user_recs_b')
    
# #     word_fields = ('title', 'author',)


# # from django_filters import rest_framework as filters

# # class IsOwnerBookFilterBackend(filters.BaseFilterBackend):
# #     """
# #     Filter that only allows users to see their own objects.
# #     """
# #     def filter_queryset(self, request, queryset, view):
# #         return queryset.filter(user_num_b=request.user.id)


class BooksEditViewSet(viewsets.ModelViewSet):
    # model = Book
    queryset = Book.objects.all() # .order_by('title')
    serializer_class = BookToEditSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    filterset_class =  BookFilter
    filter_backends = [filters.DjangoFilterBackend, base_filters.OrderingFilter, base_filters.SearchFilter, FullWordSearchFilter,]
    search_fields = ['title', 'author', 'summary',  'surname', 'category',] # owner__username
    ordering_fields = ['title', 'surname', 'published']
    word_fields = ['title', 'author', 'summary',  'surname', 'category',]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    # def list(self, request):
    #     queryset = Book.objects.all()
    #     serializer = BookToListSerializer(queryset, context={'request': request}, many=True)
            
    #     filter_backends = [filters.DjangoFilterBackend, base_filters.OrderingFilter, base_filters.SearchFilter, FullWordSearchFilter]
    #     search_fields = ['title', 'author', 'summary',  'surname', 'category',] # owner__username
    #     ordering_fields = ['title', 'surname', 'published']
    #     word_fields = ['title', 'author', 'category',]
    #     return Response(serializer.data)


        

    # def create(self, request, *args, **kwargs):
    #     user = request.user
    #     #book = Book(created_by=account)
    #     serializer_book = self.get_serializer(data=request.data)
    #     serializer_book.is_valid(raise_exception=True)
    #     serializer_obj = serializer_book.save(commit=False)
    #     created_by = Account.objects.filter(id=user.id).first()
    #     serializer_obj.created_by = created_by
    #     serializer = serializer_obj.save(commit=False)
    #     # serializer = serializer_book.save(commit=False)
    #     user_num_b = user.id
    #     serializer.user_num_b = user_num_b
    #     serializer.save()

    #     try:
    #         return {'Location': str(data[api_settings.URL_FIELD_NAME])}
    #     except (TypeError, KeyError):
    #         return {}
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     user = request.user

    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
        
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
    #     if user.id != instance.created_by.id:
            
    #         return Response({"message": "You are not owner this record, you can't change it"})

    #     elif user == instance.creared_by:
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         if getattr(instance, '_prefetched_objects_cache', None):
    #             instance._prefetched_objects_cache = {}

    #     return Response(serializer.data)

    # def partial_update(self, request, *args, **kwargs):
    #     user = request.user
    #     permission_classes = [permissions.IsAdminUser]
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)
        
    # def destroy(self, request, *args, **kwargs):
    #     user = request.user
    #     if not user.is_authenticated :
    #         return redirect('api')
    #     elif user.is_authenticated:
    #         instance = self.get_object()
    #         if user == instance.created_by:
    #             instance.delete()
    #         else:
    #             return Response({"message": "You are not owner this record, you can't delete it"})
    #     return Response(status=status.HTTP_204_NO_CONTENT)




