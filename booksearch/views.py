from django.shortcuts import render, get_object_or_404, redirect
from booksearch.forms import BookSearch
from booksmart.models import url_img, url_img_author, Book, Author, context_bm #, BackgroundPoster, BackgroundVideo
import os, requests, json, re, datetime
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.authentication import TokenAuthentication
from accounts.views_authorization import *
from accounts.api.views import AccountViewSet, UserDetailViewSet, UserViewSet
from booksmart.api.views import BooksEditViewSet, AuthorViewSet, BooksFullViewSet


import datetime

context_bm = {}
context_list = []

context_bm['no_date'] = datetime.date(3000, 1, 1)
context_bm['url_img_book'] = url_img
context_bm['url_img_author'] = url_img_author

try:
    if Book.objects.all():
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

@api_view(['GET', 'POST'])
@permission_classes([])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer])
def gbsearch_book(request):
    r_user = request.user
    context = context_bm
    form = BookSearch()

    # form_a = a_account_view(request)
    # #form_out = a_logout_view(request)
    # form_r = a_registration_view(request)
    # form_l = a_login_view(request)

    # # user = request.user
    # # context['user_form'] = user
    
    # #context['logout_form'] = form_out
    # context['login_form'] = form_l
    # context['registration_form'] = form_r
    # context['account_form'] = form_a

    current_url_name = request.path

    # poster = BackgroundPoster.objects.last()
    # video = BackgroundVideo.objects.last()
    # context['poster_url'] = poster
    # context['video_url'] = video

    context['current_url'] = current_url_name
    
    context['form'] = form
    return Response(context, template_name='gbsearch_book.html', )   


# from internetarchive import get_item
# item = get_item('harrypotterdeath0000rowl_n2u6')
# print('item.exists', item.exists)   
  
