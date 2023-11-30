from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from rest_framework.response import Response
from rest_framework.views import APIView
from booksmart.forms import ItemsSearchForm
from rest_framework.authentication import TokenAuthentication
from accounts.views_forms import *
from django.contrib import messages
from rest_framework import viewsets

from rest_framework.response import Response
from booksmart.models import Book, Author, BackgroundPoster, BackgroundVideo, url_img_author, url_img # ,context_bm, 
from accounts.models import Account
from accounts.forms import RechaptchaMailForm
from booksmart.api.serializers import BooksSerializer, AuthorsSerializer
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view
import os, requests, json, re, datetime, requests.api
import urllib
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
from django.http import JsonResponse
# from django.utils.text import slugify
# try:
#     txt = "Cześć: .&перевод чего-либо"
#     txt_slugify = txt.replace("-", "slugify")
#     txt_to_search = slugify(txt_slugify).replace("-", " ").replace("slugify", "-")
#     print("txt_to_search: ", txt_to_search)
# except Exception as e:
#     print("exception ", e)


import datetime

context_list = []

context_main = {}

context_main['no_date'] = datetime.date(3000, 1, 1)
context_main['url_img_book'] = url_img
context_main['url_img_author'] = url_img_author

try:
    if Book.objects.all():
    # if Book.objects.filter().all():
        all_books = Book.objects.all()
        # context_list.append(all_books)
        num_books = Book.objects.all().count()
        context_main['allbooks'] = all_books
        context_main['num_books'] = num_books
    elif not Book.objects.all():
    # elif not Book.objects.filter().all():
        context_main['allbooks'] = None
        context_main['num_books'] = 0
except:
    print("booksmart models 335 no Book.objects.all():")
    pass

try:
    if Author.objects.all():
    # if Author.objects.filter().all():
        all_authors = Author.objects.all()
        # context_list.append(all_authors)
        num_authors = Author.objects.all().count()
        context_main['allauthors'] = all_authors
        context_main['num_authors'] = num_authors
    elif not Author.objects.all():
    #elif not Author.objects.filter().all():
        context_main['allauthors'] = None
        context_main['num_authors'] = 0
except:
    print("booksmart models 351 no Author.objects.all():")
    pass

