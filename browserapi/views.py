from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from rest_framework import viewsets

from booksmart.models import Book, Author 
from accounts.models import Account
from booksmart.api.serializers import BookSerializer, AuthorSerializer
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
from accounts.api.serializers import RegistrationSerializer, AccountUpdateSerializer, LoginSerializer, PasswordSerializer, AccountSerializer, UserDetailSerializer
from accounts.api.views import AccountViewSet, UserDetailViewSet, UserViewSet
from booksmart.api.views import BookViewSet, AuthorViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication



                        
class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format)
    })