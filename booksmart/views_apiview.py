# # from .views_acc import *
from accounts.models import Account, MyAccountManager
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from booksmart.models import url_img, url_img_author, Book, Author, BackgroundPoster, BackgroundVideo #, context_bm  
from booksmart.forms import *

from django.db.models import Avg, Max, Min
import os, requests, json, re, datetime, requests.api

from django.db.models import Q, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.contrib.sites.shortcuts import get_current_site
from django.urls import resolve

from rest_framework.authtoken.views import ObtainAuthToken
# from .views import CustomAuthToken
import requests, datetime
# from datetime import datetime
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer, HTMLFormRenderer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from booksmart.api.permissions import IsOwner, IsOwnerOrReadOnly
from accounts.views_authorization import *

from rest_framework import filters as base_filters

import datetime

# context_list = []
context_main = {}

context_main['no_date'] = datetime.date(3000, 1, 1)
context_main['url_img_book'] = url_img
context_main['url_img_author'] = url_img_author
context_main['parameters'] = ""
context_main['message'] = ""
context_main['values'] = ""
context_main['modal_uni'] = "{% include 'snippets-booksmart/modal_message_booksmart_uni.html' %}"

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
    # print("booksmart models 335 no Book.objects.all():")
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
    # print("booksmart models 351 no Author.objects.all():")
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
    # print("booksmart models 367 no BackgroundVideo.objects.filter().last():")
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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def all_records(request):

    r_user = request.user
    current_url_name = request.path

    last_id = list(Book.objects.values_list('id').order_by('-id')[0])[0]
    book_add_last = Book.objects.all().order_by('-id') 

    # all_books = Book.objects.all().order_by("title")
    all_books = Book.objects.all()
    all_authors = Author.objects.all()
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main
    context["last_id"] = last_id
    context["book_add_last"] = book_add_last
    context['allbooks'] = all_books
    context['allauthors'] = all_authors
    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name

    context = context_main

    search_form = SearchRecord()
    form_search = ItemsSearchForm() 
    author = BooksAuthor()
    book_sort = BookSort(request.GET)
    # book_sort = BookSort()

    context['search_form'] = search_form
    context['form_search'] = form_search
    context['search_author'] = author
    context['book_sort'] = book_sort

    sort_kind = ['title']
    if book_sort.is_valid():
        field_sorting = book_sort.cleaned_data['sorting']

        if field_sorting != '':
            sort_kind.append(field_sorting)

        elif field_sorting == '':
            print("167 views_apiview")
    
    all_books = Book.objects.all().order_by(sort_kind[-1])
    context['allbooks'] = all_books

    context['current_url'] = current_url_name

    filtered_books = all_books

    paginated_filtered_books = Paginator(filtered_books, 10) 
    page_number = request.GET.get('page')
    book_page_obj = paginated_filtered_books.get_page(page_number)
    context['book_page_obj'] = book_page_obj
    return Response(context, template_name='allrecords.html', )
    # return render(request, 'allrecords.html', context)

@api_view(['GET', 'POST'])
# @permission_classes([])  
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def all_authors(request):

    r_user = request.user
    current_url_name = request.path
    if Author.objects.all().count() > 0:
        last_id = list(Author.objects.values_list('id').order_by('-id')[0])[0]
        author_add_last = Author.objects.all().order_by('-id')
    else:
        last_id = []
        author_add_last = []
    # author_add_last = get_object_or_404(Author, pk=last_id) 
    # print('author_add_last:', author_add_last)
    # all_authors = Author.objects.all().order_by('-created_at')
    all_authors = Author.objects.all().order_by('last_name')
    # print('all_authors:', all_authors)
    num_authors = Author.objects.all().count()
    all_books = Book.objects.all()
    num_books = Book.objects.all().count()

    context = context_main
    context["last_id"] = last_id
    context["author_add_last"] = author_add_last
    context['allbooks'] = all_books
    context['num_books'] = num_books
    context['allauthors'] = all_authors
    context['num_authors'] = num_authors
    context['current_url'] = current_url_name
    
    search_form = SearchRecord()
    form_search = ItemsSearchForm()
    author = BooksAuthor()
    book_sort = BookSort(request.GET)
    context['book_sort'] = book_sort
    context['search_form'] = search_form
    context['search_author'] = author
    context['form_search'] = form_search
  
    # paginator = Paginator(all_authors, 10) 
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    
    # context['page_obj'] = page_obj

    paginator_extras_authors = Paginator(all_authors, 10)
    page_number_authors = request.GET.get('page')
    author_page_obj = paginator_extras_authors.get_page(page_number_authors)
    context['author_page_obj'] =  author_page_obj

    return Response(context, template_name='all_authors.html', )
    # return render(request, 'all_authors.html', context)