try:
    if BackgroundPoster.objects.filter().last():
        poster = BackgroundPoster.objects.filter().last()
        context_main['poster_url_1'] = poster.link_poster_1
        context_main['poster_url_2'] = poster.link_poster_2
    elif not BackgroundPoster.objects.filter().last():
        context_main['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
        context_main['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
except:
    print("booksmart models 367 no BackgroundPoster.objects.filter().last():")
    pass

try:
    if BackgroundVideo.objects.filter().last():   
        video = BackgroundVideo.objects.filter().last()
        context_main['video_url'] = video.link_video
        context_main['video_type'] = video.type_video
    elif not BackgroundVideo.objects.filter().last():
        context_main['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
        context_main['video_type'] = "mp4"
except:
    print("booksmart models 367 no BackgroundVideo.objects.filter().last():")
    pass

try:
    if BackgroundMusic.objects.filter().last():   
        music = BackgroundVideo.objects.filter().last()
        context_main['music_url_1'] = music.link_music_1
        context_main['music_type_1'] = music.type_music_1
        context_main['music_url_2'] = music.link_music_2
        context_main['music_type_2'] = music.type_music_2
    elif not BackgroundMusic.objects.filter().last(): 
        context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_main['music_type_1'] = "mp3"
        context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_main['music_type_2'] = "mp3"
except:
    context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
    context_main['music_type_1'] = "mp3"
    context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
    context_main['music_type_2'] = "mp3"
# print(list(set(Book.objects.values_list('author', 'author'))))

cont = {}
user_recs =  [("", "")]


# books_in_db_no_author_c = [book for book in Book.objects.filter(author_c__isnull=True)]
# print(books_in_db_no_author_c)

# books_in_db_no_author_c = [book_in_db for book_in_db in books_in_db if 



@api_view(['GET', 'POST'])
@permission_classes([])
# @authentication_classes([]) # TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
def index_home_not(request):
    """View function for home page of site."""
    r_user = request.user
    current_url_name = request.path

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name

    if r_user.username == "":
        context['r_user'] = "Anonymuous"
    elif r_user.username != "":
        context['r_user'] = r_user
    return Response(context, template_name='index_home_not.html', )

recapitcha_value = ""

@api_view(['GET', 'POST'])
@permission_classes([])
# @authentication_classes([]) # TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
def index_home(request):
    """View function for home page of site."""
    context ={}
    r_user = request.user
    current_url_name = request.path
    print("1. current_url_name =", current_url_name)
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main
    # form_recaptcha_mail = RechaptchaMailForm()
    # context["form_recaptcha_mail"] = form_recaptcha_mail
    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name

    context["test_word"] = "test-word"

    # context['mail_sender'] = ""
    index_home.recaptcha_status = ""

    # if request.method == 'POST': 
    #     data_recaptcha = json.loads(request.body.decode("utf-8"))
    #     if data_recaptcha:
            
    #         print("data_rcecaptcha =", data_recaptcha)
    #     else:
    #         print("no data_recaptcha")

#   route("/verify_grecaptcha", methods=["POST"])

    if request.method == 'POST':
        print("request.method == 'POST'")
        # data_recaptcha = json.loads(request.data.decode("utf-8"))
        # data_recaptcha = json.loads(request.data)
        data_recaptcha = request.data
        # data_recaptcha = json.loads(request.body)
        recaptcha_text = data_recaptcha['response_mm']
        # print(recaptcha_text)
        url = 'https://www.google.com/recaptcha/api/siteverify'
        RECAPTCHA_SECRET_KEY = '6Le3IP4nAAAAAH5J3uPYy4BPPEsS55k0RwCaYxeY'
        params = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_text
        }
    
        verify_rs = requests.get(url, params=params, verify=True)
        # result = json.load(response)
        result = verify_rs.json()
        print('result =', result)
        # context['mail_sender'] = "ready"
        if result['success']:
            print('success')
            
            # messages.success(request, 'New comment added with success!')
            index_home.recaptcha_status = 'SUCCESS'
            return JsonResponse({'status': 'SUCCESS'})
        else:
            print('error')
            index_home.recaptcha_status = 'ERROR'
            # messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return JsonResponse({'status': 'ERROR'})

    # if request.method == 'POST':
    #     # form_recaptcha_mail = RechaptchaMailForm(request.POST)
    #     # recapitcha_token = request.POST.get('recapitcha_value', None)
       
    #     data_recaptcha = json.loads(request.body.decode("utf-8"))
    #     if data_recaptcha:
    #     # if form_recaptcha_mail.is_valid():
    #         # Do something with the form data
    #         # recaptcha_token = form_recaptcha_mail.cleaned_data["recaptcha_mail_token"]
    #         print("data_recapitcha['tag'][:20] =", data_recaptcha['tag'][:20])
    #         if len(data_recaptcha['tag']) > 200:
    #             index_home.recaptcha_token = data_recaptcha['tag']
    #         # return JsonResponse({'status': 'success'})
    #         else:
    #             index_home.recaptcha_token = ""

    #     else:
    #         print("status error")

    # recapitcha_value = request.GET.get('recapitcha_value', None)
    # if recapitcha_value:
    #     print('recapitcha_value =', recapitcha_value[:20])
    #     context['recapitcha_value'] = recapitcha_value
        
    # else:
    #     recapitcha_value = ""
    #     print('NO recapitcha_value')

    try:
        if r_user.is_authenticated:
            context['person_name'] = r_user.username
            print("context['person_name']", context['person_name'])
        elif not r_user.is_authenticated:
            context['person_name'] = "Anonymous"

    except:
        print('something went wrong;')

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
    
    # context['form_recaptcha_mail'] = RechaptchaMailForm()
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
#     context_a = context_mainsite
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
#     context = context_mainsite
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
    context = context_main
    # return Response(context, template_name='page-404.html', )
    return render(request, "page-404.html", context)

# @api_view(['GET'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer,JSONRenderer])
def custom_error_view(request, exception=None):
    context = context_main
    # return Response(context, template_name='page-500.html', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return render(request, "page-500.html", context)


# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
def custom_permission_denied_view(request, exception=None):
    context = context_main
    # return Response(context, template_name='page-403.html', )
    return render(request, "page-403.html", context)

# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
def custom_bad_request_view(request, exception=None):
    context = context_mains
    # return Response(context, template_name='page-400.html', )
    return render(request, "page-400.html", context)

def custom_unauthorized_view(request, exception=None):
    context = context_mains
    # return Response(context, template_name='page-400.html', )
    return render(request, "page-401.html", context)