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
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
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
@permission_classes([])  #IsAuthenticated
# @authentication_classes([]) # authentication.TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
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
            # context['no_sort_params'] = "no sort parmas"
            # all_books = Book.objects.all()
            # context['allbooks'] = all_books
            pass
    
    # all_books = all_books_sort
    # current_url_name = request.resolver_match.url_name
    # currents.append(current_url_name)

    all_books = Book.objects.all().order_by(sort_kind[-1])
    context['allbooks'] = all_books
    # print('current_url_name', current_url_name)
    context['current_url'] = current_url_name
    # print('sort_kind', sort_kind)

    # form_a = a_account_view(request)
    # #form_out = a_logout_view(request)
    # form_r = a_registration_view(request)
    # form_l = a_login_view(request)
    
    # #context['logout_form'] = form_out
    # context['login_form'] = form_l
    # context['registration_form'] = form_r
    # context['account_form'] = form_a
    filtered_books = all_books

    paginated_filtered_books = Paginator(filtered_books, 10) 
    page_number = request.GET.get('page')
    book_page_obj = paginated_filtered_books.get_page(page_number)
    context['book_page_obj'] = book_page_obj
    return Response(context, template_name='allrecords.html', )
    # return render(request, 'allrecords.html', context)

@api_view(['GET', 'POST'])
@permission_classes([])  #IsAuthenticated
# @authentication_classes([]) # authentication.TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
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
    book_sort = BookSort()
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
@permission_classes([])  #IsAuthenticated
# @authentication_classes([]) # authentication.TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
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
    book_sort = BookSort()
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
@permission_classes([])  #IsAuthenticated
# @authentication_classes([]) # authentication.TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
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
@permission_classes([])  #IsAuthenticated
# @authentication_classes([]) # authentication.TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
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
    book_sort = BookSort()
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
@permission_classes([])  #IsAuthenticated
# @authentication_classes([]) # authentication.TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
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
    book_sort = BookSort()
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
@permission_classes([])  #IsAuthenticated
# @authentication_classes([]) # authentication.TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
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
    book_sort = BookSort()
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