@api_view(['GET', 'POST' ])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def account_records(request):
    r_user = request.user
    current_url_name = request.path

    all_books = Book.objects.all()
    all_authors = Author.objects.all()

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context_a = context_main

    context_a['allbooks'] = all_books
    context_a['allauthors'] = all_authors

    context_a['num_authors'] = num_authors
    context_a['num_books'] = num_books
    context_a['current_url'] = current_url_name

    search_form = SearchRecord()
    author = BooksAuthor()
    form_search = ItemsSearchForm()
    book_sort = BookSort(request.GET)
    context_a['book_sort'] = book_sort
    context_a['search_form'] = search_form
    context_a['form_search'] = form_search
    context_a['search_author'] = author
    # authors_add = Author.objects.filter(user_add=request.user)
    # books_add = Book.objects.filter(user_add=request.user)
    authors_add = Author.objects.filter(user_num_a=r_user.id)
    global books_add
    books_add = Book.objects.filter(user_num_b=r_user.id)
    context_a['authors_add'] = authors_add
    context_a['books_add'] = books_add

    paginator = Paginator(books_add, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context_a['page_obj'] = page_obj
    return Response(context_a, template_name='account-records.html', )
    # return render(request, 'account.html', context_a)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def authors_last(request):
    r_user = request.user
    current_url_name = request.path
    
    author = BooksAuthor()
 
    all_authors = Author.objects.all().order_by('last_name')
    search_form = SearchRecord()
    author = BooksAuthor()

    # current_url_name = request.resolver_match.url_name
    # currents.append(current_url_name)
    context = context_main

    context['allbooks'] = all_books
    context['allauthors'] = all_authors

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name

    context['search_form'] = search_form
    context['search_author'] = author
    context['form_search'] = form_search

    paginator = Paginator(all_authors, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return Response(context, template_name='authors_last.html', )
    #return render(request, 'authors.html', context)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def all_records_author(request, *arg, **kwargs):
    r_user = request.user
    current_url_name = request.path

    all_books = Book.objects.all().order_by('surname') #.values() 'surname',
    all_authors = Author.objects.all()

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['allbooks'] = all_books
    context['allauthors'] = all_authors

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name

    search_form = SearchRecord()
    form_search = ItemsSearchForm() 
    author = BooksAuthor()
    book_sort = BookSort(request.GET)
    context['book_sort'] = book_sort
    # current_url_name = request.resolver_match.url_name
    # currents.append(current_url_name)

    context['search_form'] = search_form
    context['form_search'] = form_search
    context['search_author'] = author

    paginator = Paginator(all_books, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return Response(context, template_name='allrecords_author.html', )
    #return render(request, 'allrecords_author.html', context)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def all_records_title(request):
    r_user = request.user
    current_url_name = request.path

    all_books = Book.objects.all().order_by('title')
    all_authors = Author.objects.all()

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['allbooks'] = all_books
    context['allauthors'] = all_authors

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name  

    search_form = SearchRecord()
    form_search = ItemsSearchForm() 
    author = BooksAuthor()
    current_url_name = request.path
    # current_url_name = request.resolver_match.url_name
    # currents.append(current_url_name)
    book_sort = BookSort(request.GET)
    context_a['book_sort'] = book_sort
    context_a['search_form'] = search_form
    context_a['form_search'] = form_search
    context_a['search_author'] = author

    paginator = Paginator(all_books, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context_a['page_obj'] = page_obj
    return Response(context_a, template_name='allrecords_title.html', )
    # return render(request, 'allrecords_title.html', context_a)

# @api_view(['GET', 'POST'])
# @permission_classes([])  #IsAuthenticated
# @authentication_classes([]) # authentication.TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
# def all_records_sort(request):
#     d = datetime.date(2018, 1, 3)
#     a = 'dumas'
#     o = 'title'
#     fd = 'published'
#     all_books = Book.objects.filter(published__gte=d, author__icontains=a).order_by(fd, o)
#     # all_books().order_by(o)
#     print('all_books', all_books)
#     all_authors = Author.objects.all()
#     num_books = Book.objects.all().count()
#     num_authors = Author.objects.all().count()
#     search_form = SearchRecord()
#     form_search = ItemsSearchForm() 
#     author = BooksAuthor()
#     context_a = {}

#     current_url_name = request.path
#     # current_url_name = request.resolver_match.url_name
#     # currents.append(current_url_name)
#     print('current_url_name', current_url_name)
#     context_a['current_url'] = current_url_name
#     context_a['allbooks'] = all_books
#     context_a['allauthors'] = all_authors
#     context_a['num_books'] = num_books
#     context_a['num_authors'] = num_authors
#     context_a['search_form'] = search_form
#     context_a['form_search'] = form_search
#     context_a['search_author'] = author

#     paginator = Paginator(all_books, 10)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)
#     context_a['page_obj'] = page_obj
#     return Response(context_a, template_name='allrecords_sort.html', )


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def books_author(request):

    r_user = request.user
    current_url_name = request.path

    all_books = Book.objects.all()
    all_authors = Author.objects.all()

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['allbooks'] = all_books
    context['allauthors'] = all_authors

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name

    author_form = BooksAuthor(request.GET)
    values_list = []
    search_form = SearchRecord()
    form_search = ItemsSearchForm() 
    author = BooksAuthor()
    book_sort = BookSort(request.GET)
    context['search_form'] = search_form
    context['form_search'] = form_search
    context['book_sort'] = book_sort
    context['search_author'] = author
    vaules_list = []
    if author_form.is_valid():
        # values=author_form.cleaned_data['author']
        
        value=author_form.cleaned_data['author_found_books']
        vaules_list.append(value)
        print("value =", value)
    
        books_result = Book.objects.filter(author=value)
        author_result = Author.objects.filter(author_name=value)
        num_books_result = books_result.count()
        num_authors_result_set = author_result.count()
        # num_books_result = Book.objects.filter(author=search_author).count()
        # num_authors_result_set = Author.objects.filter(author_name=values).count()
       
        context["parameters"] = value
        context['books_result'] = books_result
        context['author_result'] = author_result
        context['num_books_result']= num_books_result
        context['num_books_result_set']= num_books_result  #
        context['num_authors_result_set'] = num_authors_result_set
        context['values'] = value


        # current_url_name = request.resolver_match.url_name
        # currents.append(current_url_name)
        current_url_name = request.path
        print('current_url_name', current_url_name)
        context['current_url'] = current_url_name

        filtered_books = books_result
        paginated_filtered_books = Paginator(filtered_books, 10)  
        # filtered_books.qs
        page_number = request.GET.get('page')
        book_page_obj = paginated_filtered_books.get_page(page_number)

        context['book_page_obj'] = book_page_obj
    return Response(context, template_name='books_author.html', )
    # return render(request, 'books_author.html',context)


@api_view(['GET', 'POST'])
# @permission_classes([])  
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer])
def records_view_get(request):
    r_user = request.user
    current_url_name = request.path
    
    all_books = Book.objects.all()
    all_authors = Author.objects.all()
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context_get = context_main

    context_get['allbooks'] = all_books
    context_get['allauthors'] = all_authors

    context_get['num_authors'] = num_authors
    context_get['num_books'] = num_books
    context_get['current_url'] = current_url_name        
    
    context_get['user_id'] = r_user.id 
    author = BooksAuthor()
    form_search = ItemsSearchForm()
    book_sort = BookSort(request.GET)
    search_form = SearchRecord(request.GET)

    context_get['search_author'] = author
    context_get['search_form'] = search_form
    context_get['form_search'] = form_search
    context_get['book_sort'] = book_sort

    min_date = Book.objects.aggregate(Min('published'))

    max_date = Book.objects.aggregate(Max('published'))

    context = {}
    context_post = {}
    sort_parameter = ['title']

    context["form_search_post"] = "no"
    context_get["form_search_get_book"] = "no"
    context_get["form_search_get_author"] = "no"
    parameters = ""
    values = ""
    dict_values = ""


    keywords_fields = {}
    
    filter_dict = {}
    # context_get["filtered_books"] = []
    context["search_resultB"] = []
    context['author_objects'] = []
    context["search_resultA"] = []
    extra_keywords_fields_search_user_num_b = []
    if search_form.is_valid():
        context_get["form_search_get_book"] = "yes"  ###
          
        keywords_fields["user_num_b"] = r_user.id if str(search_form.cleaned_data["user_num_b"]) == "True" else ""

        keywords_fields["epub"] = "yes" if str(search_form.cleaned_data["epub"]) == "True" else ""

        keywords_fields['title__icontains'] = search_form.cleaned_data['title']
        
        # search_author = search_form.cleaned_data['author']
        keywords_fields['author__icontains'] = search_form.cleaned_data['author']

        # search_language = search_form.cleaned_data["language"]
        keywords_fields['language'] = search_form.cleaned_data["language"]

        # search_google_id = search_form.cleaned_data["google_id"]
        keywords_fields['google_id'] = search_form.cleaned_data["google_id"]

        # search_published__gte = search_form.cleaned_data["published__gte"]
        keywords_fields['published__gte'] = search_form.cleaned_data["published__gte"]

        # search_published__lt = search_form.cleaned_data["published__lt"]
        keywords_fields['published__lt'] = search_form.cleaned_data["published__lt"]

        # search_owner = search_form.cleaned_data["owner__username"]
        keywords_fields["owner__username__icontains"] = search_form.cleaned_data["owner__username"]

        # search_author_list = search_form.cleaned_data["author_list"] ###
        keywords_fields["author"] = search_form.cleaned_data["author_list"]

        # search_ordering = search_form.cleaned_data["ordering"]
        context_get["search_ordering"] = search_form.cleaned_data["ordering"] if search_form.cleaned_data["ordering"] != "" else "title"

        context_get["author_details_q"] = str(search_form.cleaned_data["author_details_q"])

    if context_get["author_details_q"] == "False":
        context_get["form_search_get_author"] = "no"
    elif context_get["author_details_q"] == "True":
        context_get["form_search_get_author"] = "yes"

    # if len(kewords_fields.values) != 0:
    for val in keywords_fields.values():
        if not val != '' and not val != None:
            msgs = ["It is necessary to pass any params to search"]
            contex_get["no_params"] = "no params"
            messages.info(request, "".join(msg for msg in msgs))
            return Response(context_get, template_name='allrecords.html', )

    
    if keywords_fields['published__gte'] != None and keywords_fields['published__gte'] != '':
        # keywords_fields['published__gte'] = search_published__gte.strftime('%Y-%m-%d')  
        keywords_fields['published__gte'] = keywords_fields['published__gte'].strftime('%Y-%m-%d')
    else:
        keywords_fields['published__gte'] = None

    if keywords_fields['published__lt']:
        # d = search_published__lt
        # keywords_fields['published__lt'] = d.strftime('%Y-%m-%d')  
        keywords_fields['published__lt'] = keywords_fields['published__lt'].strftime('%Y-%m-%d')
    else:
        keywords_fields['published__lt'] = None

    keywords_fields_items = list(keywords_fields.items())
    # query = '&'.join([f"{k}={v.replace(' ','+')}" if v == type(str) else f'{k}=' for k, v in keywords_fields.items()])
    # print("query", query)

    parameters_list = []
    
    # print('keywords_fields_items =', keywords_fields_items)
    for key, value in keywords_fields_items:
        if value != '' and value != None and not isinstance(value, int):
            # parameters_list.append((key, value))
            parameters_list.append((str(key).replace("__gte", "-start").replace("__lt", "-end").replace("__icontains", "").replace("__contains", ""), value))
            filter_dict[key] = value
        elif isinstance(value, int):
            filter_dict[key] = f"{value}"

    # print("parameters_list=", parameters_list)
    if len(parameters_list) == 0:
        context_get['parameters'] = ""
        context_get['parameters_get'] = ""

    # if len(keywords_fields.values()) == 2:
    elif len(parameters_list) == 1:
        # print(f'1 parameters_list 557: {parameters_list}')
        # parameters = f"{parameters_list[0][0]: {parameters_list[0][1]}}"
        parameters = f"{parameters_list[0][0]}: {parameters_list[0][1]}"
        context_get['parameters'] = parameters
        context_get['parameters_get'] = parameters
        
    elif len(parameters_list) > 1:
        # print(f'2 parameters_list line 559: {parameters_list}')
        parameters = ',<br>'.join([': '.join([str(e)[:e.index('_')] if not isinstance(e, int) and '_' in e else e if not isinstance(e, int) else str(e) for e in el]) for el in parameters_list])
        context_get['parameters'] = parameters
        context_get['parameters_get'] = parameters
        
    key = ''.join(filter_dict.keys())
    val = ''.join(filter_dict.values())

    
    books_result_queryset_distinct = []
    books_result_queryset = []
    books_result_title = [] # list with books title
    books_title = []
    books_result_queryset_list_sort = [] # queryset list with books

    if not filter_dict:
        all_books_sort = Book.objects.all().order_by(context_get["search_ordering"])
        # books_result_queryset.extend(list(all_books_sort))
        books_result_queryset_list_sort.extend(all_books_sort)
        msgs = ["You should enter some parameters for the search to work",]
        context_get['no_params'] = "no params"
        messages.info(request, "".join(msg for msg in msgs))
        # return Response(context_get, template_name='allrecords.html', )
        return redirect('/')
        # return redirect(current_url_name)
        

    elif filter_dict:

        try:
            queryset_books_distinct_sort = Book.objects.filter(**filter_dict).distinct().order_by(context_get["search_ordering"])
            queryset_books_distinct_sort_list = [book for book in queryset_books_distinct_sort]
            # print("queryset_books_distinct_sort_list =", queryset_books_distinct_sort_list)
            # queryset_books = Book.objects.filter(**filter_dict)
            list_tuple_books = queryset_books_distinct_sort.values_list("title")
            books_list_title = [book.title for book in queryset_books_distinct_sort]
            books_result_title.extend(books_list_title)
            # queryset_books_sort = queryset_books.order_by(context_get["search_ordering"])
            books_result_queryset_list_sort.extend(queryset_books_distinct_sort_list)
            # books_result_queryset_list_sort.extend(list(set(queryset_book_sort for queryset_book_sort in queryset_books_sort)))
            context_get["books_result_queryset_list_sort"] = queryset_books_distinct_sort_list
            # print('books_result_sort', queryset_books_sort)
            # queryset_b = Book.objects.filter(**filter_dict)
            # # print('queryset_b', queryset_b)
            # for book in queryset_b:
            books_result_queryset.extend(queryset_books_distinct_sort)
            books_result_queryset_distinct.extend(queryset_books_distinct_sort)
            books_result_title.extend([book.title for book in queryset_books_distinct_sort])
            # for book in queryset_books_sort:
            #     books_result_queryset.append(book)
            #     books_result_title.apend(book.title)
                
        except Exception as e:
            print('796. e:', e)
    else:
        print("api_views 798")
            

    authors_result_queryset = []
    authors_result_list = []
    context_get["authors_result_found_list"] = []
    if len(context_get["books_result_queryset_list_sort"]) == 0:
        print('context_get["books_result_queryset_list_sort"] = 0')
        # msgs = ["there are no books in the database, with entered parameters:<br>", parameters]
        msgs = ["there are no books in the database, with entered parameters:<br>", context_get['parameters']]
        messages.info(request, "".join(msg for msg in msgs))

    elif len(context_get["books_result_queryset_list_sort"]) > 0: 
        # print('context_get["books_result_queryset_list_sort"] =', context_get["books_result_queryset_list_sort"])
        if context_get["author_details_q"] == "False":
            print(f'False context["form_search_get_author"] = {context_get["form_search_get_author"]}\n')
            
        
        elif context_get["author_details_q"] == "True":
            # print(f'True context["form_search_get_author"] = {context_get["form_search_get_author"]}\n')
            # context["form_search_get_author"] = "yes"
            try:
                authors_result_list_book_author = [book.author for book in context_get["books_result_queryset_list_sort"]]

                authors_result_search_book_author = list(set(authors_result_list_book_author))

                # print('authors_result_search_book_author =', authors_result_search_book_author)

                authors_result_found = [Author.objects.filter(author_name__iexact=author_result_search_book_author).last() for author_result_search_book_author in authors_result_search_book_author if Author.objects.filter(author_name__iexact=author_result_search_book_author).last()]

                # print('authors_result_found =', authors_result_found)

                if len(authors_result_found) > 0:

                    authors_result_found_list = [author_result_found for author_result_found in authors_result_found]

                    print("822 authors_result_found_list", authors_result_found_list)

                    context_get["authors_result_found_list"] = authors_result_found_list

                    authors_result_queryset.extend(authors_result_found_list)

                    authors_result_found_author_name = [author_result_found_list.author_name for author_result_found_list in authors_result_found_list]

                    authors_result_list.extend(authors_result_found_author_name)

                elif len(authors_result_found) == 0:

                    authors_found_by_surname = [Author.objects.filter(author_name__icontains=author_result_search.split()[-1]).last() for author_result_search in authors_result_search if Author.objects.filter(author_name__icontains=author_result_search.split()[-1]).last()]

                    if authors_found_by_surname:
                        authors_found_by_surname_list = [author_found_by_surname for author_found_by_surname in authors_found_by_surname]

                        print("834 authors_found_by_surname_list", authors_result_found_list)

                        context_get["authors_result_found_list"] = authors_found_by_surname_list

                        authors_result_queryset.extend(authors_found_by_surname_list)

                        authors_found_by_surname_surname = [author_found_by_surname_list.author_name for author_found_by_surname_list in authors_found_by_surname_list]

                        authors_result_list.extend(authors_found_by_surname_surname)

                    elif not authors_found_by_surname:
                        context_get["authors_result_found_list"] = authors_found_by_surname_list
                        print("elif not authors_found_by_surname:")
                        
                elif not authors_result_found and not authors_result_search:
                    print("not authors_result_found and not authors_result_search")

            except Exception as e:
                print('1. e:', e)
        
    if len(context_get["books_result_queryset_list_sort"]) == 0:
        if len(context_get["authors_result_found_list"]) == 0:
            # filtered_books = context_get["books_result_queryset_list_sort"]
            # list_authors_result_queryset_set = []
            # list_authors_result_list_set = []
            # context['books_result'] = filtered_books
            # context['filtered_books'] = filtered_books
            context_get['authors_result_set'] = context_get["authors_result_found_list"]
            context_get['books_result_get'] = context_get["books_result_queryset_list_sort"]
            context_get['authors_result_get'] = context_get["authors_result_found_list"]
            # context['num_books_result'] = len(filtered_books)
            # context['num_books_result_set'] = len(filtered_books)
            # context['num_books_result'] = len(filtered_books)
            context_get['num_books_result_get'] = len(context_get["books_result_queryset_list_sort"])
            context_get['num_authors_result_get'] = len(context_get["authors_result_found_list"])
            # book_page_obj = context['filtered_books'] #
            context_get['book_page_obj'] = context_get["books_result_queryset_list_sort"]
            # print("context_get["books_result_queryset_list_sort"] and not authors_result_queryset")

    elif len(context_get["books_result_queryset_list_sort"]) > 0:
        # if len(authors_result_queryset) == 0:
        if len(context_get["authors_result_found_list"]) == 0:
            context_get['authors_result_set'] = context_get["authors_result_found_list"]
            context_get['books_result_get'] = context_get["books_result_queryset_list_sort"]
            context_get['authors_result_get'] = context_get["authors_result_found_list"]
            context_get['num_books_result_get'] = len(context_get["books_result_queryset_list_sort"])
            context_get['num_authors_result_get'] = len(context_get["authors_result_found_list"])
            context_get['book_page_obj'] = context_get["books_result_queryset_list_sort"]
            # print("context_get["books_result_queryset_list_sort"] and not authors_result_queryset")
        elif len(context_get["authors_result_found_list"]) > 0:
            context_get['authors_result_set'] = context_get["authors_result_found_list"]
            context_get['books_result_get'] = context_get["books_result_queryset_list_sort"]
            context_get['authors_result_get'] = context_get["authors_result_found_list"]
            context_get['num_books_result_get'] = len(context_get["books_result_queryset_list_sort"])
            context_get['num_authors_result_get'] = len(context_get["authors_result_found_list"])
            context_get['book_page_obj'] = context_get["books_result_queryset_list_sort"]

    dict_values = ' '.join([dic_v.replace("__gte", "-start").replace("__lt", "-end").replace("__icontains", "").replace("__contains", "") if dic_v != '' and dic_v != None and not isinstance(dic_v, int) else f"{dic_v}" if isinstance(dic_v, int) else f"{dic_v}" for dic_v in keywords_fields.values()])


    if dict_values == "":
        context_get['dict_values'] = dict_values
        print('if dict_values == "":')
        
    elif dict_values != "":
        # print('dict_values = ', dict_values)
        print('elif dict_values != "":')

    book_page_obj = context_get['book_page_obj']
    paginated_filtered_books = Paginator(book_page_obj, 10) 
    page_number = request.GET.get('page')
    book_page_obj = paginated_filtered_books.get_page(page_number)
    
    # print("book_page_obj:", book_page_obj)
    # keywords_fields = {}
    # print('return keywords_fields:', keywords_fields)
    # return render(request, 'records.html', context)
    
    # return Response(context_get, template_name='records.html', )

    author = BooksAuthor()
    form_search = ItemsSearchForm()
    book_sort = BookSort(request.GET)
    search_form = SearchRecord()
    context_get['search_author'] = author
    context_get['search_form'] = search_form
    context_get['form_search'] = form_search
    context_get['book_sort'] = book_sort

    context['search_author'] = author
    context['search_form'] = search_form
    context['form_search'] = form_search
    context['book_sort'] = book_sort
    return Response(context_get, template_name='records_get.html', )

@api_view(['GET', 'POST'])
# @permission_classes([])  
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer])
def records_view_post(request):
    r_user = request.user
    current_url_name = request.path

    all_books = Book.objects.all()
    all_authors = Author.objects.all()

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    
    context = context_main

    # search_form = SearchRecord()
    # book_sort = BookSort(request.GET)
    # search_form = SearchRecord(request.GET)
    book_sort = BookSort(request.GET)
    search_form = SearchRecord()
    author = BooksAuthor()
    context['allbooks'] = all_books
    context['allauthors'] = all_authors

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name

    allbooks_dict = context['allbooks']
    allauthors_dict = context['allauthors']
    
    current_url_name = request.path
    # current_url_name = request.resolver_match.url_name
    # currents.append(current_url_name)

    context['search_author'] = author
    context['search_form'] = search_form
    context['book_sort'] = book_sort
    
    context['parameters_post'] =  ""
    context["form_search_post"] = "no"
    # context_get = {}
    # context_get['parameters'] = ""
    # context_get["form_search_get_author"] = "no"
    # context_get["form_search_get_book"] = "no"
    parameters = ""
    values = ""
    search_resultA = []
    search_resultB = []
    form_search = ItemsSearchForm(request.POST)
    context['form_search'] = form_search
    keywords_fields = {}
    context_post = {}
    filter_dict = {}
    if not form_search.is_valid(): 
        return redirect('booksmart:allrecords')  #()
        # return redirect(current_url_name)
        #  return redirect('/')
    
    elif form_search.is_valid():
        search_phrase = form_search.cleaned_data['search_field']
        values = search_phrase
        context_post["values"] = values
        print("context_post'values'] =", context_post["values"])
        #  context['parameters'] = values
        context['parameters_post'] = context_post["values"]
        context["form_search_post"] = "yes"

        
        search_resultB_Q = allbooks_dict.filter(
            Q(author__contains=search_phrase.capitalize()) |
            Q(title__icontains=search_phrase.upper()) |
            Q(title__icontains=search_phrase) |
            Q(language__contains=search_phrase.lower()) |
            Q(category__contains=search_phrase.capitalize()) |
            Q(owner__username__contains=search_phrase)  
        )
        
        # print("list(set(search_resultB.values_list('surname')))", list(set(search_resultB.values_list('surname'))))
        search_resultAb_Q = allauthors_dict.filter(
        #search_resultA = all_authors.filter(
            Q(author_name__contains=search_phrase.capitalize()) |
            Q(owner__username__icontains=search_phrase)
        )
        print('942 views_apiview search_resultAb')
        # search_result = all_books.filter(author__icontains=search_phrase).filter(title__icontains=search_phrase).filter(language__icontains=search_phrase).filter(category__icontains=search_phrase)

        # search_word = all_books.filter(author__icontains=search_phrase).filter(title__icontains=search_phrase).filter(language__icontains=search_phrase).filter(category__icontains=search_phrase)
        # search_result = all_books.filter(title__icontains=title, author__icontains=author, google_id=google_id, language=language, published__gte=published_start, published_lte=pbulished_end)

        search_resultB = [found_book for found_book in search_resultB_Q]
        context_post["search_resultB"] = search_resultB
        search_resultAb = [found_author for found_author in search_resultAb_Q]
        search_resultA = []
        context_post["search_resultA"] = []
        if search_resultB and search_resultAb:

            list_surname_search_resultB = list(set(record_b.surname for record_b in search_resultB))
            list_last_name_search_resultAb = [record_a.last_name for record_a in search_resultAb]

            if len(list_surname_search_resultB) == 1:
                search_resultA_1 = list(allauthors_dict.filter(last_name=list_surname_search_resultB[0]))
                if search_resultA_1:
                    search_resultA = list(set(search_resultAb + search_resultA_1))
                    context_post["search_resultA"] = search_resultA
                else:
                    search_resultA = search_resultAb
                    context_post["search_resultA"] = search_resultA
            elif len(list_surname_search_resultB) > 1:
                search_resultA_1 = [Author.objects.filter(last_name__iexact=author_found_post).last() for author_found_post in list_surname_search_resultB if Author.objects.filter(last_name__iexact=author_found_post).last()]
                
                if search_resultA_1:
                    search_resultA = list(set(search_resultAb + search_resultA_1))
                    context_post["search_resultA"] = search_resultA
                else:
                    search_resultA = search_resultAb
                    context_post["search_resultA"] = search_resultA

        elif search_resultB and not search_resultAb:
            list_surname_search_resultB = list(set(record_b.surname for record_b in search_resultB))
            if len(list_surname_search_resultB) == 1:
                search_resultA_1 = allauthors_dict.filter(last_name=list_surname_search_resultB[0]) 
                if search_resultA_1:
                    search_resultA = search_resultA_1
                    context_post["search_resultA"] = search_resultA

            elif len(list_surname_search_resultB) > 1:
                # if search_resultAb:
                #     authors_result_queryset_post.append(search_resultAb)
                print("1053 wiews_apiview list_authors_search_resultB > 1")
                search_resultA_1 = [Author.objects.filter(last_name__iexact=author_found_post).last() for author_found_post in list_surname_search_resultB if Author.objects.filter(last_name__iexact=author_found_post).last()]
                if search_resultA_1:
                    search_resultA = search_resultA_1
                    context_post["search_resultA"] = search_resultA
                else:
                    search_resultA = []
                    context_post["search_resultA"] = search_resultA


        print('len search_resultB:', len(context_post["search_resultB"]))
        print('len search_resultA:', len(context_post["search_resultA"]))
        num_books_result_Q = len(context_post["search_resultB"])
        num_authors_result_Q = len(context_post["search_resultA"])
        print('2. search_resultB:', context_post["search_resultB"])
        print('2. search_resultA:', context_post["search_resultA"])
        context["books_result"] = num_books_result_Q
        context['num_books_result'] = num_books_result_Q
        context['num_authors_result'] = num_authors_result_Q
        # context['form_search'] = form_search

        context['num_books_result_post'] = num_books_result_Q
        context['num_authors_result_post'] = num_authors_result_Q
        # context['book_obj'] = search_resultB
        
        context['author_objects'] = context_post["search_resultA"]
        context["search_resultA"] = context_post["search_resultA"]
        context["search_resultB"] = context_post["search_resultB"]
        # paginator = Paginator(search_resultB, 3)
        # page_number = request.GET.get('page', 1)
        # page_obj = paginator.get_page(page_number)
        # context['page_obj'] = page_obj
        # return render(request, 'records.html', context)
        filtered_books = context_post["search_resultB"]
        # filtered_books = books_result.reverse()
        # print('filtered_books', filtered_books)
        context_post['filtered_books'] = filtered_books
        paginated_filtered_books = Paginator(context_post['filtered_books'], 10) 
        page_number = request.GET.get('page')
        book_page_obj = paginated_filtered_books.get_page(page_number)
        context['book_page_obj'] = book_page_obj
        # print(book_page_obj)
        keywords_fields = {}
        # print('return keywords_fields:', keywords_fields)
        return Response(context, template_name='records_post.html', )


    # context['num_books_result_post'] = None
    # context['num_authors_result_post'] = None
    # context['parameters_post'] = ""
    # context["form_search_post"] = "yes"
    # context['parameters'] = ""

    print('views_apiview 1081')
    # book_sort = BookSort()
    # search_form = SearchRecord()
    # author = BooksAuthor()
    form_search = ItemsSearchForm() 
    # form_search = ItemsSearchForm(request.POST)
    # context['book_sort'] = book_sort
    # context['search_form'] = search_form
    # context['search_author'] = author
    context['form_search'] = form_search
    # context['form_search'] = ItemsSearchForm()

    # return Response(context, template_name='records.html', )
    return Response(context, template_name='records_post.html', )


# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_cookie, vary_on_headers
# BOOKS_RESULT_PER_PAGE = 10
# class RecordsView(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
#     # authentication_classes = []
#     renderer_classes = [JSONRenderer, TemplateHTMLRenderer, HTMLFormRenderer]
#     # permission_classes = [IsAuthenticated,]
#     # permission_classes = []
#     # renderer_classes=[TemplateHTMLRenderer]
#     # template_name="register.html"

#     # def get_form_kwargs(self):
#     #     # kwargs = super().get_form_kwargs()
#     #     # kwargs.update({'request': self.request})
#     #     # return kwargs
#     #     kwargs = super(SearchRecord, self).get_form_kwargs()
#     #     kwargs['GET', 'request'] = self.request
#     #     return kwargs
#     # authentication_classes = []
#     # permission_classes = [] #IsAuthenticated
#     # filter_backends = [base_filters.OrderingFilter,]
#     # ordering_fields = ['published', 'title']
#     # def get_form_kwargs(self, **kwargs):
#     #     kwargs = super().get_form_kwargs()
#     #     kwargs.update({'request': self.request})
#     #     # kwargs.update({'request': self.request})
#     #     return kwargs
#     @method_decorator(vary_on_headers("Authorization",))
#     def get(self, request, *args, **kwargs):
#         r_user = request.user
#         current_url_name_get = request.path
        
