import os, re, json, time, requests, datetime, random
from os import environ
from booksmart.models import url_img, url_img_author, Book, Author, BackgroundPoster, BackgroundVideo
from booksmart.forms import BookForm, AuthorForm, SearchRecord, BookChange, ItemsSearchForm, LibrarySearch, BackgroundFormPoster, BackgroundFormVideo
from accounts.models import Account
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer, HTMLFormRenderer #, IsOwnerIsAdminOrReadOnly
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny, IsAuthenticatedOrReadOnly
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from accounts.views_authorization import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.generics import UpdateAPIView

from rest_framework.exceptions import APIException
from rest_framework.authtoken.views import ObtainAuthToken

from django.utils.html import format_html
from booksmart.read_book import *


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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def read_book(request, id):

    formlib = LibrarySearch(request.GET)
    book = get_object_or_404(Book, pk=id)

    r_user = request.user
    current_url_name = request.path
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['num_authors'] = num_authors
    context['num_books'] = num_books    

    context['book'] = book

    keyword_field = {}

    logs = [('booksmart01@hotmail.com', 'Djangoapp01o'), ('booksmart02@hotmail.com', 'Djangoapp02o'), ('booksmart03@hotmail.com', 'Djangoapp03o')]
    log = random.choice(logs)
    # print('log', log)

    context['mail'] = log[0]
    context['pass'] = log[1]
    return Response(context, template_name='read_book.html', )
    # return render(request, "read_book.html", context )


# @api_view(['GET', 'POST'])
# # @authentication_classes([])
# @renderer_classes([TemplateHTMLRenderer, JSONRenderer])
# @permission_classes([permissions.IsAuthenticated, ])



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def new_book(request):
    r_user = request.user
    current_url_name = request.path

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context_a = context_main

    context_a['num_authors'] = num_authors
    context_a['num_books'] = num_books

    context_a['current_url'] = current_url_name

    if not r_user.is_authenticated:
        return redirect('index')

    form_new_book = BookForm(request.POST or None, request.FILES or None)

    if form_new_book.is_valid():
        newbook = form_new_book.save(commit=False)
        owner = Account.objects.filter(id=r_user.id).first()
       
        newbook.user_num_b = r_user.id
        newbook.owner = owner
        newbook.save()
        # book.save()
        # form_book = BookForm()
        return redirect('booksmart:allrecords')
    
    context_a['form_newbook'] = form_new_book
    context_a['new'] = True
    # return render(request, 'new_book.html', context_a)
    return Response(context_a, template_name='new_book.html', )


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def edit_book(request, id):
    r_user = request.user

    editbook = get_object_or_404(Book, pk=id)

    current_url_name = request.path

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context_a = context_main

    context_a['num_authors'] = num_authors
    context_a['num_books'] = num_books
    context_a['current_url'] = current_url_name
  
    form_edit_book = BookForm(request.POST or None, request.FILES or None, instance=editbook)

    context_a['book'] = editbook
    context_a['user_book_id'] = editbook.user_num_b
    # if request.method == "POST":
    if form_edit_book.is_valid() and request.method == "POST":    
        if r_user.id == editbook.user_num_b:
        # if user == book.owner:
            editbook = form_edit_book.save(commit=False)
            editbook.save()
            return redirect('booksmart:allrecords')
        elif r_user.id != editbook.user_num_b:
            time.sleep(7)
            return redirect('logout')
    context_a['form_editbook'] = form_edit_book
    context_a['new'] = False
    # return render(request, 'edit_book.html', context_a)

    if editbook.published:
        b_p = str(editbook.published)
        book_published = f"{b_p[8:10]}/{b_p[5:7]}/{b_p[0:4]}"
        # context_a['book_published'] = book_published
        context_a['book_published'] = editbook.published
        # print("date published:", book_published)
    else:
        print("NO date published")

    return Response(context_a, template_name='edit_book.html', )
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def delete_book(request, id):

    r_user = request.user
    book = get_object_or_404(Book, pk=id)

    current_url_name = request.path

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context_a = context_main

    context_a['num_authors'] = num_authors
    context_a['num_books'] = num_books

    context_a['book'] = book
    # user_add = BookChange(request.GET)
    # if user_add.is_valid():
    if request.method == "POST":
        if r_user.id == book.user_num_b:
        # if user == book.owner:
            book.delete()
            return redirect('booksmart:allrecords')
        else:
            time.sleep(7)
            return redirect('logout')
    # else:
    #     return redirect('account')

    # return render(request, 'submit.html', context_a)
    return Response(context_a, template_name='delete_book.html', )


