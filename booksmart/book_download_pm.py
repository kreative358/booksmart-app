# # from .views_acc import *
from accounts.models import Account, MyAccountManager
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from booksmart.models import url_img, url_img_author, Book, Author, BackgroundPoster, BackgroundVideo, BackgroundMusic
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
from accounts.views_authorization import *

from rest_framework import filters as base_filters

import datetime

from django.utils.text import slugify

from booksmart.search_download_gs import SearchRequestGS
from booksmart.search_download_is import SearchRequestIS
from booksmart.search_download_pm import SearchRequestPM
from bs4 import BeautifulSoup

def context_book_download_pm():
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
        
    context_book_download_pm.context_main = context_main
    return context_main 

MIRROR_SOURCES = ["GET", "Cloudflare", "IPFS.io", "Infura"]
MIRROR_SOURCES_GET = ["GET"]

class LibgenSearchPM:
    def search_title(self, query):
        search_request = SearchRequestPM(query, search_type="title")
        return search_request.aggregate_request_data()

    def search_author(self, query):
        search_request = SearchRequestPM(query, search_type="author")
        return search_request.aggregate_request_data()

    def search_title_filtered(self, query, filters, exact_match=True):
        search_request = SearchRequestPM(query, search_type="title")
        results = search_request.aggregate_request_data()
        filtered_results = filter_resultsPM(
            results=results, filters=filters, exact_match=exact_match
        )
        return filtered_results

    def search_author_filtered(self, query, filters, exact_match=True):
        search_request = SearchRequestPM(query, search_type="author")
        results = search_request.aggregate_request_data()
        filtered_results = filter_resultsPM(
            results=results, filters=filters, exact_match=exact_match
        )
        return filtered_results

    def resolve_download_links(self, item):
        
        mirror_1 = item["Mirror_1"]
        page = requests.get(mirror_1)
        soup = BeautifulSoup(page.text, "html.parser")
        
        links = soup.find_all("a", string=MIRROR_SOURCES_GET)
        download_links = {link.string: link["href"] for link in links}
        
        # print(f"\n1. download_links = {download_links}\n")
        # links = soup.find_all("a", string=MIRROR_SOURCES)
        # download_links = {link.string: link["href"] for link in links}
        return download_links

    def resolve_download_links_my(self, item):
        
        mirror_1 = item["Mirror_1"]
        page = requests.get(mirror_1)
        soup = BeautifulSoup(page.text, "html.parser")
        
        links = soup.find_all("a", string=MIRROR_SOURCES_GET)
        download_links = {link.string: link["href"] for link in links}
        
        print(f"\n1. download_links = {download_links}\n")
        # links = soup.find_all("a", string=MIRROR_SOURCES)
        # download_links = {link.string: link["href"] for link in links}
        return download_links

