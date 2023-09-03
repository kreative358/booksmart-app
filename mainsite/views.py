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
from booksmart.models import context_bm, Book, Author, BackgroundPoster, BackgroundVideo, url_img_author, url_img
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

# from django.utils.text import slugify
# try:
#     txt = "Cześć: .&перевод чего-либо"
#     txt_slugify = txt.replace("-", "slugify")
#     txt_to_search = slugify(txt_slugify).replace("-", " ").replace("slugify", "-")
#     print("txt_to_search: ", txt_to_search)
# except Exception as e:
#     print("exception ", e)

import datetime

context_bm = {}
context_list = []

context_bm['no_date'] = datetime.date(3000, 1, 1)
context_bm['url_img_book'] = url_img
context_bm['url_img_author'] = url_img_author

try:
    if Book.objects.all():
        Book.objects.update()
    # if Book.objects.filter().all():
        all_books = Book.objects.all()
        context_list.append(all_books)
        num_books = Book.objects.all().count()
        context_bm['allbooks'] = all_books
        context_bm['num_books'] = num_books
    elif not Book.objects.all():
    # elif not Book.objects.filter().all():
        context_bm['allbooks'] = None
        context_bm['num_books'] = 0
except:
    print("booksmart models 335 no Book.objects.all():")
    pass

try:
    if Author.objects.all():
        Author.objects.update()
    # if Author.objects.filter().all():
        all_authors = Author.objects.all()
        context_list.append(all_authors)
        num_authors = Author.objects.all().count()
        context_bm['allauthors'] = all_authors
        context_bm['num_authors'] = num_authors
    elif not Author.objects.all():
    #elif not Author.objects.filter().all():
        context_bm['allauthors'] = None
        context_bm['num_authors'] = 0
except:
    print("booksmart models 351 no Author.objects.all():")
    pass

try:
    if BackgroundPoster.objects.filter().last():
        poster = BackgroundPoster.objects.filter().last()
        context_bm['poster_url_1'] = poster.link_poster_1
        context_bm['poster_url_2'] = poster.link_poster_2
    elif not BackgroundPoster.objects.filter().last():
        context_bm['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
        context_bm['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
except:
    print("booksmart models 367 no BackgroundPoster.objects.filter().last():")
    pass

try:
    if BackgroundVideo.objects.filter().last():   
        video = BackgroundVideo.objects.filter().last()
        context_bm['video_url'] = video.link_video
        context_bm['video_type'] = video.type_video
    elif not BackgroundVideo.objects.filter().last():
        context_bm['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"

        context_bm['video_type'] = "mp4"
except:
    print("booksmart models 367 no BackgroundVideo.objects.filter().last():")
    pass


try:
    if BackgroundMusic.objects.filter().last():   
        music = BackgroundVideo.objects.filter().last()
        context_bm['music_url_1'] = music.link_music_1
        context_bm['music_type_1'] = music.type_music_1
        context_bm['music_url_2'] = music.link_music_2
        context_bm['music_type_2'] = music.type_music_2
    elif not BackgroundMusic.objects.filter().last(): 
        context_bm['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_bm['music_type_1'] = "mp3"
        context_bm['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_bm['music_type_2'] = "mp3"
except:
    context_bm['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
    context_bm['music_type_1'] = "mp3"
    context_bm['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
    context_bm['music_type_2'] = "mp3"


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

    all_books = Book.objects.all()
    num_books = Book.objects.all().count()
    context['allbooks'] = all_books
    context['num_books'] = num_books
    
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

# from django import template
# # from django.contrib.auth.decorators import login_required
# # from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
# from django.urls import reverse

# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
# def error_pages(request):
#     r_user = request.user
#     context = context_bm
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]
#         print('load_template:', load_template)
#         if load_template == 'admin':
#             # return HttpResponseRedirect(reverse('admin:index'))
#             return Response(context, template_name='admin.html', )
#         context['segment'] = load_template

#         html_template = loader.get_template('booksmartapp/' + load_template)
#         # return HttpResponse(html_template.render(context, request))
#         return Response(context, template_name=html_template, )

#     except template.TemplateDoesNotExist:

#         # html_template = loader.get_template('page-404.html')
#         # print('404 load_template:', load_template)
#         # return HttpResponse(html_template.render(context, request))
#         return Response(context, template_name='booksmartapp/page-404.html', )

#     except:
#         # html_template = loader.get_template('page-500.html')
#         # print('500 load_template:', load_template)
#         # return HttpResponse(html_template.render(context, request))
#         return Response(context, template_name='page-500.html', )

# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
def custom_page_not_found_view(request, exception):
    # return Response(context, template_name='page-500.html', )
    context = context_bm
    # return Response(context, template_name='page-404.html', )
    return render(request, "page-404.html", context)

# @api_view(['GET'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer,JSONRenderer])
def custom_error_view(request, exception=None):
    context = context_bm
    # return Response(context, template_name='page-500.html', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return render(request, "page-500.html", context)


# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
def custom_permission_denied_view(request, exception=None):
    context = context_bm
    # return Response(context, template_name='page-403.html', )
    return render(request, "page-403.html", context)

# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
def custom_bad_request_view(request, exception=None):
    context = context_bm
    # return Response(context, template_name='page-400.html', )
    return render(request, "page-400.html", context)