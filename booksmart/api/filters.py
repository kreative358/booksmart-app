from django import forms
from django_filters.rest_framework import FilterSet
from django_filters import CharFilter, ChoiceFilter, NumberFilter, BooleanFilter, ModelChoiceFilter
from booksmart.models import Book, Author
from django_filters.widgets import RangeWidget, BooleanWidget
from django_filters import DateFromToRangeFilter, ModelMultipleChoiceFilter
from rest_framework import routers, serializers
from django_filters import rest_framework as filters
from rest_framework import filters
#from .views_api import CurrentUserDefault
import requests
from booksmart.api.hyperlink import FilterList
from django.contrib.auth import authenticate
# from bookmain.middleware import current_user
# from crum import get_current_user
# from django_currentuser.middleware import (
#     get_current_user, get_current_authenticated_user)

# print('get_current_user', get_current_user)

class IsOwnerFilterBackend(filters.BaseFilterBackend):
   
    def filter_queryset(self, request, queryset, view):
        global user
        user = request.user
        global owner_user
        owner_user = queryset.filter(owner=user)
        return owner_user

    # def user_querytset(self, request, queryset, view):
    #     return Book.objects.filter(owner=request.user)



def user_records_b(request):
    if request.user:
        user = request.user
        user_books = Book.objects.filter(user_num_b=user.id).values('user_num_b').first()
        print(str(*user_books))
        return user_books
    else:
        return None
user_records_b

def not_user_records_b(request):
    if request.user:
        user = request.user
        not_user_books= Book.objects.exclude(user_num_b = user.id)
        print()
        return not_user_books
    else:
        return None

# def departments(request):
#     if request is None:
#         return Department.objects.none()

#     company = request.user.company
#     return company.department_set.all()

# class EmployeeFilter(filters.FilterSet):
#     department = filters.ModelChoiceFilter(queryset=departments)


def queryset_books(request):
    if request is None:
        return Book.objects.none()

    user = request.user
    # return user.owner_set.all() #many to many
    user_owner = Book.objects.filter(user_num_b=user.id)
    return user_owner


user_b = queryset_books

def filter_books_user(requst, queryset, name, value):   
    books = Book.objects.all()
    for book in books:
        if book.owner != request.user:
            book = 'isnull'
            lookup = '__'.join([name, 'isnull'])
            return queryset.filter(**{lookup: True})
        else:
            pass

class BookFilter(FilterSet): 
    
    owner = IsOwnerFilterBackend
    
    
    books = CharFilter(field_name='owner', label='search by username', lookup_expr='icontains')
    title = CharFilter(lookup_expr='icontains', label="search by title")
    author = CharFilter(lookup_expr='icontains', label="search by author")
   # author_c = ChoiceFilter(label="choose author from list ")
    published = DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date', 'id':'bs_input'}), label= 'From start published to end published') 

    user_books = ModelChoiceFilter( queryset=queryset_books, label="your books", to_field_name='owner') # to_field_name

    author_c = ModelChoiceFilter(queryset = Author.objects.all(), label="choose author from list ")

    # OWNER_RECORDS = [
    # ('',''),
    # ('user record', get_current_user)]
    # owner_books = ChoiceFilter( choices=OWNER_RECORDS)

    owner_records = BooleanFilter(field_name='owner', method=filter_books_user, label='boolean owner')

    # def filter_owner(self, queryset):
    #     return queryset.filter(owner=get_current_user)

    current = ModelMultipleChoiceFilter(queryset=queryset_books,
        widget=forms.CheckboxSelectMultiple, label='current records')

    class Meta:
        model = Book
        fields = ['title', 'author', 'published', 'owner', 'user_books', 'books', 'owner_records', 'current', 'author_c'] #'owner_records','owner', 

# class FilterBook(django_filters.FilterSet):
#     min_date = django_filters.DateFilter(field_name = 'min_date', lookup_expr='gte')
#     max_date = django_filters.DateFilter(field_name = 'max_date', lookup_expr='lt')
#     title = django_filters.CharFilter(lookup_expr='icontains')
#     author = django_filters.CharFilter(lookup_expr='icontains')
#     author_c__author_name = django_filters.CharFilter(lookup_expr='icontains')

#     class Meta:
#         model = Book
#         fields = [
#             'title',
#             'author',
#             'author_c', 
#             'isbn',  
#             'category', 
#             'language', 
#             'epub', 
#             'embeddable',
#             'google_id',
#             'published',
             
#             ]