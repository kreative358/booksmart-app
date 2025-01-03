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
from booksmart.models import Book, Author, BackgroundPoster, BackgroundVideo, BackgroundMusic, url_img_author, url_img # ,context_bm, 
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
from bookmain import settings as my_settings
# from mainsite.test_docer import *
# from django.utils.text import slugify
# try:
#     txt = "Cześć: .&перевод чего-либо"
#     txt_slugify = txt.replace("-", "slugify")
#     txt_to_search = slugify(txt_slugify).replace("-", " ").replace("slugify", "-")
#     print("txt_to_search: ", txt_to_search)
# except Exception as e:
#     print("exception ", e)
import datetime
import browsers
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

context_list = []

# print("my_settings.STATIC_ROOT =", my_settings.STATIC_ROOT)

def context_mainsite_views():
    context_main = {}

    context_main['no_date'] = datetime.date(3000, 1, 1)
    context_main['url_img_book'] = url_img
    context_main['url_img_author'] = url_img_author

    try:
        if Book.objects.all().count() > 0:
        # if Book.objects.filter().all():
            # all_books = Book.objects.all()
            # context_list.append(all_books)
            num_books = Book.objects.all().count()
            # context_main['allbooks'] = all_books
            context_main['num_books'] = num_books
        elif Book.objects.all().count() == 0:
        # elif not Book.objects.filter().all():
            context_main['allbooks'] = None
            context_main['num_books'] = 0
    except Exception as err:
        print(f"mainsite views: Book.objects.all() except Exception as {err}")
        context_main['allbooks'] = None
        context_main['num_books'] = 0        

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
    except Exception as err:
        print(f"mainsite views: Author.objects.all(): except Exception as {err}")
        context_main['allauthors'] = None
        context_main['num_authors'] = 0        

    try:
        if BackgroundPoster.objects.filter().last():
            poster = BackgroundPoster.objects.filter().last()
            context_main['poster_url_1'] = poster.link_poster_1
            context_main['poster_url_2'] = poster.link_poster_2
        elif not BackgroundPoster.objects.filter().last():
            context_main['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
            context_main['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
    except Exception as err:
        print(f"booksmart views: Author.objects.all(): except Exception as {err}")
        context_main['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
        context_main['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"        

    try:
        if BackgroundVideo.objects.filter().last():   
            video = BackgroundVideo.objects.filter().last()
            context_main['video_url'] = video.link_video
            context_main['video_type'] = video.type_video
        elif not BackgroundVideo.objects.filter().last():
            context_main['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
            context_main['video_type'] = "mp4"
    except Exception as err:
        print(f"mainsite views: BackgroundVideo.objects.filter().last(): except Exception as {err}")
        context_main['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
        context_main['video_type'] = "mp4"
        
    try:
        if BackgroundMusic.objects.filter().last():   
            music = BackgroundMusic.objects.filter().last()
            context_main['music_url_1'] = music.link_music_1
            context_main['music_type_1'] = music.type_music_1
            context_main['music_url_2'] = music.link_music_2
            context_main['music_type_2'] = music.type_music_2
        elif not BackgroundMusic.objects.filter().last(): 
            context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
            context_main['music_type_1'] = "mp3"
            context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
            context_main['music_type_2'] = "mp3"
    except Exception as err:
        print(f"mainsite views: BackgroundMusic.objects.filter().last(): except Exception as {err}")
        context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_main['music_type_1'] = "mp3"
        context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_main['music_type_2'] = "mp3"
        
    context_mainsite_views.context_main = context_main
 
    return context_main  # print(list(set(Book.objects.values_list('author', 'author'))))

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
    context_mainsite_views()    
    # context = context_main
    context = context_mainsite_views.context_main
    r_user = request.user
    current_url_name = request.path

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

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
def index_home(request, *args, **kwargs):
    """View function for home page of site."""
    # book_test = Book.objects.filter(pk=4).values()[0]
    # print("book_test =", book_test)
    # context = context_main context_mainsite_views(context_main)
    # context_main = {}
    context_mainsite_views()
    context = context_mainsite_views.context_main    
    r_user = request.user
    current_url_name = request.path
    print("1. current_url_name =", current_url_name)
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    
    # try:
    #     browser_path = browsers.get("chrome")["path"]
    #     if browser_path:
    #         print("browser_path =", browser_path)
    #         context['browser_path'] = browser_path
    #     elif not browser_path:
    #         print("NO browser_path =")    
    #         context['browser_path'] = "NO browser_path"
    # except Exception as err:
    #     print(f"Exception browser_path as {err}")                 

    list_elements = []
    try:
        chrome_options_1 = webdriver.ChromeOptions()
        # chrome_service_1 = webdriver.ChromeService()
        chrome_options_1.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options_1.add_argument("--headless")
        chrome_options_1.add_argument("--disable-dev-shm-usage")
        chrome_options_1.add_argument("--no-sandbox")
        chrome_service_1 = webdriver.ChromeService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        browser_1 = webdriver.Chrome(options=chrome_options_1, service=chrome_service_1)
        time.sleep(2)
        wait = WebDriverWait(browser_1, 10)
        browser_1.get('https://news.ycombinator.com/')
        time.sleep(2)
        element_list = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title > span > a"))
        )

        for element in element_list:
            try:
                title, url = element.text, element.get_attribute('href')
                list_elements.append("<br>".join("Title:", title, "\nURL:", url, end="\n\n"))
                print("Title:", title, "\nURL:", url, end="\n\n")
            except Exception as e:
                print(f"1a.Exception akjasim as {e}")
        time.sleep(2)
        browser_1.quit()        
    except Exception as e:
        print(f"1b.Exception akjasim as {e}")
        
    time.sleep(2)  
    try:
        chrome_options_2 = webdriver.ChromeOptions()
        # chrome_service_2 = webdriver.ChromeService()
        chrome_options_2.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options_2.add_argument("--headless")
        chrome_options_2.add_argument("--disable-dev-shm-usage")
        chrome_options_2.add_argument("--no-sandbox")
        chrome_service_2 = webdriver.ChromeService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        browser_2 = webdriver.Chrome(options=chrome_options_2, service=chrome_service_2)
        time.sleep(2)
        browser_2.get('https://python.com/')
        time.sleep(2)
        try:
            browser_title = browser_2.title
            if browser_title !="" and browser_title != None:
                print("browser_path =", browser_title)
                context['browser_path'] = browser_title
            else:
                print("NO browser_title")
                context['browser_path'] = "NO browser_title"                    
            time.sleep(2)
            browser_2.quit()
        except Exception as e:
            print(f"2a.Exception michaelkitas as {e}")                    
    except Exception as e:
        print(f"2b.Exception michaelkitas as {e}")    
        
    time.sleep(2)  
    try:
        chrome_options_3 = webdriver.ChromeOptions()
        # chrome_service_3 = webdriver.ChromeService()
        chrome_options_3.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # chrome_options.add_argument("--headless")
        chrome_options_3.add_argument("--disable-dev-shm-usage")
        chrome_options_3.add_argument("--no-sandbox")
        chrome_service_3 = ChromeService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        browser_3 = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options_3, service=chrome_service_3)
        time.sleep(1)
        browser_3.get('https://python.com/')
        time.sleep(20)
        browser_3.quit()                
    except Exception as e:
        print(f"3a.Exception michaelkitas as {e}")          
            
    # try:
    #     chrome_options = webdriver.ChromeOptions()
    #     chrome_service = webdriver.ChromeService()
    #     # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    #     chrome_options.add_argument("--headless")
    #     chrome_options.add_argument("--disable-dev-shm-usage")
    #     chrome_options.add_argument("--no-sandbox")
    #     # chrome_service = ChromeService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    #     browser = webdriver.Chrome(options=chrome_options, service=chrome_service)
    #     time.sleep(2)
    #     wait = WebDriverWait(browser, 10)
    #     browser.get('https://news.ycombinator.com/')
    #     time.sleep(2)
    #     element_list = wait.until(
    #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title > span > a"))
    #     )

    #     for element in element_list:
    #         try:
    #             title, url = element.text, element.get_attribute('href')
    #             # list_elements.append("<br>".join("Title:", title, "\nURL:", url, end="\n\n"))
    #             print("Title:", title, "\nURL:", url, end="\n\n")
    #         except Exception as e:
    #             print(f"1a.Exception akjasim as {e}")
    #     time.sleep(2)
    #     browser.quit()        
    # except Exception as e:
    #     print(f"1b.Exception akjasim as {e}")    
    time.sleep(2)        
    # try:
    #     chrome_options = webdriver.ChromeOptions()
    #     chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    #     # chrome_options.add_argument("--headless")
        
    #     chrome_options.add_argument("--disable-dev-shm-usage")
    #     chrome_options.add_argument("--no-sandbox")
    #     chrome_service = ChromeService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    #     browser = webdriver.Chrome(options=chrome_options, service=chrome_service)
    #     time.sleep(2)
    #     wait = WebDriverWait(browser, 10)
    #     browser.get('https://news.ycombinator.com/')
    #     time.sleep(10)
    #     element_list = wait.until(
    #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title > a"))
    #     )

    #     browser.quit()        
    # except Exception as err:
    #     print(f"2b. Exception akjasim as {err}")        
        
    time.sleep(10)        
    # form_recaptcha_mail = RechaptchaMailForm()
    # context["form_recaptcha_mail"] = form_recaptcha_mail
    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name
    context["test_word"] = "test-word"
    if len(list_elements) > 0:
        context["list_elements"] = list_elements[0]
    else:    
        context["list_elements"] = "NO title No url"
         
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
        # if Book.objects.filter(owner__id=r_user.id):
        #     global books_user
        #     books_user = Book.objects.filter(owner__id=r_user.id)
        #     context['books_user'] = books_user
        #     for book_user in books_user:
        #         user_recs.append((f'"{book_user.title}", "{book_user.author}"'))

        #     # user_books = Book.objects.filter(owner__id=user.id).values_list('title', 'author')    
        #     # print('user_books', list(user_books))
        #     return Response(context, template_name='index_home.html', )
        # elif not Book.objects.filter(owner__id=r_user.id):
        #     messages.info(request, "You haven't any own books yet here")
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

    # author_book_docer_full = "Ernest Hemingway"
    # author_book_docer = author_book_docer_full.split()[-1]


    return Response(context, template_name='index_home.html', )
    # return render(request, 'index.html', context)


# book_id=4
# book = Book.objects.filter(pk=book_id).first()
# print()
# print("book =", book)
# book_values = Book.objects.filter(pk=book_id).values()[0]
# print()
# print("book_values =", book_values)
# book_values_list = Book.objects.filter(pk=book_id).values_list()[0]
# print()
# print("book_values_list =", book_values_list)
# print()
# book_title = Book.objects.filter(pk=book_id).values_list("title")[0][0]

# book_id=22
# book_title = Book.objects.filter(pk=book_id).values_list("title")[0][0]
# print("book_title =", book_title)
# try:
#     books_no = Book.objects.filter(author_c__isnull=True)
#     books_no_id = [book_no.id for book_no in books_no]
#     for book_no in books_no:
#         if Author.objects.filter(last_name=book_no.surname):
#             author_class = Author.objects.filter(last_name=book_no.surname).last()    
#             book_no.author_c = author_class
#             book_no.save()
#             # print('yes')
#         elif not Author.objects.filter(last_name=book_no.surname):
            
#             print('no author_c for', book_no.surname)
# except Exception as e:
#     print(f'bookmain exception: {e}')



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
    # context = context_main
    context_mainsite_views()    
    context = context_mainsite_views.context_main
    # return Response(context, template_name='page-404.html', )
    return render(request, "page-404.html", context)

# @api_view(['GET'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer,JSONRenderer])
def custom_error_view(request, exception=None):
    # context = context_main
    context_mainsite_views()    
    context = context_mainsite_views.context_main
    # return Response(context, template_name='page-500.html', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return render(request, "page-500.html", context)


# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
def custom_permission_denied_view(request, exception=None):
    # context = context_main
    context_mainsite_views()
    context = context_mainsite_views.context_main
    # return Response(context, template_name='page-403.html', )
    return render(request, "page-403.html", context)

# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
def custom_bad_request_view(request, exception=None):
    # context = context_main
    context_mainsite_views()    
    context = context_mainsite_views.context_main
    # return Response(context, template_name='page-400.html', )
    return render(request, "page-400.html", context)

def custom_unauthorized_view(request, exception=None):
    # context = context_main
    context_mainsite_views()    
    context = context_mainsite_views.context_main
    # return Response(context, template_name='page-400.html', )
    return render(request, "page-401.html", context)
    
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from booksmart.api.serializers import BookTestSerializer, BookPdfUrlSerializer
# pdf_url = "https://book_secret_url"
# pdf_search_url = "https://search_book_secret_url"
# pdf_filename = "Book secret filename"
# book_id = 4
# book_found = Book.objects.filter(pk=book_id).values()[0]
# book_found = Book.objects.filter(pk=book_id).first()
# data = { 
#         "url_pdf": pdf_url,
#         "url_pdf_search": pdf_search_url,
#         "pdf_search_filename": pdf_filename
# }
# serializer = BookPdfUrlSerializer(book_found, data=data, partial=True)
# if serializer.is_valid():
#     serializer.save()
#     print("serializer.data =", serializer.data)

# book_serializer = BookTestSerializer(data=book_found)
# serializer = BookTestSerializer(book_serializer, data={'url_pdf': pdf_url, 'url_pdf_search': pdf_search_url, 'pdf_search_filename': pdf_filename}, partial=True)
# if serializer.is_valid():
#     serializer.save()
# serializer_book_found = BookPdfUrlSerializer(book_found, many=True)
# # serializer = BookTestSerializer(book_found, data={'url_pdf': pdf_url, 'url_pdf_search': pdf_search_url, 'pdf_search_filename': pdf_filename}, many=True)
# # serializer = BookTestSerializer(serializer_book_found, data={'url_pdf': pdf_url, 'url_pdf_search': pdf_search_url, 'pdf_search_filename': pdf_filename}, many=True, partial=True)
# # serializer.is_valid()
# serializer = BookPdfUrlSerializer(serializer_book_found, data={'url_pdf': pdf_url}, partial=True)

# if serializer.is_valid():
#     serializer.save()
# # serializer.url_pdf = pdf_url
# # serializer.url_pdf_search = pdf_search_url
# # serializer.pdf_search_filename = pdf_filename

# print(serializer_book_found.initial_data)

# book_id = 4
# book_found = Book.objects.filter(pk=book_id).first()
# print("book_found.title =", book_found.title)