#         all_books = Book.objects.all()
#         all_authors = Author.objects.all()
#         num_books = Book.objects.all().count()
#         num_authors = Author.objects.all().count()

#         context_get = context_main

#         context_get['allbooks'] = all_books
#         context_get['allauthors'] = all_authors

#         context_get['num_authors'] = num_authors
#         context_get['num_books'] = num_books
#         context_get['current_url'] = current_url_name_get        
        
#         context_get['user_id'] = r_user.id 
#         author = BooksAuthor()
#         form_search = ItemsSearchForm()
#         book_sort = BookSort(request.GET)
#         search_form = SearchRecord(request.GET)

#         # search_form = SearchRecord(request=request)
#         # id_user = IdUser()
#         # context['user_id'] = user_id
#         # current_url_name = request.resolver_match.url_name
#         # currents.append(current_url_name)

#         context_get['search_author'] = author
#         context_get['search_form'] = search_form
#         context_get['form_search'] = form_search
#         context_get['book_sort'] = book_sort

#         min_date = Book.objects.aggregate(Min('published'))
#         #min_date = Book.objects.agregate(min_date=Min('date'))
#         # print("min_date['published__min']:", min_date['published__min'])
#         # print("min_date['published__min'].strftime('%Y-%m-%d'):", min_date['published__min'].strftime('%Y-%m-%d'))
#         max_date = Book.objects.aggregate(Max('published'))
#         # max_date = Book.objects.agregate(max_date=Max('date')).value()
#         # print("max_date['published__max']:", max_date['published__max'])
#         # print("max_date['published__max'].strftime('%Y-%m-%d'):" , max_date['published__max'].strftime('%Y-%m-%d'))
#         context = {}
#         context_post = {}
#         sort_parameter = ['title']