def filter_resultsPM(results, filters, exact_match):
    """
    Returns a list of results that match the given filter criteria.
    When exact_match = true, we only include results that exactly match
    the filters (ie. the filters are an exact subset of the result).

    When exact-match = false,
    we run a case-insensitive check between each filter field and each result.

    exact_match defaults to TRUE -
    this is to maintain consistency with older versions of this library.
    """

    filtered_list = []
    if exact_match:
        for result in results:
            # check whether a candidate result matches the given filters
            if filters.items() <= result.items():
                filtered_list.append(result)

    else:
        filter_matches_result = False
        for result in results:
            for field, query in filters.items():
                if query.casefold() in result[field].casefold():
                    filter_matches_result = True
                else:
                    filter_matches_result = False
                    break
            if filter_matches_result:
                filtered_list.append(result)
    return filtered_list



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def download_bookPM(request):

    # book = get_object_or_404(Book, pk=id)
    # print("formlib_download:", formlib_download)
    r_user = request.user
    current_url_name = request.path
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    context_book_download_pm()
    context = context_book_download_pm.context_main
    title_download = ""
    context["title_download"] = ""
    context["title_read_last_chance"] = ""
    context['num_authors'] = num_authors
    context['num_books'] = num_books    

    formlib_download = BookDownload(request.GET)

    links_to_download = []
    s = LibgenSearchPM()
    # if request.method == "POST":
    #     if request.POST.get('title_download_search', False):

    # results = s.search_title("Harry Potter i zakon feniksa")
    # print('results', results)

    if formlib_download.is_valid():
        title_download=formlib_download.cleaned_data['title_download_search']
        print("1. title_download", title_download)
        context["title_download"] = title_download
        title_docer_pdf = title_download.replace(" ", "+")
        context["title_read_last_chance"] = f"https://docer.pl/show/?q={title_docer_pdf}&ext=pdf" 
        results = s.search_title(title_download)

        if results:
            try:
                items_to_download = results
                pdf_links = [s.resolve_download_links(item_to_download) for item_to_download in items_to_download if item_to_download["Ext."] == "pdf"] 
                if pdf_links:

                    print("pdf_links", pdf_links)
                    context["pdf_links"] = pdf_links
                    context["len_pdf_links"] = len(pdf_links)
                    
                    pdf_links_id = [[pdf_links.index(pdf_link), pdf_link] for pdf_link in pdf_links]
                    context["pdf_links_id"] = pdf_links_id

                    if len(pdf_links) >= 2:
                        download_links_1a = pdf_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        print("download_links_1a =", download_links_1a)
                        context["download_links_1a"] = download_links_1a
                        download_links_2a = pdf_links[1]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        context["download_links_2a"] = download_links_2a
                        print("download_links_2a =", download_links_2a)

                        return Response(context, template_name='download_book_pm.html',)

                    elif len(pdf_links) == 1:
                        download_links_1a = pdf_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        context["download_links_1a"] = download_links_1a

                        return Response(context, template_name='download_book_pm.html',)

                else:
                    context["message_read_download"] = "This book is probably not available for download in pdf, below is the last chance for those who persevere"
                    # print("2. title_download", title_download)
                    # title_slugify = slugify(title_download).replace(" ", "+").replace(" ", "-")

                    return Response(context, template_name='download_book_pm.html',)

            except Exception as e:
                context["message_read_download"] = f"This book is probably not available for download in pdf, reason: {e}"
                # print("3. title_download", title_download)
                return Response(context, template_name='download_book_pm.html',)

        else:
            # print("4. title_download", title_download)
            context["message_read_download"] = "This book is probably not available for download in pdf, below is the last chance for those who persevere."
            return Response(context, template_name='download_book_pm.html',)

    # if request.POST:
    #     formlib_download = LibrarySearch(request.POST)
    #     print("2. formlib_download", formlib_download)
    #     return Response(context, template_name='download_book.html', )
    #     results = s.search_title(formlib_download)
    #     if len(results) == 0:
    #         return Response(context, template_name='download_book.html', )
        
    #     elif len(results) >= 1:
    #         if len(results) == 1:
    #             try:
    #                 item_to_download_1 = results[0]
    #                 download_links_1 = s.resolve_download_links(item_to_download_1)
    #                 download_links_1a = download_links_1["GET"].replace("get.php", "https://libgen.pm/get.php")
    #                 links_to_download.append(download_links_1a)

    #             except Exception as e:
    #                 context["message_read_download"] = f"probably there is no this book to download, reason: {e}"
    #                 return Response(context, template_name='download_book.html', )
    #         elif len(results) > 1:
    #     # print(f"download_links_1a = {download_links_1a}")
    #     # print("results:", results)
    #             try:
    #                 item_to_download_2 = results[1]
    #                 download_links_2 = s.resolve_download_links(item_to_download_2)
    #                 download_links_2a = download_links_2["GET"].replace("get.php", "https://libgen.pm/get.php")
    #                 links_to_download.append(download_links_2a)
    #             except Exception as e:
    #                     context["message_read_download"] = f"probably there is only one book to download, reason: {e}"
    #             # print(f"download_links_2a = {download_links_2a}")
    #     context["links_download"] = links_to_download
    #     return Response(context, template_name='download_book.html', )
    context["search_title_download"] = BookDownload()
    return Response(context, template_name='download_book_pm.html', )