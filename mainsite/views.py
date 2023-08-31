from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from rest_framework.response import Response
from rest_framework.views import APIView
from booksmart.forms import ItemsSearchForm
from rest_framework.authentication import TokenAuthentication
from accounts.views_forms import *


from rest_framework import viewsets

from rest_framework.response import Response
from booksmart.models import context_bm, Book, Author, BackgroundPoster, BackgroundVideo
from accounts.models import Account
from booksmart.api.serializers import BooksSerializer, AuthorsSerializer
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
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_currentuser.middleware import (
    get_current_user, 
    get_current_authenticated_user,
    )

from django.utils.text import slugify



try:
    txt = "Cześć: .&перевод чего-либо"
    txt_slugify = txt.replace("-", "slugify")
    txt_to_search = slugify(txt_slugify).replace("-", " ").replace("slugify", "-")
    print("txt_to_search: ", txt_to_search)
except Exception as e:
    print("exception ", e)


# print(list(set(Book.objects.values_list('author', 'author'))))

cont = {}
user_recs =  [("", "")]

@api_view(['GET', 'POST'])
@permission_classes([])
# @authentication_classes([]) # TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
def index_home_not(request):
    """View function for home page of site."""
    r_user = request.user
    context = context_bm

    context['r_user'] = "Anonymuous"
    return Response(context, template_name='index_home_not.html', )

@api_view(['GET', 'POST'])
@permission_classes([])
# @authentication_classes([]) # TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
def index_home(request):
    """View function for home page of site."""
    r_user = request.user
    context = context_bm


    try:
        if r_user.is_authenticated:
            context['person_name'] = r_user.username
            print("context['person_name']", context['person_name'])
        elif not r_user.is_authenticated:
            context['person_name'] = "Anonymous"

    except:
        print('something went wrong;')


        
    # try:
    #     if BackgroundPoster.objects.last():
    #         poster = BackgroundPoster.objects.filter().last()
    #         print('poster', poster.link_poster_1)
    #         context['poster_url'] = poster.link_poster_1


    #     else:
    #         print('no poster')
    # except Exception as e:
    #     print(f'oster exception: {e}')

    # try:
    #     if BackgroundVideo.objects.filter().last():
    #         video = BackgroundVideo.objects.filter().last()
    #         print('video', video.link_video)
    #         context['video_url'] = video.link_video
    #     else:
    #         print('no video')
    # except Exception as e:
    #     print(f'video exception: {e}')        

    context['gb_books'] = r"https://books.google.com/"

    if r_user.is_authenticated:
        # cont['user_id'] = user.id
        context['r_user'] = r_user
        print('r_user.id', r_user.id)
        if Book.objects.filter(owner__id=r_user.id):
            global books_user
            books_user = Book.objects.filter(owner__id=r_user.id)
            context['books_user'] = books_user
            for book_user in books_user:
                user_recs.append((f'"{book_user.title}", "{book_user.author}"'))

            # user_books = Book.objects.filter(owner__id=user.id).values_list('title', 'author')    
            # print('user_books', list(user_books))
            return Response(context, template_name='index_home.html', )
        elif not Book.objects.filter(owner__id=r_user.id):
            messages.info(request, "You haven't any own books yet here")
    elif not r_user.is_authenticated:
        context['r_user'] = "Anonymuous"
        return Response(context, template_name='index_home.html', )
    else:
        context['r_user'] = "Anonymuous"
        return Response(context, template_name='index_home.html', )

    if get_current_user():
        print('views mainsite, get_current_user', get_current_user())
    else:
        print('views mainsite, no get_current_user')
    # context_a['CustomAuthToken']= CustomAuthToken
    return Response(context, template_name='index_home.html', )
    # return render(request, 'index.html', context)


try:
    books_no = Book.objects.filter(author_c__isnull=True)
    books_no_id = [book_no.id for book_no in books_no]
    for book_no in books_no:
        if Author.objects.filter(last_name=book_no.surname):
            author_class = Author.objects.filter(last_name=book_no.surname).last()    
            book_no.author_c = author_class
            book_no.save()
            # print('yes')
        elif not Author.objects.filter(last_name=book_no.surname):
            
            print('no author_c for', book_no.surname)
except Exception as e:
    print(f'bookmain exception: {e}')


@api_view(['GET', 'POST'])
@permission_classes([])
# @authentication_classes([]) # TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
def ajax_info_1(request):
    """View function for home page of site."""
    return Response(template_name='booksmartapp/ajax_info_1.txt', )
# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
# def index_home_ex(request):
# # def index_home(request, *args):
#     """View function for home page of site."""
#     user = request.user
#     cont_main['user-id'] = user.id
#     form = AccountUpdateForm()
#     context_a = context_bm
#     # context_a['account_view_form'] = account_view_form
#     context_a['account_form']= form

#     context_a['gb_books'] = r"https://books.google.com/"
#     return Response(context_a, template_name='index_home.html', )