#         context["form_search_post"] = "no"
#         context_get["form_search_get_book"] = "no"
#         context_get["form_search_get_author"] = "no"
#         parameters = ""
#         values = ""
#         dict_values = ""

#         search_resultA = []
#         search_resultB = []
#         # context['author_objects'] = []
#         # context['filtered_books'] = []
#         filtered_books = []
#         # search_user_num_b_byname = request.GET["name_user_num_b"]
#         keywords_fields = {}
        
#         filter_dict = {}
#         # context_get["filtered_books"] = []
#         context["search_resultB"] = []
#         context['author_objects'] = []
#         context["search_resultA"] = []
#         extra_keywords_fields_search_user_num_b = []
#         if search_form.is_valid():
#             context_get["form_search_get_book"] = "yes"  ###
            
#             # search_user_num_b = str(search_form.cleaned_data["user_num_b"])
#             # print('str(search_form.cleaned_data["user_num_b"]) =', str(search_form.cleaned_data["user_num_b"])) 
#             # context_get["search_user_num_b"] = str(search_form.cleaned_data["user_num_b"])  
#             keywords_fields["user_num_b"] = r_user.id if str(search_form.cleaned_data["user_num_b"]) == "True" else ""
#             # print('keywords_fields["user_num_b"] =', keywords_fields["user_num_b"])
#             # print('context_get["search_user_num_b"] =', context_get["search_user_num_b"])
#             # context_get_keywords_fields["search_user_num_b"] = str(search_form.cleaned_data["user_num_b"])
            
#             # search_epub = "yes" if str(search_form.cleaned_data["epub"]) == "True" else ""
#             # print('str(search_form.cleaned_data["epub"]) =', str(search_form.cleaned_data["user_num_b"]))
#             keywords_fields["epub"] = "yes" if str(search_form.cleaned_data["epub"]) == "True" else ""
#             # print('keywords_fields["epub"] =', keywords_fields["epub"])
#             # search_title = search_form.cleaned_data['title']
#             keywords_fields['title__icontains'] = search_form.cleaned_data['title']
            
#             # search_author = search_form.cleaned_data['author']
#             keywords_fields['author__icontains'] = search_form.cleaned_data['author']

