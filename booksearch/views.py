import os, requests, json, re, datetime
from django.shortcuts import render, get_object_or_404, redirect
from booksearch.forms import BookSearch
from booksmart.models import url_img, url_img_author, Book, Author, BackgroundPoster, BackgroundVideo, BackgroundMusic #, context_bm_m
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

def context_bm_booksearch_views():
    context_main = {}

    context_main['no_date'] = datetime.date(3000, 1, 1)
    # context_main['no_date_start'] = datetime.date(3000, 1, 1)
    # context_main['no_date_end'] = datetime.date(3000, 1, 1)
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
    except Exception as err:
        print(f"book_download_pm no Book.objects.all(): except Exception as {err}")
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
        print(f"book_download_pm no Author.objects.all(): Exception as {err}")
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
        print(f"book_download_pm Author.objects.all(): except Exception as {err}")
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
        print(f"book_download_pm BackgroundVideo.objects.filter().last(): except Exception as {err}")
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
        print(f"book_download_pm BackgroundMusic.objects.filter().last(): except Exception as {err}")
        context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_main['music_type_1'] = "mp3"
        context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_main['music_type_2'] = "mp3"
        
    context_bm_booksearch_views.context_main = context_main
    return context_main 


@api_view(['GET', 'POST'])
@permission_classes([])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer])
def gbsearch_book(request):
    context_bm_booksearch_views()
    context = context_bm_booksearch_views.context_main
    r_user = request.user
    form = BookSearch()

    current_url_name = request.path

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    # context = context_main
    context['num_authors'] = num_authors
    context['num_books'] = num_books

    context['current_url'] = current_url_name
    
    context['form'] = form
    return Response(context, template_name='gbsearch_book.html', )   


  