BOOKS_RESULT_PER_PAGE = 10
class RecordsView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer, HTMLFormRenderer]
    permission_classes = [IsAuthenticated,]
    # renderer_classes=[TemplateHTMLRenderer]
    template_name="register.html"

    # def get_form_kwargs(self):
    #     # kwargs = super().get_form_kwargs()
    #     # kwargs.update({'request': self.request})
    #     # return kwargs
    #     kwargs = super(SearchRecord, self).get_form_kwargs()
    #     kwargs['GET', 'request'] = self.request
    #     return kwargs
    # authentication_classes = []
    # permission_classes = [] #IsAuthenticated
    # filter_backends = [base_filters.OrderingFilter,]
    # ordering_fields = ['published', 'title']
    # def get_form_kwargs(self, **kwargs):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'request': self.request})
    #     # kwargs.update({'request': self.request})
    #     return kwargs

    def get(self, request, *args, **kwargs):
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
        
        context['user_id'] = r_user.id 
        author = BooksAuthor()
        form_search = ItemsSearchForm()
        book_sort = BookSort(request.GET)
        # search_form = SearchRecord()
        search_form = SearchRecord(request.GET)
        # context['search_form'] = ""
        # context['form_search'] = ""
        # context['book_sort'] = ""
        # context['search_author'] = ""

        # search_form = SearchRecord(request=request)
       

       
        # id_user = IdUser()
        # context['user_id'] = user_id
        # current_url_name = request.resolver_match.url_name
        # currents.append(current_url_name)

        context['search_author'] = author
        context['search_form'] = search_form
        context['form_search'] = form_search
        context['book_sort'] = book_sort

        min_date = Book.objects.aggregate(Min('published'))
        #min_date = Book.objects.agregate(min_date=Min('date'))
        # print("min_date['published__min']:", min_date['published__min'])
        # print("min_date['published__min'].strftime('%Y-%m-%d'):", min_date['published__min'].strftime('%Y-%m-%d'))
        max_date = Book.objects.aggregate(Max('published'))
        # max_date = Book.objects.agregate(max_date=Max('date')).value()
        # print("max_date['published__max']:", max_date['published__max'])
        # print("max_date['published__max'].strftime('%Y-%m-%d'):" , max_date['published__max'].strftime('%Y-%m-%d'))

        keywords_fields = {}

        sort_parameter = ['title']
        context["form_search_get"] = "no"
        # search_user_num_b_byname = request.GET["name_user_num_b"]
        if search_form.is_valid():

            context["form_search_get"] = "yes"  ###
            search_title = search_form.cleaned_data['title']
            search_author = search_form.cleaned_data['author']
            search_language = search_form.cleaned_data["language"]
            search_google_id = search_form.cleaned_data["google_id"]
            search_published__gte = search_form.cleaned_data["published__gte"]
            # print('search_published__gte', search_published__gte)
            search_published__lt = search_form.cleaned_data["published__lt"]

            search_owner = search_form.cleaned_data["owner__username"] 
            search_author_list = search_form.cleaned_data["author_list"] ###

            search_user_num_b = search_form.cleaned_data["user_num_b"]
            # search_epub = search_form.cleaned_data["epub"]
            print("search_user_num_b =", str(search_user_num_b))

            if str(search_user_num_b) == "True":
                print("search_user_num")
                # print("context['user_id']:", context['user_id'])
                # search_user_num_b = context['user_id']      
                keywords_fields["user_num_b"] = r_user.id
            else:
                # keywords_fields["user_num_b"] = ""                
                print("NO search_user_num_b")

            search_epub = search_form.cleaned_data["epub"]
            print("search_epub =", str(search_epub))
            if str(search_epub) == "True":
                keywords_fields["epub"] = "yes"
            else:
                print("NO search_epub")

            search_ordering = search_form.cleaned_data["ordering"]
            # print('search_ordering', search_ordering)
            if search_ordering != '':
                sort_parameter.append(search_ordering)
            else:
                pass

        keywords_fields['title__icontains'] = search_title.upper()
        keywords_fields['author__icontains'] = search_author
        keywords_fields['language'] = search_language
        keywords_fields['google_id'] = search_google_id
        keywords_fields['published__gte'] = search_published__gte
        keywords_fields['published__lt'] = search_published__lt

        keywords_fields["owner__username__icontains"] = search_owner 
        keywords_fields["author"] = search_author_list ###
        #keywords_fields["title"] = search_user_books
        
        # keywords_fields["user_num_b"] = search_user_num_b
        print('keywords_fields:', keywords_fields)
        # if len(kewords_fields.values) != 0:
        for val in keywords_fields.values():
            if not val != '' and not val != None:
                msgs = ["It is necessary to pass any params to search"]
                contex["no_params"] = "no params"
                messages.info(request, "".join(msg for msg in msgs))
                return Response(context, template_name='allrecords.html', )

        
        if keywords_fields['published__gte'] != None and keywords_fields['published__gte'] != '':
            keywords_fields['published__gte'] = search_published__gte.strftime('%Y-%m-%d')  
        else:
            keywords_fields['published__gte'] = None

        if keywords_fields['published__lt']:
            d = search_published__lt
            keywords_fields['published__lt'] = d.strftime('%Y-%m-%d')  
        else:
            keywords_fields['published__lt'] = None
        keywords_fields_items = list(keywords_fields.items())
        # query = '&'.join([f"{k}={v.replace(' ','+')}" if v == type(str) else f'{k}=' for k, v in keywords_fields.items()])
        # print("query", query)

        parameters_list = []
        filter_dict = {}

        for key, value in keywords_fields_items:
            if value != '' and value != None and not isinstance(value, int):
                # parameters_list.append((key, value))
                parameters_list.append((str(key).replace("__gte", "-start").replace("__lt", "-end"), value))
                filter_dict[key] = value
            elif isinstance(value, int):
                filter_dict[key] = f"{value}"

        if len(keywords_fields.values()) < 2:
            # print(f'1 parameters_list 557: {parameters_list}')
            parameters = f"{parameters_list[0]: {parameters_list[1]}}"
            
        else:
            # print(f'2 parameters_list line 559: {parameters_list}')
            parameters = ',<br>'.join([': '.join([str(e)[:e.index('_')] if not isinstance(e, int) and '_' in e else e if not isinstance(e, int) else str(e) for e in el]) for el in parameters_list])
            

        context['parameters'] = parameters
        context['parameters_get'] = parameters
        if parameters:
            context['parameters_get'] = parameters
            print("parameters =", parameters)
            print("context['parameters_get'] =", context['parameters_get'])
        else:
            print("NO context['parameters_get']")

        # print('filter_dict', filter_dict)
        key = ''.join(filter_dict.keys())
        val = ''.join(filter_dict.values())

        books_result_queryset = [] # queryset list with books
        books_result_queryset_distinct = []
        books_result_title = [] # list with books title
        # books_title = []
        if not filter_dict:
            all_books_sort = Book.objects.all().order_by(f'{sort_parameter[-1]}')
            # books_result_queryset.extend(list(all_books_sort))
            books_result_queryset.extend(all_books_sort)
            msgs = ["You should enter some parameters for the search to work",]
            context['no_params'] = "no params"
            messages.info(request, "".join(msg for msg in msgs))
            return Response(context, template_name='allrecords.html', )

            # context['allbooks'] = all_books_sort
            # return Response(context, template_name='allrecords.html', )
        elif filter_dict:

            try:
                queryset_books_distinct = Book.objects.filter(**filter_dict).distinct()
                queryset_books = Book.objects.filter(**filter_dict)
                list_tuple_books = queryset_books.values_list("title")
                books_list_title = [book.title for book in queryset_books_distinct]
                books_result_title.extend(books_list_title)
                # print("books_list_title:", books_list_title)
                # distinct This eliminates duplicate rows from the query results.
                # # print('queryset_b', queryset_b)
                # queryset <QuerySet [<Book: DAMA KAMELIOWA>, <Book: DAMA KAMELIOWA>]>
                queryset_books_sort = queryset_books.order_by(f'{sort_parameter[-1]}')

                # print('books_result_sort', queryset_books_sort)
                # queryset_b = Book.objects.filter(**filter_dict)
                # # print('queryset_b', queryset_b)
                # for book in queryset_b:
                books_result_queryset.extend(queryset_books_sort)
                books_result_queryset_distinct.extend(queryset_books_distinct)
                books_result_title.extend([book.title for book in queryset_books_sort])
                # for book in queryset_books_sort:
                #     books_result_queryset.append(book)
                #     books_result_title.apend(book.title)
                    
            except Exception as e:
                print('1. e:', e)
        else:
            pass
                
        # print('1. books_result_queryset', books_result_queryset)
        # print("1. books_result_title", books_result_title)

        # books_result = list(set(books_result))
        # # print('2. books_result', books_result)
        # books_result = tuple(books_result)

        authors_result_queryset = []
        authors_result_list = []
        if not books_result_queryset_distinct:
            # pass
            # # print('not books_result')
            # all_books_sort = Book.objects.all().order_by(f'{sort_parameter[-1]}')
            # context['allbooks'] = all_books_sort
            msgs = ["there are no books in the database, with entered parameters:<br>", parameters]
            messages.info(request, "".join(msg for msg in msgs))
            # return Response(context, template_name='allrecords.html', )
        elif books_result_queryset_distinct:
            try:
                authors_result_list = [book.author for book in books_result_queryset_distinct]
                authors_result_search = list(set(authors_result_list))
                # authors_result_search_surname = ["".join(author.split()[-1]) ]
                # print('authors_result_search:', authors_result_search)
                # authors_result_search ['Antonia Susan Byatt', 'J. R. R. Tolkien',...]
                # list_founded_authors = [Author.objects.filter(author_name=author).distinct() for author in authors_result_search]
                for author_found in authors_result_search:
                    # queryset_author = Author.objects.filter(author_name=author_found).distinct()
                    queryset_author = Author.objects.filter(author_name__iexact=author_found).last()
                    # NO author '1. queryset_author' <QuerySet []>
                    # YES author '1. queryset_author'[<Author: Jack London>]>
                    
                    if queryset_author:
                        # print()
                        print('1. queryset_author')
                        # for author in queryset_a:
                        
                        authors_result_queryset.append(queryset_author)
                        author_result_string = queryset_author.author_name
                        authors_result_list.append(author_result_string)

                    elif not queryset_author:
                        author_surname = author_found.split()[-1]
                        # print('author_surname:', author_surname)
                        try:
                            # queryset_author_surname = Author.objects.filter(last_name=author_surname).distinct()
                            queryset_author_surname = Author.objects.filter(author_name__icontains=author_surname).last()
                            if queryset_author_surname:
                                authors_result_queryset.append(queryset_author_surname)
                                author_result_string = queryset_author_surname.author_name
                                # print()
                                # print('author_result_string:', author_result_string)
                                authors_result_list.append(author_result_string)
                            else:
                                pass
                        except Exception as e:
                            print(f'views_apiview exception 642: {e}')
                            
                    else:
                        pass
                        # authors_result_list_surname = [el.author.split()[-1] for el in books_result]
                        # print('authors_result_list', authors_result_list)
                        # authors_result_search = list(set(authors_result_list))
                        # for author in authors_result_search:
                        #     queryset_a = Author.objects.filter(last_name = author).distinct()
                        #     print('2. queryset_a', queryset_a)
                        #     if queryset_a:
                        #         for author in queryset_a:
                        #             authors_result.append(author)
            except Exception as e:
                print('1. e:', e)
            
        else:
            # messages.info(request, 'It is necessary to fill in at least one field.')
            # context['message'] = 'It is necessary to fill in at least one field.'
            # queryset = ""
            # return Response(context, template_name='records.html', )
            # return render(request, 'records.html', context)
            # all_books_sort = Book.objects.all().order_by(f'{sort_parameter[-1]}')
            # context['allbooks'] = all_books_sort
            # return Response(context, template_name='allrecords.html', )
            pass

        list_authors_result_queryset_set = list(set(authors_result_queryset))
        list_authors_result_list_set = list(set(authors_result_list))
        # if request.GET:
        # print('1. books_result_queryset', books_result_queryset)
        # print('1. books_result_title', books_result_title)
        # # authors_result = list(set(authors_result))
        # print('2. list_authors_result_list_set', list_authors_result_list_set)
        # print('2. list_authors_result_queryset_set', list_authors_result_queryset_set)

        # dict_values = ' '.join([dic_v for dic_v in keywords_fields.values() if dic_v != '' and dic_v != None])
        dict_values = ' '.join([dic_v if dic_v != '' and dic_v != None and not isinstance(dic_v, int) else f"{dic_v}" if isinstance(dic_v, int) else f"{dic_v}" for dic_v in keywords_fields.values()])
        if dict_values:
            # print('dict_values:', dict_values)
            pass
        else:
            print('NO dict_values')
            # all_books_sort = Book.objects.all().order_by(f'{sort_parameter[-1]}')
            # context['allbooks'] = all_books_sort
            # return Response(context, template_name='allrecords.html', )

        context['dict_values'] = ""
        context['filtered_books'] = ""

        context['books_result'] = ""
        context['authors_result_set'] = ""
        # context['author_objects'] = list_authors_result_queryset_set
        context['num_books_result'] = ""
        context['num_books_result_set'] = "" #

        # # print('end sort_parameter', sort_parameter)
        num_books_result = len(books_result_queryset)
        num_authors_result_set = len(list_authors_result_queryset_set)
        # # print('5. books_result_queryset', books_result_queryset)
        # # print('5. list_authors_result_queryset_set', list_authors_result_queryset_set)
        # # books_result_filter = books_result.order_by('-title)
        
        filtered_books = books_result_queryset
        # filtered_books = books_result.reverse()
        # print('filtered_books', filtered_books)

        context['dict_values'] = dict_values
        context['filtered_books'] = filtered_books

        context['books_result'] = books_result_queryset
        context['authors_result_set'] = list_authors_result_queryset_set
        # context['author_objects'] = list_authors_result_queryset_set
        context['num_books_result'] = num_books_result
        context['num_books_result_set'] = num_books_result  #
        if context['num_books_result_set']:
            print("868. context['num_books_result_set'] =", context['num_books_result_set'])
        context['num_authors_result_set'] = num_authors_result_set
        if context['num_authors_result_set']:
            print("context['num_authors_result_set'] =", context['num_authors_result_set'])

        paginated_filtered_books = Paginator(filtered_books, 10) 
        page_number = request.GET.get('page')
        book_page_obj = paginated_filtered_books.get_page(page_number)
        
        context['book_page_obj'] = book_page_obj
        # print("book_page_obj:", book_page_obj)
        keywords_fields = {}
        # print('return keywords_fields:', keywords_fields)
        return Response(context, template_name='records.html', )
        # return render(request, 'records.html', context)

    def post(self, request, *args, **kwargs):
        r_user = request.user
        current_url_name = request.path

        all_books = Book.objects.all()
        all_authors = Author.objects.all()

        num_books = Book.objects.all().count()
        num_authors = Author.objects.all().count()
        book_sort = BookSort(request.GET)
        context = context_main
        context['search_form'] = ""
        context['form_search'] = ""
        context['book_sort'] = ""
        context['search_author'] = ""

        book_sort = BookSort(request.GET)
        # search_form = SearchRecord()
        search_form = SearchRecord(request.GET)
        author = BooksAuthor()
        context['allbooks'] = all_books
        context['allauthors'] = all_authors

        context['num_authors'] = num_authors
        context['num_books'] = num_books
        context['current_url'] = current_url_name

        search_form = SearchRecord()

        form_search = ItemsSearchForm(request.POST)
        
        author = BooksAuthor()
        allbooks_dict = context['allbooks']
        allauthors_dict = context['allauthors']
       
        current_url_name = request.path
        # current_url_name = request.resolver_match.url_name
        # currents.append(current_url_name)

        context['search_author'] = author
        context['search_form'] = search_form
        context['form_search'] = form_search
        context['book_sort'] = book_sort
        
        context['parameters'] = ""
        context["form_search_post"] = "no"
        if not form_search.is_valid(): 
            return redirect('booksmart:allrecords')  #()
            #  return redirect('/')
        
        elif form_search.is_valid():
            search_phrase = form_search.cleaned_data['search_field']
            values = search_phrase
            print("values =", values)
            #  context['parameters'] = values
            context['parameters_post'] = values
            context["form_search_post"] = "yes"

            
            search_resultB = allbooks_dict.filter(
            # search_resultB = all_books.filter(
                Q(author__contains=search_phrase.capitalize()) |
                Q(title__contains=search_phrase.upper()) |
                Q(language__contains=search_phrase.lower()) |
                Q(category__contains=search_phrase.capitalize()) |
                Q(owner__username__contains=search_phrase)  
            )
            
            # print("list(set(search_resultB.values_list('surname')))", list(set(search_resultB.values_list('surname'))))
            search_resultAb = allauthors_dict.filter(
            #search_resultA = all_authors.filter(
                Q(author_name__contains=search_phrase.capitalize()) |
                Q(owner__username__contains=search_phrase)
            )
            print('search_resultAb =', search_resultAb)
            # search_result = all_books.filter(author__icontains=search_phrase).filter(title__icontains=search_phrase).filter(language__icontains=search_phrase).filter(category__icontains=search_phrase)

            # search_word = all_books.filter(author__icontains=search_phrase).filter(title__icontains=search_phrase).filter(language__icontains=search_phrase).filter(category__icontains=search_phrase)
            # search_result = all_books.filter(title__icontains=title, author__icontains=author, google_id=google_id, language=language, published__gte=published_start, published_lte=pbulished_end)

            
            search_resultA = []
            if search_resultB and search_resultAb:
                search_resultAb_list = [author_resultAb for author_resultAb in search_resultAb]
                list_authors_search_resultB = list(set(record_b.surname for record_b in search_resultB))
                if len(list_authors_search_resultB) == 1:
                    search_resultA_1 = list(allauthors_dict.filter(last_name=list_authors_search_resultB[0]))
                    if search_resultA_1:
                        search_resultA = list(set(search_resultAb_list + search_resultA_1))
                    else:
                        search_resultA = search_resultAb_list
                elif len(list_authors_search_resultB) > 1:
                    search_resultA_1 = [Author.objects.filter(last_name__iexact=author_found_post).last() for author_found_post in list_authors_search_resultB if Author.objects.filter(last_name__iexact=author_found_post).last()]
                    
                    if search_resultA_1:
                        search_resultA = list(set(search_resultAb_list + search_resultA_1))
                    else:
                        search_resultA = search_resultAb_list

            elif search_resultB and not search_resultAb:
                list_authors_search_resultB = list(set(record_b.surname for record_b in search_resultB))
                if len(list_authors_search_resultB) == 1:
                    search_resultA_1 = allauthors_dict.filter(last_name=list_authors_search_resultB[0]) 
                    if search_resultA_1:
                        search_resultA = search_resultA_1

                elif len(list_authors_search_resultB) > 1:
                    # if search_resultAb:
                    #     authors_result_queryset_post.append(search_resultAb)
                    print("list_authors_search_resultB =", list_authors_search_resultB)
                    search_resultA_1 = [Author.objects.filter(last_name__iexact=author_found_post).last() for author_found_post in list_authors_search_resultB if Author.objects.filter(last_name__iexact=author_found_post).last()]
                    if search_resultA_1:
                        search_resultA = search_resultA_1
                    else:
                        search_resultA = []
 

            print('len search_resultB:', len(search_resultB))
            print('len search_resultA:', len(search_resultA))
            num_books_result_Q = len(search_resultB)
            num_authors_result_Q = len(search_resultA)
            print('2. search_resultB:', search_resultB)
            print('2. search_resultA:', search_resultA)
            context["books_result"] = num_books_result_Q
            context['num_books_result'] = num_books_result_Q
            context['num_authors_result'] = num_authors_result_Q
            context['form_search'] = form_search

            context['num_books_result_post'] = num_books_result_Q
            context['num_authors_result_post'] = num_authors_result_Q
            # context['book_obj'] = search_resultB
            
            context['author_objects'] = search_resultA

            # paginator = Paginator(search_resultB, 3)
            # page_number = request.GET.get('page', 1)
            # page_obj = paginator.get_page(page_number)
            # context['page_obj'] = page_obj
            # return render(request, 'records.html', context)
            filtered_books = search_resultB
            # filtered_books = books_result.reverse()
            # print('filtered_books', filtered_books)
            context['filtered_books'] = filtered_books
            paginated_filtered_books = Paginator(filtered_books, 10) 
            page_number = request.GET.get('page')
            book_page_obj = paginated_filtered_books.get_page(page_number)
            context['book_page_obj'] = book_page_obj
            # print(book_page_obj)
            keywords_fields = {}
            # print('return keywords_fields:', keywords_fields)
            return Response(context, template_name='records.html', )


        context['num_books_result_post'] = None
        context['num_authors_result_post'] = None
        context['parameters_post'] = ""
        context["form_search_post"] = "yes"
        context['parameters'] = ""
        context['form_search'] = ItemsSearchForm()
        return Response(context, template_name='records.html', )