#             # search_language = search_form.cleaned_data["language"]
#             keywords_fields['language'] = search_form.cleaned_data["language"]

#             # search_google_id = search_form.cleaned_data["google_id"]
#             keywords_fields['google_id'] = search_form.cleaned_data["google_id"]

#             # search_published__gte = search_form.cleaned_data["published__gte"]
#             keywords_fields['published__gte'] = search_form.cleaned_data["published__gte"]

#             # search_published__lt = search_form.cleaned_data["published__lt"]
#             keywords_fields['published__lt'] = search_form.cleaned_data["published__lt"]

#             # search_owner = search_form.cleaned_data["owner__username"]
#             keywords_fields["owner__username__icontains"] = search_form.cleaned_data["owner__username"]

#             # search_author_list = search_form.cleaned_data["author_list"] ###
#             keywords_fields["author"] = search_form.cleaned_data["author_list"]

#             # search_ordering = search_form.cleaned_data["ordering"]
#             context_get["search_ordering"] = search_form.cleaned_data["ordering"] if search_form.cleaned_data["ordering"] != "" else "title"
#             # print('context_get["search_ordering"] =', context_get["search_ordering"])
#             # author_details_q = str(search_form.cleaned_data["author_details_q"])
#             # print('str(search_form.cleaned_data["epub"]) =', str(search_form.cleaned_data["user_num_b"]))
#             context_get["author_details_q"] = str(search_form.cleaned_data["author_details_q"])
#             # print('context_get["author_details_q"] =', context_get["author_details_q"])

#             # print("author_details_q =", author_details_q)
#         # keywords_fields['title__icontains'] = search_title.upper()
#         # context_get["search_user_num_b"] = search_user_num_b
#         # keywords_fields["epub"] = search_epub
#         # keywords_fields['title__icontains'] = search_title
#         # keywords_fields['author__icontains'] = search_author
#         # keywords_fields['language'] = search_language
#         # keywords_fields['google_id'] = search_google_id
#         # keywords_fields['published__gte'] = search_published__gte
#         # keywords_fields['published__lt'] = search_published__lt
#         # keywords_fields["owner__username__icontains"] = search_owner 
#         # keywords_fields["author"] = search_author_list ###
#         # context_get["search_ordering"] = search_ordering
#         # context_get["author_details_q"] = author_details_q
#         #keywords_fields["title"] = search_user_books
        
#         # keywords_fields["user_num_b"] = search_user_num_b
#         # print('keywords_fields:', keywords_fields)
#         print()
#         if context_get["author_details_q"] == "False":
#             context_get["form_search_get_author"] = "no"
#         elif context_get["author_details_q"] == "True":
#             context_get["form_search_get_author"] = "yes"

#         # if len(kewords_fields.values) != 0:
#         for val in keywords_fields.values():
#             if not val != '' and not val != None:
#                 msgs = ["It is necessary to pass any params to search"]
#                 contex_get["no_params"] = "no params"
#                 messages.info(request, "".join(msg for msg in msgs))
#                 return Response(context_get, template_name='allrecords.html', )

        
#         if keywords_fields['published__gte'] != None and keywords_fields['published__gte'] != '':
#             # keywords_fields['published__gte'] = search_published__gte.strftime('%Y-%m-%d')  
#             keywords_fields['published__gte'] = keywords_fields['published__gte'].strftime('%Y-%m-%d')
#         else:
#             keywords_fields['published__gte'] = None

#         if keywords_fields['published__lt']:
#             # d = search_published__lt
#             # keywords_fields['published__lt'] = d.strftime('%Y-%m-%d')  
#             keywords_fields['published__lt'] = keywords_fields['published__lt'].strftime('%Y-%m-%d')
#         else:
#             keywords_fields['published__lt'] = None

#         keywords_fields_items = list(keywords_fields.items())
#         # query = '&'.join([f"{k}={v.replace(' ','+')}" if v == type(str) else f'{k}=' for k, v in keywords_fields.items()])
#         # print("query", query)

#         parameters_list = []
        
#         # print('keywords_fields_items =', keywords_fields_items)
#         for key, value in keywords_fields_items:
#             if value != '' and value != None and not isinstance(value, int):
#                 # parameters_list.append((key, value))
#                 parameters_list.append((str(key).replace("__gte", "-start").replace("__lt", "-end").replace("__icontains", "").replace("__contains", ""), value))
#                 filter_dict[key] = value
#             elif isinstance(value, int):
#                 filter_dict[key] = f"{value}"

#         # print("parameters_list=", parameters_list)
#         if len(parameters_list) == 0:
#             context_get['parameters'] = ""
#             context_get['parameters_get'] = ""

#         # if len(keywords_fields.values()) == 2:
#         elif len(parameters_list) == 1:
#             # print(f'1 parameters_list 557: {parameters_list}')
#             # parameters = f"{parameters_list[0][0]: {parameters_list[0][1]}}"
#             parameters = f"{parameters_list[0][0]}: {parameters_list[0][1]}"
#             context_get['parameters'] = parameters
#             context_get['parameters_get'] = parameters
            
#         elif len(parameters_list) > 1:
#             # print(f'2 parameters_list line 559: {parameters_list}')
#             parameters = ',<br>'.join([': '.join([str(e)[:e.index('_')] if not isinstance(e, int) and '_' in e else e if not isinstance(e, int) else str(e) for e in el]) for el in parameters_list])
#             context_get['parameters'] = parameters
#             context_get['parameters_get'] = parameters
            
#         key = ''.join(filter_dict.keys())
#         val = ''.join(filter_dict.values())

        
#         books_result_queryset_distinct = []
#         books_result_queryset = []
#         books_result_title = [] # list with books title
#         books_title = []
#         books_result_queryset_list_sort = [] # queryset list with books

#         if not filter_dict:
#             all_books_sort = Book.objects.all().order_by(context_get["search_ordering"])
#             # books_result_queryset.extend(list(all_books_sort))
#             books_result_queryset_list_sort.extend(all_books_sort)
#             msgs = ["You should enter some parameters for the search to work",]
#             context_get['no_params'] = "no params"
#             messages.info(request, "".join(msg for msg in msgs))
#             return Response(context, template_name='allrecords.html', )

#         elif filter_dict:

#             try:
#                 queryset_books_distinct_sort = Book.objects.filter(**filter_dict).distinct().order_by(context_get["search_ordering"])
#                 queryset_books_distinct_sort_list = [book for book in queryset_books_distinct_sort]
#                 # print("queryset_books_distinct_sort_list =", queryset_books_distinct_sort_list)
#                 # queryset_books = Book.objects.filter(**filter_dict)
#                 list_tuple_books = queryset_books_distinct_sort.values_list("title")
#                 books_list_title = [book.title for book in queryset_books_distinct_sort]
#                 books_result_title.extend(books_list_title)
#                 # queryset_books_sort = queryset_books.order_by(context_get["search_ordering"])
#                 books_result_queryset_list_sort.extend(queryset_books_distinct_sort_list)
#                 # books_result_queryset_list_sort.extend(list(set(queryset_book_sort for queryset_book_sort in queryset_books_sort)))
#                 context_get["books_result_queryset_list_sort"] = queryset_books_distinct_sort_list
#                 # print('books_result_sort', queryset_books_sort)
#                 # queryset_b = Book.objects.filter(**filter_dict)
#                 # # print('queryset_b', queryset_b)
#                 # for book in queryset_b:
#                 books_result_queryset.extend(queryset_books_distinct_sort)
#                 books_result_queryset_distinct.extend(queryset_books_distinct_sort)
#                 books_result_title.extend([book.title for book in queryset_books_distinct_sort])
#                 # for book in queryset_books_sort:
#                 #     books_result_queryset.append(book)
#                 #     books_result_title.apend(book.title)
                    
#             except Exception as e:
#                 print('796. e:', e)
#         else:
#             print("api_views 798")
                