# def new_author(request):
#     form_author_c = AuthorForm(request.POST or None, request.FILES or None)
#     if form_author_c.is_valid():
#         author_c = form_author_c.save(commit=False)
#         author_c.save()
#         return redirect('allauthors')
#     return render(request, 'new_author.html', {"form_author_c": form_author_c, 'new': True})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def new_author(request):

    r_user = request.user
    current_url_name = request.path
    form_new_author = AuthorForm(request.POST or None, request.FILES or None)

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name    
    
    if form_new_author.is_valid():
        newauthor = form_new_author.save(commit=False)
        newauthor.owner = r_user
        newauthor.save()
        newauthor.user_num_a = r_user.id
        newauthor.save()

        return redirect('booksmart:allauthors')

    context['form_newauthor'] = form_new_author
    context['new'] = True
    # return render(request, 'new_author.html', context)
    return Response(context, template_name='new_author.html', )
    


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def edit_author(request, id):

    r_user = request.user
    current_url_name = request.path

    editauthor = get_object_or_404(Author, pk=id)

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context_a = context_main

    context_a['num_authors'] = num_authors
    context_a['num_books'] = num_books
    context_a['current_url'] = current_url_name

    form_edit_author = AuthorForm(request.POST or None, request.FILES or None, instance=editauthor)

    end_date = editauthor.date_of_death
    end_life = end_date.strftime('%m/%d/%Y')
    context_a['endlife'] = end_life
    
    context_a['author_c'] = editauthor
    # book = get_object_or_404(Book, id=pk)
    
    if form_edit_author.is_valid() and request.method == "POST":
        if r_user.id == editauthor.user_num_a:
        # if user == author_c.owner:
            editauthor = form_edit_author.save(commit=False)
            editauthor.save()
            return redirect('booksmart:allauthors')
        elif r_user.id != editauthor.user_num_a:
        # elif user != author_c.owner:
            time.sleep(7)
            return redirect('logout')

    # if request.method == "POST":
    #     if user.id == author_c.user_num_a:    
    #         author_c = form_author_c.save(commit=False)
    #         author_c.save()
    #         return redirect('allauthors')

        # else:
        # form_author_c = AuthorForm(instance=author_c)
            # time.sleep(7)
            # return redirect('logout')

    context_a['form_editauthor'] = form_edit_author
    context_a['new'] = False

    # return render(request, 'edit_author.html', context_a)
    return Response(context_a, template_name='edit_author.html', )

# def delete_author(request, id):
#     author = get_object_or_404(Author, pk=id)

#     if request.method == "POST":
#         author.delete()
#         return redirect('allauthors')

#     return render(request, 'submita.html', {'author': author})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def delete_author(request, id):
    r_user = request.user
    current_url_name = request.path    

    author_c = get_object_or_404(Author, pk=id)

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context_a = context_main

    context_a['num_authors'] = num_authors
    context_a['num_books'] = num_books
    context_a['current_url'] = current_url_name    


    context_a['author_c'] = author_c

    if request.method == "POST":
        if r_user.id == author_c.user_num_a:
        # if user == author_c.owner:
            author_c.delete()
            return redirect('booksmart:allauthors')
        else:
            time.sleep(7)
            return redirect('logout')
    
    return Response(context_a, template_name='delete_author.html', )


def lr_registration_view(request):  
    r_user = request.user
    current_url_name = request.path

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name

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

    return redirect('/')
    # return render(request, c_path, context)



def lr_login_view(request):
    
    r_user = request.user
    current_url_name = request.path

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name

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

    context['login_form'] = form

    return redirect("/")
    # return render(request, c_path, context)
    # return HttpResponse("snippets/log_reg.html", context)

def lr_account_view(request):
    r_user = request.user
    current_url_name = request.path

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name
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
    
    # return HttpResponse(content_a) 
    return redirect("/") 
    # return render(request, 'account_copy.html', context)


def lr_logout_view(request):
	logout(request)
	return redirect('/')


