import os, requests, json, re, datetime, requests.api
from accounts.models import Account, MyAccountManager
from booksmart.forms import BookForm, AuthorForm, SearchRecord, BooksAuthor, UrlPathForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import resolve, reverse_lazy
from django.contrib import messages
from django.db.models import Q, ObjectDoesNotExist
from django.core.paginator import Paginator
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, View, UpdateView

from django.http import HttpResponse, HttpResponseRedirect

from django.utils import timezone

from django.template.response import TemplateResponse
from django.template import loader
from django.db.models.query import QuerySet
from django.views.decorators.cache import cache_control
from django.contrib.auth.mixins import LoginRequiredMixin

from booksmart.api.serializers import BookSerializer, AuthorSerializer

# from booksmart.filters import FilterBook #, FilterBookTest 
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, UrlPathForm, SearchRecord

from rest_framework.response import Response
from rest_framework import viewsets, views
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from booksmart.models import Book, Author, BackgroundPoster, BackgroundVideo, BackgroundMusic, url_img, url_img_author#, context_bm_models
import datetime

def context_bm_models():    
    print("views_test_auth context_bm_models()")
    context_bm = {}
    context_list = []

    context_bm['no_date'] = datetime.date(3000, 1, 1)
    context_bm['url_img_book'] = url_img
    context_bm['url_img_author'] = url_img_author

    try:
        if Book.objects.all().count() > 0:
        # if Book.objects.filter().all():
            # all_books = Book.objects.all()
            # context_list.append(all_books)
            num_books = Book.objects.all().count()
            # context_bm['allbooks'] = all_books
            context_bm['num_books'] = num_books
        elif Book.objects.all().count() == 0:
        # elif not Book.objects.filter().all():
            # context_bm['allbooks'] = None
            context_bm['num_books'] = 0
    except Exception as err:
        print(f"booksmart models 335 no Book.objects.all(): except Exception as {err}")
        context_bm['allbooks'] = None
        context_bm['num_books'] = 0  

    try:
        if Author.objects.all().count() > 0:
        # if Author.objects.filter().all():
            # all_authors = Author.objects.all()
            # context_list.append(all_authors)
            num_authors = Author.objects.all().count()
            # context_bm['allauthors'] = all_authors
            context_bm['num_authors'] = num_authors
        elif Author.objects.all() == 0:
        #elif not Author.objects.filter().all():
            # context_bm['allauthors'] = None
            context_bm['num_authors'] = 0
    except Exception as err:
        print(f"booksmart models 351 no Author.objects.all(): Exception as {err}")
        context_bm['allauthors'] = None
        context_bm['num_authors'] = 0

    try:
        if BackgroundPoster.objects.filter().last():
            poster = BackgroundPoster.objects.filter().last()
            context_bm['poster_url_1'] = poster.link_poster_1
            context_bm['poster_url_2'] = poster.link_poster_2
        elif not BackgroundPoster.objects.filter().last():
            context_bm['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
            context_bm['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
    except Exception as err:
        print(f"booksmart models 367 no BackgroundPoster.objects.filter().last(): Exception as {err}")
        context_bm['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
        context_bm['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"

    try:
        if BackgroundVideo.objects.filter().last():   
            video = BackgroundVideo.objects.filter().last()
            context_bm['video_url'] = video.link_video
            context_bm['video_type'] = video.type_video
        elif not BackgroundVideo.objects.filter().last():
            context_bm['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
            context_bm['video_type'] = "mp4"
    except Exception as err:
        print(f"booksmart models no BackgroundVideo.objects.filter().last(): Exception as {err}")
        context_bm['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
        context_bm['video_type'] = "mp4"

    try:
        if BackgroundMusic.objects.filter().last():   
            music = BackgroundMusic.objects.filter().last()
            context_bm['music_url_1'] = music.link_music_1
            context_bm['music_type_1'] = music.type_music_1
            context_bm['music_url_2'] = music.link_music_2
            context_bm['music_type_2'] = music.type_music_2
        elif not BackgroundMusic.objects.filter().last(): 
            context_bm['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
            context_bm['music_type_1'] = "mp3"
            context_bm['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
            context_bm['music_type_2'] = "mp3"
    except Exception as err:
        print(f"booksmart models 400 BackgroundMusic.objects.filter().last(): except Exception as {err}")    
        context_bm['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_bm['music_type_1'] = "mp3"
        context_bm['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_bm['music_type_2'] = "mp3"
    
    context_bm_models.context_bm = context_bm
    # context_bm = context_bm_models.copy()
    return context_bm

class ObtainAuthTokenView(APIView):

    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'
    # context_serializer = context_bm_models.context_bm
    def get(self, request):
        # serializer = LoginSerializer()
        # context = self.context_serializer
        context_bm_models()
        context = context_bm_models.context_bm
        return Response(context, template_name='login.html')
    def post(self, request):
        context_bm_models()
        context = context_bm_models.context_bm

        email = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(email=email, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)

            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = email
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'

        return Response(context,)
# @login_required(login_url="/loginn")
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def backend(request):
#     return render(request, "backend.html")

# class frontend(TemplateView):
#     template_name = 'frontend.html'

# class backend(LoginRequiredMixin, TemplateView):
#     template_name = 'backend.html'
#     login_url = '/loginn/'

# def Login(request):
#     if request.user.is_authenticated:
#         # return redirect("/")
#         return render(request, "backend.html")
#     else: 
#         messages.info(request, "Please login to access this page")
#         return HttpResponseRedirect("/")

# def LoginUser(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username = username, password = password)
#         if user != None:
#             login(request, user)
#             return HttpResponseRedirect("/backend")
#         else:
#             messages.error(request, "Enter your data correctly")
#             return HttpResponseRedirect("/")

# def Logout(request):
#     logout(request)
#     request.user = None
#     return HttpResponseRedirect("/")


def registration_view(request):
    context_bm_models()    
    context = context_bm_models.context_bm
    
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('/')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    # return HttpResponse(content_a) 
    # return redirect("/", content_a) 
    return render(request, 'register.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')

def login_view(request):
    context_bm_models()
    context = context_bm_models.context_bm
    r_user = request.user
    if r_user.is_authenticated:
        return redirect("index")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            r_user = authenticate(email=email, password=password)

            if r_user:
                login(request, r_user)
                return redirect("index")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, 'login.html', context)

def account_view(request):
    context_bm_models()    
    context_a = context_bm_models.context_bm    
    r_user = request.user
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    all_books = Book.objects.all()
    all_authors = Author.objects.all()
    search_form = SearchRecord()
    
    context_a['allbooks'] = all_books
    context_a['allauthors'] = all_authors
    context_a['num_books'] = num_books
    context_a['num_authors'] = num_authors
    context_a['search_form'] = search_form


    # authors_add = Author.objects.filter(user_add=request.user)
    # books_add = Book.objects.filter(user_add=request.user)
    authors_add = Author.objects.filter(user_num_a=r_user.id)
    books_add = Book.objects.filter(user_num_b=r_user.id)
    context_a['authors_add'] = authors_add
    context_a['books_add'] = books_add

    paginator = Paginator(books_add, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context_a['page_obj'] = page_obj

    return render(request, 'account.html', context_a)

# def account_view(request):
#     num_books = Book.objects.all().count()
#     num_authors = Author.objects.all().count()
#     all_books = Book.objects.all()
#     all_authors = Author.objects.all()
#     context_a
    
#     context_a['allbooks'] = all_books
#     context_a['allauthors'] = all_authors
#     context_a['num_books'] = num_books
#     context_a['num_authors'] = num_authors

#     if not request.user.is_authenticated:
#         return redirect("index")

#     if request.POST:
#         form = AccountUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             context['success_message'] = "update successfully"
#     else:
#         form = AccountUpdateForm(
#             initial={
#                 "email": request.user.email,
#                 "username": request.user.username,
#             }
#         )
#     context['account_form'] = form

#     # authors_add = Author.objects.filter(user_add=request.user)
#     # books_add = Book.objects.filter(user_add=request.user)
#     authors_add = Author.objects.filter(user_num_a=request.user.id)
#     books_add = Book.objects.filter(user_num_b=request.user.id)
#     context['books_add'] = books_add

#     paginator = Paginator(books_add, 10)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)
#     context['page_obj'] = page_obj

#     return render(request, 'account.html', context)


def lr_registration_view(request):  
    # c_path = cur_path[1:-1]+".html"
    # print('c_path', c_path)
    context_bm_models()     
    context = context_bm_models.context_bm
    r_user = request.user
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('/')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form

    # content_rr = context['registration_form']
    # content_r = f"{context['registration_form']}"
    
    # return HttpResponse(content_l) 
    # return redirect("/", content_l) 
    return redirect('/')
    # return render(request, c_path, context)


# def current(request):
#     path = get_current_site(request)
#     print('path', path)
#     path1 = get_current_site(request)
#     print('path1', path1)
#     path2 = request.path
#     print('path2', path2)
#     path3 = request.get_host() + request.path
#     print('path3', path3)
#     if author_form.is_valid():
#         values=author_form.cleaned_data['author']
#         print(values, type(values))

# def urlpath(request):
#     context = {}
#     print(request.method)
    
#     form_url = UrlPathForm()
#     print(form_url)
    # if form_url.is_valid():
    #     values=form_url.cleaned_data['url_path']
    #     print(values, type(values))
        

    #     context['values'] = values
    # print(str(context['values']))  
    # print('1', curent)
    # path = get_current_site(request)
    # print('path', path)
    # path1 = get_current_site(request)
    # print('path1', path1)
    # path2 = request.path
    # print('path2', path2)
    # path3 = request.get_host() + request.path
    # print('path3', path3)
    # value= request.GET['value']
    # print(value)
        
    # return render(request, "urlpath.html", {'formurl':form_url})
    

# if currents:
#     print('if currents:',currents)


def lr_login_view(request):
    context_bm_models()     
    # print('login currents', currents)
    # cur_path = currents[-1][11:-1]
    # print('login cur_path', cur_path)
    # c_path = cur_path+".html"
    # print('c_path', c_path)
    context = context_bm_models.context_bm
    r_user = request.user
    form_url = UrlPathForm()
    # print('2', form_url)
    if r_user.is_authenticated:
        return redirect("/")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            r_user = authenticate(email=email, password=password)

            if r_user:
                login(request, r_user)
                return redirect("/")

    else:
        form = AccountAuthenticationForm()

    # path = request.path
    # print('path_l', path)
    # path1 = get_current_site(request)
    # print('path1_l', path1)
    # path2 = request.path
    # print('path2_l', path2)
    # path3 = request.get_host() + request.path
    # print('path3_l', path3)

    context['login_form'] = form
    # form_url = UrlPathForm()
    # return HttpResponseRedirect(content_l) 
    #  render(request, 'booksmart.html', context)
    return redirect("/")
    # return render(request, c_path, context)
    # return HttpResponse("snippets/log_reg.html", context)

def lr_account_view(request):
    context_bm_models()     
    context = context_bm_models.context_bm
    r_user = request.user
    if not request.user.is_authenticated:
        return redirect("/")

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['success_message'] = "update successfully"
            return redirect("/")
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
           		"username": request.user.username,
            }
        )
    context['account_form'] = form
    # content_ar = context['account_form']
    # print(content)
    # content_a = f"{context['account_form']}"
    
    # return HttpResponse(content_a) 
    return redirect("/") 
   #  return render(request, 'account_copy.html', context)
    #return redirect("/")

def lr_logout_view(request):
	logout(request)
	return redirect('/')