#         authors_result_queryset = []
#         authors_result_list = []
#         context_get["authors_result_found_list"] = []
#         if len(context_get["books_result_queryset_list_sort"]) == 0:
#             print('context_get["books_result_queryset_list_sort"] = 0')
#             # msgs = ["there are no books in the database, with entered parameters:<br>", parameters]
#             msgs = ["there are no books in the database, with entered parameters:<br>", context_get['parameters']]
#             messages.info(request, "".join(msg for msg in msgs))

#         elif len(context_get["books_result_queryset_list_sort"]) > 0: 
#             # print('context_get["books_result_queryset_list_sort"] =', context_get["books_result_queryset_list_sort"])
#             if context_get["author_details_q"] == "False":
#                 print(f'False context["form_search_get_author"] = {context_get["form_search_get_author"]}\n')
                
           
#             elif context_get["author_details_q"] == "True":
#                 # print(f'True context["form_search_get_author"] = {context_get["form_search_get_author"]}\n')
#                 # context["form_search_get_author"] = "yes"
#                 try:
#                     authors_result_list_book_author = [book.author for book in context_get["books_result_queryset_list_sort"]]

#                     authors_result_search_book_author = list(set(authors_result_list_book_author))

#                     # print('authors_result_search_book_author =', authors_result_search_book_author)

#                     authors_result_found = [Author.objects.filter(author_name__iexact=author_result_search_book_author).last() for author_result_search_book_author in authors_result_search_book_author if Author.objects.filter(author_name__iexact=author_result_search_book_author).last()]

#                     # print('authors_result_found =', authors_result_found)

#                     if len(authors_result_found) > 0:

#                         authors_result_found_list = [author_result_found for author_result_found in authors_result_found]

#                         print("822 authors_result_found_list", authors_result_found_list)

#                         context_get["authors_result_found_list"] = authors_result_found_list

#                         authors_result_queryset.extend(authors_result_found_list)

#                         authors_result_found_author_name = [author_result_found_list.author_name for author_result_found_list in authors_result_found_list]

#                         authors_result_list.extend(authors_result_found_author_name)

#                     elif len(authors_result_found) == 0:

#                         authors_found_by_surname = [Author.objects.filter(author_name__icontains=author_result_search.split()[-1]).last() for author_result_search in authors_result_search if Author.objects.filter(author_name__icontains=author_result_search.split()[-1]).last()]

#                         if authors_found_by_surname:
#                             authors_found_by_surname_list = [author_found_by_surname for author_found_by_surname in authors_found_by_surname]

#                             print("834 authors_found_by_surname_list", authors_result_found_list)

#                             context_get["authors_result_found_list"] = authors_found_by_surname_list

#                             authors_result_queryset.extend(authors_found_by_surname_list)

#                             authors_found_by_surname_surname = [author_found_by_surname_list.author_name for author_found_by_surname_list in authors_found_by_surname_list]

#                             authors_result_list.extend(authors_found_by_surname_surname)

#                         elif not authors_found_by_surname:
#                             context_get["authors_result_found_list"] = authors_found_by_surname_list
#                             print("elif not authors_found_by_surname:")
                            
#                     elif not authors_result_found and not authors_result_search:
#                         print("not authors_result_found and not authors_result_search")

#                 except Exception as e:
#                     print('1. e:', e)
            
#         if len(context_get["books_result_queryset_list_sort"]) == 0:
#             if len(context_get["authors_result_found_list"]) == 0:
#                 # filtered_books = context_get["books_result_queryset_list_sort"]
#                 # list_authors_result_queryset_set = []
#                 # list_authors_result_list_set = []
#                 # context['books_result'] = filtered_books
#                 # context['filtered_books'] = filtered_books
#                 context_get['authors_result_set'] = context_get["authors_result_found_list"]
#                 context_get['books_result_get'] = context_get["books_result_queryset_list_sort"]
#                 context_get['authors_result_get'] = context_get["authors_result_found_list"]
#                 # context['num_books_result'] = len(filtered_books)
#                 # context['num_books_result_set'] = len(filtered_books)
#                 # context['num_books_result'] = len(filtered_books)
#                 context_get['num_books_result_get'] = len(context_get["books_result_queryset_list_sort"])
#                 context_get['num_authors_result_get'] = len(context_get["authors_result_found_list"])
#                 # book_page_obj = context['filtered_books'] #
#                 context_get['book_page_obj'] = context_get["books_result_queryset_list_sort"]
#                 # print("context_get["books_result_queryset_list_sort"] and not authors_result_queryset")

#         elif len(context_get["books_result_queryset_list_sort"]) > 0:
#             # if len(authors_result_queryset) == 0:
#             if len(context_get["authors_result_found_list"]) == 0:
#                 context_get['authors_result_set'] = context_get["authors_result_found_list"]
#                 context_get['books_result_get'] = context_get["books_result_queryset_list_sort"]
#                 context_get['authors_result_get'] = context_get["authors_result_found_list"]
#                 context_get['num_books_result_get'] = len(context_get["books_result_queryset_list_sort"])
#                 context_get['num_authors_result_get'] = len(context_get["authors_result_found_list"])
#                 context_get['book_page_obj'] = context_get["books_result_queryset_list_sort"]
#                 # print("context_get["books_result_queryset_list_sort"] and not authors_result_queryset")
#             elif len(context_get["authors_result_found_list"]) > 0:
#                 context_get['authors_result_set'] = context_get["authors_result_found_list"]
#                 context_get['books_result_get'] = context_get["books_result_queryset_list_sort"]
#                 context_get['authors_result_get'] = context_get["authors_result_found_list"]
#                 context_get['num_books_result_get'] = len(context_get["books_result_queryset_list_sort"])
#                 context_get['num_authors_result_get'] = len(context_get["authors_result_found_list"])
#                 context_get['book_page_obj'] = context_get["books_result_queryset_list_sort"]

#         dict_values = ' '.join([dic_v.replace("__gte", "-start").replace("__lt", "-end").replace("__icontains", "").replace("__contains", "") if dic_v != '' and dic_v != None and not isinstance(dic_v, int) else f"{dic_v}" if isinstance(dic_v, int) else f"{dic_v}" for dic_v in keywords_fields.values()])


#         if dict_values == "":
#             context_get['dict_values'] = dict_values
#             print('if dict_values == "":')
            
#         elif dict_values != "":
#             # print('dict_values = ', dict_values)
#             print('elif dict_values != "":')

#         book_page_obj = context_get['book_page_obj']
#         paginated_filtered_books = Paginator(book_page_obj, 10) 
#         page_number = request.GET.get('page')
#         book_page_obj = paginated_filtered_books.get_page(page_number)
        
#         # print("book_page_obj:", book_page_obj)
#         # keywords_fields = {}
#         # print('return keywords_fields:', keywords_fields)
#         # return render(request, 'records.html', context)
        
#         # return Response(context_get, template_name='records.html', )

#         author = BooksAuthor()
#         form_search = ItemsSearchForm()
#         book_sort = BookSort(request.GET)
#         search_form = SearchRecord()
#         context_get['search_author'] = author
#         context_get['search_form'] = search_form
#         context_get['form_search'] = form_search
#         context_get['book_sort'] = book_sort

#         context['search_author'] = author
#         context['search_form'] = search_form
#         context['form_search'] = form_search
#         context['book_sort'] = book_sort
#         return Response(context_get, template_name='records_get.html', )
        

#     @method_decorator(vary_on_headers("Authorization",))
#     def post(self, request, *args, **kwargs):
#         r_user = request.user
#         current_url_name_post = request.path

#         all_books = Book.objects.all()
#         all_authors = Author.objects.all()

#         num_books = Book.objects.all().count()
#         num_authors = Author.objects.all().count()
        
#         context = context_main

#         # search_form = SearchRecord()
#         # book_sort = BookSort(request.GET)
#         # search_form = SearchRecord(request.GET)
#         book_sort = BookSort(request.GET)
#         search_form = SearchRecord()
#         author = BooksAuthor()
#         context['allbooks'] = all_books
#         context['allauthors'] = all_authors

#         context['num_authors'] = num_authors
#         context['num_books'] = num_books
#         context['current_url'] = current_url_name_post

#         allbooks_dict = context['allbooks']
#         allauthors_dict = context['allauthors']
       
#         current_url_name = request.path
#         # current_url_name = request.resolver_match.url_name
#         # currents.append(current_url_name)

#         context['search_author'] = author
#         context['search_form'] = search_form
#         context['book_sort'] = book_sort
        
#         context['parameters_post'] =  ""
#         context["form_search_post"] = "no"
#         context_get = {}
#         context_get['parameters'] = ""
#         context_get["form_search_get_author"] = "no"
#         context_get["form_search_get_book"] = "no"
#         parameters = ""
#         values = ""
#         search_resultA = []
#         search_resultB = []
#         form_search = ItemsSearchForm(request.POST)
#         context['form_search'] = form_search
#         keywords_fields = {}
#         context_post = {}
#         filter_dict = {}
#         if not form_search.is_valid(): 
#             return redirect('booksmart:allrecords')  #()
#             #  return redirect('/')
        
#         elif form_search.is_valid():
#             search_phrase = form_search.cleaned_data['search_field']
#             values = search_phrase
#             context_post["values"] = values
#             print("context_post'values'] =", context_post["values"])
#             #  context['parameters'] = values
#             context['parameters_post'] = context_post["values"]
#             context["form_search_post"] = "yes"

            
#             search_resultB_Q = allbooks_dict.filter(
#                 Q(author__contains=search_phrase.capitalize()) |
#                 Q(title__icontains=search_phrase.upper()) |
#                 Q(title__icontains=search_phrase) |
#                 Q(language__contains=search_phrase.lower()) |
#                 Q(category__contains=search_phrase.capitalize()) |
#                 Q(owner__username__contains=search_phrase)  
#             )
            
#             # print("list(set(search_resultB.values_list('surname')))", list(set(search_resultB.values_list('surname'))))
#             search_resultAb_Q = allauthors_dict.filter(
#             #search_resultA = all_authors.filter(
#                 Q(author_name__contains=search_phrase.capitalize()) |
#                 Q(owner__username__icontains=search_phrase)
#             )
#             print('942 views_apiview search_resultAb')
#             # search_result = all_books.filter(author__icontains=search_phrase).filter(title__icontains=search_phrase).filter(language__icontains=search_phrase).filter(category__icontains=search_phrase)

#             # search_word = all_books.filter(author__icontains=search_phrase).filter(title__icontains=search_phrase).filter(language__icontains=search_phrase).filter(category__icontains=search_phrase)
#             # search_result = all_books.filter(title__icontains=title, author__icontains=author, google_id=google_id, language=language, published__gte=published_start, published_lte=pbulished_end)

#             search_resultB = [found_book for found_book in search_resultB_Q]
#             context_post["search_resultB"] = search_resultB
#             search_resultAb = [found_author for found_author in search_resultAb_Q]
#             search_resultA = []
#             context_post["search_resultA"] = []
#             if search_resultB and search_resultAb:

#                 list_surname_search_resultB = list(set(record_b.surname for record_b in search_resultB))
#                 list_last_name_search_resultAb = [record_a.last_name for record_a in search_resultAb]

#                 if len(list_surname_search_resultB) == 1:
#                     search_resultA_1 = list(allauthors_dict.filter(last_name=list_surname_search_resultB[0]))
#                     if search_resultA_1:
#                         search_resultA = list(set(search_resultAb + search_resultA_1))
#                         context_post["search_resultA"] = search_resultA
#                     else:
#                         search_resultA = search_resultAb
#                         context_post["search_resultA"] = search_resultA
#                 elif len(list_surname_search_resultB) > 1:
#                     search_resultA_1 = [Author.objects.filter(last_name__iexact=author_found_post).last() for author_found_post in list_surname_search_resultB if Author.objects.filter(last_name__iexact=author_found_post).last()]
                    
#                     if search_resultA_1:
#                         search_resultA = list(set(search_resultAb + search_resultA_1))
#                         context_post["search_resultA"] = search_resultA
#                     else:
#                         search_resultA = search_resultAb
#                         context_post["search_resultA"] = search_resultA

#             elif search_resultB and not search_resultAb:
#                 list_surname_search_resultB = list(set(record_b.surname for record_b in search_resultB))
#                 if len(list_surname_search_resultB) == 1:
#                     search_resultA_1 = allauthors_dict.filter(last_name=list_surname_search_resultB[0]) 
#                     if search_resultA_1:
#                         search_resultA = search_resultA_1
#                         context_post["search_resultA"] = search_resultA

#                 elif len(list_surname_search_resultB) > 1:
#                     # if search_resultAb:
#                     #     authors_result_queryset_post.append(search_resultAb)
#                     print("1053 wiews_apiview list_authors_search_resultB > 1")
#                     search_resultA_1 = [Author.objects.filter(last_name__iexact=author_found_post).last() for author_found_post in list_surname_search_resultB if Author.objects.filter(last_name__iexact=author_found_post).last()]
#                     if search_resultA_1:
#                         search_resultA = search_resultA_1
#                         context_post["search_resultA"] = search_resultA
#                     else:
#                         search_resultA = []
#                         context_post["search_resultA"] = search_resultA
 

#             print('len search_resultB:', len(context_post["search_resultB"]))
#             print('len search_resultA:', len(context_post["search_resultA"]))
#             num_books_result_Q = len(context_post["search_resultB"])
#             num_authors_result_Q = len(context_post["search_resultA"])
#             print('2. search_resultB:', context_post["search_resultB"])
#             print('2. search_resultA:', context_post["search_resultA"])
#             context["books_result"] = num_books_result_Q
#             context['num_books_result'] = num_books_result_Q
#             context['num_authors_result'] = num_authors_result_Q
#             # context['form_search'] = form_search

#             context['num_books_result_post'] = num_books_result_Q
#             context['num_authors_result_post'] = num_authors_result_Q
#             # context['book_obj'] = search_resultB
            
#             context['author_objects'] = context_post["search_resultA"]
#             context["search_resultA"] = context_post["search_resultA"]
#             context["search_resultB"] = context_post["search_resultB"]
#             # paginator = Paginator(search_resultB, 3)
#             # page_number = request.GET.get('page', 1)
#             # page_obj = paginator.get_page(page_number)
#             # context['page_obj'] = page_obj
#             # return render(request, 'records.html', context)
#             filtered_books = context_post["search_resultB"]
#             # filtered_books = books_result.reverse()
#             # print('filtered_books', filtered_books)
#             context_post['filtered_books'] = filtered_books
#             paginated_filtered_books = Paginator(context_post['filtered_books'], 10) 
#             page_number = request.GET.get('page')
#             book_page_obj = paginated_filtered_books.get_page(page_number)
#             context['book_page_obj'] = book_page_obj
#             # print(book_page_obj)
#             keywords_fields = {}
#             # print('return keywords_fields:', keywords_fields)
#             return Response(context, template_name='records_post.html', )


#         # context['num_books_result_post'] = None
#         # context['num_authors_result_post'] = None
#         # context['parameters_post'] = ""
#         # context["form_search_post"] = "yes"
#         # context['parameters'] = ""

#         print('views_apiview 1081')
#         # book_sort = BookSort()
#         # search_form = SearchRecord()
#         # author = BooksAuthor()
#         form_search = ItemsSearchForm() 
#         # form_search = ItemsSearchForm(request.POST)
#         # context['book_sort'] = book_sort
#         # context['search_form'] = search_form
#         # context['search_author'] = author
#         context['form_search'] = form_search
#         # context['form_search'] = ItemsSearchForm()

#         # return Response(context, template_name='records.html', )
#         return Response(context, template_name='records_post.html', )
        

    

        # https://stackoverflow.com/questions/71814729/sort-search-results-in-django
