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
import os, time, requests, json, re, datetime, requests.api

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
from booksmart.api.serializers import BookPdfUrlSerializer
from slugify import slugify as text_slugify

# from booksmart.search_download_gs import SearchRequestGS
# from booksmart.search_download_gs import SearchRequestRS
# from booksmart.search_download_is import SearchRequestIS
# from booksmart.search_download_pm import SearchRequestPM, SearchRequestPM_my
from booksmart.search_download import SearchRequestRS, SearchRequestGS
from bs4 import BeautifulSoup
from booksmart.test_docer import book_scrap, book_scrap_ready
# from booksmart.docer_spoofer import *

Languages = {
    'en': 'English',
    'eo': 'Esperanto',
    'fr': 'French',
    'de': 'German',
    'pl': 'Polish',
    'pe': 'Portuguese',
    'es': 'Spanish',
    'uk': 'Ukrainian'
}    

context_main = {}

context_main['no_date'] = datetime.date(3000, 1, 1)
context_main['url_img_book'] = url_img
context_main['url_img_author'] = url_img_author

# try:
#     if Book.objects.all():
#     # if Book.objects.filter().all():
#         all_books = Book.objects.all()
#         # context_list.append(all_books)
#         num_books = Book.objects.all().count()
#         context_main['allbooks'] = all_books
#         context_main['num_books'] = num_books
#     elif not Book.objects.all():
#     # elif not Book.objects.filter().all():
#         context_main['allbooks'] = None
#         context_main['num_books'] = 0
# except Exception as err:
#     print(f"book_download: Book.objects.all() except Exception as {err}")
#     pass

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
    print(f"book_download: Author.objects.all(): except Exception as {err}")
    pass

try:
    if BackgroundPoster.objects.filter().last():
        poster = BackgroundPoster.objects.filter().last()
        context_main['poster_url_1'] = poster.link_poster_1
        context_main['poster_url_2'] = poster.link_poster_2
    elif not BackgroundPoster.objects.filter().last():
        context_main['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1FNl36zxhcZBXSbJdFB8V-4eWHoOIVHMl"
        context_main['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1FNl36zxhcZBXSbJdFB8V-4eWHoOIVHMl"
except Exception as err:
    print(f"book_download: Author.objects.all(): except Exception as {err}")
    pass

try:
    if BackgroundVideo.objects.filter().last():   
        video = BackgroundVideo.objects.filter().last()
        context_main['video_url'] = video.link_video
        context_main['video_type'] = video.type_video
    elif not BackgroundVideo.objects.filter().last():
        context_main['video_url'] = "https://drive.google.com/uc?export=download&id=1L52HH0GCbHoYH8ttJICj0P5iwg_sNTqz"
        context_main['video_type'] = "mp4"
except Exception as err:
    print(f"book_download: BackgroundVideo.objects.filter().last(): except Exception as {err}")
    pass

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
    print(f"book_download: BackgroundMusic.objects.filter().last(): except Exception as {err}")
    context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
    context_main['music_type_1'] = "mp3"
    context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
    context_main['music_type_2'] = "mp3"

MIRROR_SOURCES = ["GET", "Cloudflare", "IPFS.io", "Infura"]
MIRROR_SOURCE_GET = ["GET"]

class LibgenSearchRS:
    def search_title(self, query):
        search_request_rs = SearchRequestRS(query, search_type="title")
        return search_request_rs.aggregate_request_data()

    def search_author(self, query):
        search_request_rs = SearchRequestRS(query, search_type="author")
        return search_request_rs.aggregate_request_data()

    def search_title_filtered(self, query, filters, exact_match=True):
        search_request_rs = SearchRequestRS(query, search_type="title")
        results_rs = search_request_rs.aggregate_request_data()
        filtered_results_rs = filter_results_rs(
            results_rs=results_rs, filters=filters, exact_match=exact_match
        )
        print("search_title_filtered =", filtered_results_rs)
        return filtered_results_rs

    def search_author_filtered(self, query, filters, exact_match=True):
        search_request_rs = SearchRequestRS(query, search_type="author")
        results_rs = search_request_rs.aggregate_request_data()
        filtered_results_rs = filter_results_rs(
            results_rs=results_rs, filters=filters, exact_match=exact_match
        )
        return filtered_results_rs

    def resolve_download_links(self, item):
        mirror_1 = item["Mirrors"]
        print("\nmirror_1 =", mirror_1)
        # page = requests.get(f'https://libgen.pm{mirror_1}')
        # page = requests.get(f'https://libgen.rs{mirror_1}')
        page = requests.get(mirror_1)
        soup = BeautifulSoup(page.text, "html.parser")
        
        links = soup.find_all("a", string=MIRROR_SOURCES)
        download_links_rs = {link.string: link["href"] for link in links}
        
        print(f"\n1. download_links_rs = {download_links_rs}\n")

        return download_links_rs



def filter_results_rs(results_rs, filters, exact_match):
    """
    Returns a list of results that match the given filter criteria.
    When exact_match = true, we only include results that exactly match
    the filters (ie. the filters are an exact subset of the result).

    When exact-match = false,
    we run a case-insensitive check between each filter field and each result.

    exact_match defaults to TRUE -
    this is to maintain consistency with older versions of this library.
    """

    filtered_list_rs = []
    if exact_match:
        for result in results_rs:
            # check whether a candidate result matches the given filters
            if filters.items() <= result.items():
                filtered_list_rs.append(result)

    else:
        filter_matches_result = False
        for result in results_rs:
            for field, query in filters.items():
                if query.casefold() in result[field].casefold():
                    filter_matches_result = True
                else:
                    filter_matches_result = False
                    break
            if filter_matches_result:
                filtered_list_rs.append(result)
    print(f"\nfiltered_list = {filtered_list_rs}\n")
    return filtered_list_rs

def download_book_rs(book_download, context_rs): 
    # context_rs = {}

    search_libgen_rs = LibgenSearchRS()
    pdf_links_rs = []

    language = Languages[book_download["language"]]
    title = book_download["title"].replace(" ", "+")
    surname = book_download["surname"]
    results_rs = search_libgen_rs.search_title(title)

    if results_rs:
        print("results =", results_rs[:2])
        items_to_download = results_rs
        
        try:
            pdf_links_rs = [search_libgen_rs.resolve_download_links(item_to_download) for item_to_download in items_to_download if item_to_download["Extension"] == "pdf" and item_to_download["Language"] == language and surname in item_to_download["Author(s)"]] 
            
            if len(pdf_links_rs) > 0:

                print("1 pdf_links_rs", pdf_links_rs)
                context_rs["pdf_links"] = pdf_links_rs
                context_rs["len_pdf_links"] = len(pdf_links_rs)
                
                pdf_links_rs_id = [[pdf_links_rs.index(pdf_link_rs), pdf_link_rs] for pdf_link_rs in pdf_links_rs]
                context_rs["pdf_links_id"] = pdf_links_rs_id

                if len(pdf_links_rs) >= 2:
                    download_links_pdf_1a = pdf_links_rs[0]["GET"]
                    context_rs["download_links_1a"] = download_links_pdf_1a
                    context_rs["extension_1a"] = "pdf"
                    print("download_links_pdf_1a =", download_links_pdf_1a)
                    download_links_pdf_2a = pdf_links_rs[1]["GET"]
                    context_rs["download_links_2a"] = download_links_pdf_2a
                    context_rs["extension_2a"] = "pdf"
                    print("download_links_pdf_2a =", download_links_pdf_2a)

                elif len(pdf_links_rs) == 1:
                    download_links_1a = pdf_links_rs[0]["GET"]
                    context_rs["download_links_1a"] = download_links_1a
                    context_rs["extension_1a"] = "pdf"
                    print("download_links_pdf_1a =", download_links_pdf_1a)

            elif len(pdf_links_rs) == 0:
                print("elif len(pdf_links_rs) == 0:")
                context_rs["message_read_download"] = "This book is probably not available for download"
                
                try:
                    pdf_links_rs = [search_libgen_rs.resolve_download_links(item_to_download) for item_to_download in items_to_download if item_to_download["Extension"] == "epub" and item_to_download["Language"] == language and surname in item_to_download["Author(s)"]] 
                    
                    if len(pdf_links_rs) > 0:

                        print("1 pdf_links_rs", pdf_links_rs)
                        context_rs["pdf_links"] = pdf_links_rs
                        context_rs["len_pdf_links"] = len(pdf_links_rs)
                        
                        pdf_links_rs_id = [[pdf_links_rs.index(pdf_link_rs), pdf_link_rs] for pdf_link_rs in pdf_links_rs]
                        context_rs["pdf_links_id"] = pdf_links_rs_id

                        if len(pdf_links_rs) >= 2:
                            download_links_pdf_1a = pdf_links_rs[0]["GET"]
                            context_rs["download_links_1a"] = download_links_pdf_1a
                            context_rs["extension_1a"] = "epub"
                            print("download_links_pdf_1a =", download_links_pdf_1a)
                            download_links_pdf_2a = pdf_links_rs[1]["GET"]
                            context_rs["download_links_2a"] = download_links_pdf_2a
                            context_rs["extension_2a"] = "epub"
                            print("download_links_pdf_2a =", download_links_pdf_2a)

                        elif len(pdf_links_rs) == 1:
                            download_links_1a = pdf_links_rs[0]["GET"]
                            context_rs["download_links_1a"] = download_links_1a
                            context_rs["extension_1a"] = "epub"
                            print("download_links_pdf_1a =", download_links_pdf_1a)

                    elif len(pdf_links_rs) == 0:
                        print("elif len(pdf_links_rs) == 0:")
                        context_rs["message_read_download"] = "This book is probably not available for download"

                except Exception as e:
                    context_rs["message_read_download"] = "This book is probably not available for download in pdf or epub, or any other format."                

        except Exception as e:
            context_rs["message_read_download"] = "This book is probably not available for download in pdf or epub, or any other format."

    else:
        context_rs["message_read_download"] = "This book is probably not available for download in pdf or epub, below is the last chance for those who persevere."
    download_book_rs.context_rs_val = context_rs
    return context_rs


class LibgenSearchGS:
    def search_title(self, query):
        search_request_gs = SearchRequestGS(query, search_type="title")
        return search_request_gs.aggregate_request_data()

    def search_author(self, query):
        search_request_gs = SearchRequestGS(query, search_type="author")
        return search_request_gs.aggregate_request_data()

    def search_title_filtered(self, query, filters, exact_match=True):
        search_request_gs = SearchRequestGS(query, search_type="title")
        results_gs = search_request_gs.aggregate_request_data()
        filtered_results_gs = filter_results_gs(
            results_gs=results_gs, filters=filters, exact_match=exact_match
        )
        print("search_title_filtered =", filtered_results_gs)
        return filtered_results_gs

    def search_author_filtered(self, query, filters, exact_match=True):
        search_request_gs = SearchRequestGS(query, search_type="author")
        results_gs = search_request_gs.aggregate_request_data()
        filtered_results_gs = filter_results_gs(
            results_gs=results_gs, filters=filters, exact_match=exact_match
        )
        return filtered_results_gs

    def resolve_download_links(self, item):
        mirror_1 = item["Mirrors"]
        print("\nmirror_1 =", mirror_1)
        if "https://"in mirror_1:
            page = requests.get(mirror_1)
        else:    
            page = requests.get(f'https://libgen.gs{mirror_1}')
        # page = requests.get(f'https://libgen.rs{mirror_1}')
        # page = requests.get(mirror_1)
        soup = BeautifulSoup(page.text, "html.parser")
        
        links = soup.find_all("a", string=MIRROR_SOURCES)
        download_links_gs = {link.string: link["href"] for link in links}
        
        print(f"\n1. download_links_gs = {download_links_gs}\n")

        return download_links_gs



def filter_results_gs(results_gs, filters, exact_match):
    """
    Returns a list of results that match the given filter criteria.
    When exact_match = true, we only include results that exactly match
    the filters (ie. the filters are an exact subset of the result).

    When exact-match = false,
    we run a case-insensitive check between each filter field and each result.

    exact_match defaults to TRUE -
    this is to maintain consistency with older versions of this library.
    """

    filtered_list_gs = []
    if exact_match:
        for result in results_gs:
            # check whether a candidate result matches the given filters
            if filters.items() <= result.items():
                filtered_list_gs.append(result)

    else:
        filter_matches_result = False
        for result in results_gs:
            for field, query in filters.items():
                if query.casefold() in result[field].casefold():
                    filter_matches_result = True
                else:
                    filter_matches_result = False
                    break
            if filter_matches_result:
                filtered_list_gs.append(result)
    print(f"\nfiltered_list = {filtered_list_gs}\n")
    return filtered_list_gs


def download_book_gs(book_download, context_gs):
    pdf_links_gs = []
    print("0. pdf_links_gs =", pdf_links_gs)
    results_gs_list = []
    context_gs['num_authors'] = num_authors
    context_gs['num_books'] = num_books    
    book_to_download = Book.objects.filter(pk=book_download["id"]).first()
    links_to_download = []
    search_libgen_gs = LibgenSearchGS()
    title_row = book_download["title"]
    title = book_download["title"].replace(" ", "+")
    language = Languages[book_download["language"]]
    surname = book_download["surname"]
    short_surname = book_download["surname"][:3].lower()
    print(f"title: {title}, surname: {surname}, lanuage: {language}")
    results_gs = search_libgen_gs.search_title(title)
    # results_gs_list.append(results_gs)
    if results_gs:
        # print("1. results_gs[0] =", results_gs[0])
        # print("results_gs =", results_gs)
        # items_to_download = results_gs_list[-1]
        results_gs_start = results_gs.copy()
        try:
            items_to_download = results_gs_start.copy()
            print("items_to_download")
            pdf_links_gs = [
                search_libgen_gs.resolve_download_links(item_to_download)

                for item_to_download in items_to_download
                
                if item_to_download["Ext."] == "pdf" and item_to_download["Language"] == language and surname in item_to_download["Author(s)"] # and title_row in item_to_download["ID Time add Title Series"] 
                or 
                item_to_download["Ext."] == "pdf" and item_to_download["Language"] == language and short_surname in text_slugify(item_to_download["Author(s)"].lower(), separator=" ", lowercase=False, replacements=[['v', 'w'], ['zh', 'rz'], ['k', 'c'], ['kh', 'h']])[:4] # and title_row in item_to_download["ID Time add Title Series"]
                ]
             
            print("1. pdf_links_gs =", pdf_links_gs)

            if len(pdf_links_gs) > 0:
                context_gs["pdf_links"] = pdf_links_gs
                context_gs["len_pdf_links"] = len(pdf_links_gs)
                
                # pdf_links_gs_id = [[pdf_links_gs.index(pdf_link_gs), pdf_link_gs] for pdf_link_gs in pdf_links_gs]
                # context_gs["pdf_links_id"] = pdf_links_gs_id
                try:
                    serializer = BookPdfUrlSerializer(book_to_download, data={'url_libgen': pdf_links_gs[0]["GET"].replace("\\", "//")}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                except Exception as err:
                    print(f"1. serializer url_libgen Exception as {err}")
                    
                if len(pdf_links_gs) >= 2:
                    context_gs["download_links_1a"] = pdf_links_gs[0]["GET"].replace("\\", "//")
                    context_gs["extension_1a"] = "pdf"
                    context_gs["download_links_2a"] = pdf_links_gs[1]["GET"].replace("\\", "//")
                    context_gs["extension_2a"] = "pdf"

                elif len(pdf_links_gs) == 1:
                    # download_links_1a = pdf_links_gs[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                    context_gs["download_links_1a"] = pdf_links_gs[0]["GET"].replace("\\", "//")
                    context_gs["extension_1a"] = "pdf"

            elif len(pdf_links_gs) == 0:
                # results_gs = search_libgen_gs.search_title(title)
                # if results_gs:
                items_to_download_1 = results_gs_start.copy()
                print("2. items_to_download_1")
                
                pdf_links_gs = [
                    search_libgen_gs.resolve_download_links(item_to_download)

                    for item_to_download in items_to_download_1
                    
                    if item_to_download["Ext."] == "epub" and item_to_download["Language"] == language and surname in item_to_download["Author(s)"] 
                    or 
                    item_to_download["Ext."] == "epub" and item_to_download["Language"] == language and short_surname in text_slugify(item_to_download["Author(s)"].lower(), separator=" ", lowercase=False, replacements=[['v', 'w'], ['zh', 'rz'], ['k', 'c'], ['kh', 'h']])[:4]
                    ]
                
                print("2. pdf_links_gs =", pdf_links_gs)
                
                if len(pdf_links_gs) > 0:
                    
                    context_gs["pdf_links"] = pdf_links_gs
                    context_gs["len_pdf_links"] = len(pdf_links_gs)
                    
                    try:
                        serializer = BookPdfUrlSerializer(book_to_download, data={'url_libgen': pdf_links_gs[0]["GET"].replace("\\", "//")}, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                    except Exception as err:
                        print(f"1. serializer url_libgen Exception as {err}")                        

                    if len(pdf_links_gs) >= 2:
                        context_gs["download_links_1a"] = pdf_links_gs[0]["GET"].replace("\\", "//")
                        context_gs["extension_1a"] = "epub"
                        context_gs["download_links_2a"] = pdf_links_gs[1]["GET"].replace("\\", "//")
                        context_gs["extension_2a"] = "epub"

                    elif len(pdf_links_gs) == 1:
                        context_gs["download_links_1a"] = pdf_links_gs[0]["GET"].replace("\\", "//")
                        context_gs["extension_1a"] = "epub"
                        
                elif len(pdf_links_gs) == 0:
                    # if results_gs:
                    items_to_download_2 = results_gs_start.copy()
                    print("3. items_to_download_2")
                    pdf_links_gs = [
                        search_libgen_gs.resolve_download_links(item_to_download)

                        for item_to_download in items_to_download_2
                        
                        if item_to_download["Language"] == language and surname in item_to_download["Author(s)"] 
                        or 
                        item_to_download["Language"] == language and short_surname in text_slugify(item_to_download["Author(s)"].lower(), separator=" ", lowercase=False, replacements=[['v', 'w'], ['zh', 'rz'], ['k', 'c'], ['kh', 'h']])[:4]
                        ]
                    print()
                    print("3. pdf_links_gs =", pdf_links_gs)
                    print()
                    if len(pdf_links_gs) > 0:
                        context_gs["pdf_links"] = pdf_links_gs
                        context_gs["len_pdf_links"] = len(pdf_links_gs)

                        try:
                            serializer = BookPdfUrlSerializer(book_to_download, data={'url_libgen': pdf_links_gs[0]["GET"].replace("\\", "//")}, partial=True)
                            if serializer.is_valid():
                                serializer.save()
                        except Exception as err:
                            print(f"1. serializer url_libgen Exception as {err}")
                            
                        if len(pdf_links_gs) >= 2:
                            context_gs["download_links_1a"] =  pdf_links_gs[0]["GET"].replace("\\", "//")
                            context_gs["extension_1a"] = "fb2 or other"
                            context_gs["download_links_2a"] = pdf_links_gs[1]["GET"].replace("\\", "//")
                            context_gs["extension_2a"] = "fb2 or other"

                        elif len(pdf_links_gs) == 1:
                            context_gs["download_links_1a"] =  pdf_links_gs[0]["GET"].replace("\\", "//")
                            context_gs["extension_1a"] = "fb2 or other"

                        elif len(pdf_links_gs) == 0:
                            context_gs["message_read_download"] = "This book is probably not available for download in pdf or epub."
                                                                                              
        except Exception as e:
            context_gs["message_read_download"] = "This book is probably not available for download in pdf or epub."

    else:
        print("NO 1. results_gs")
        context_gs["message_read_download"] = "This book is probably not available for download in pdf or epub, below is the last chance for those who persevere."
    # download_book_gs.context_gs_val = context_gs
    return context_gs


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def download_book(request, id):
    current_url_name = request.path
    print()
    print("current_url_name =", current_url_name)
    print()
    context = context_main
    book_id = current_url_name.split("/")[-1]
    # book = get_object_or_404(Book, pk=book_id)
    book = Book.objects.filter(pk = book_id).first()
    context['book'] = book
    print("book.id", book.id)
    book_download= Book.objects.filter(pk = book_id).values()[0]
    # print(book_download)
    print("book_download =", book_download)
    print()
    # print("formlib_download:", formlib_download)
    r_user = request.user
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    formlib_download = BookDownload(request.GET)

    context["book_id"] = book_download["id"]
    context['num_authors'] = num_authors
    context['num_books'] = num_books    

    context['book_id'] = book.id
    print("book.id", book.id)
    print("book.title", book.title)
    print("book.author", book.author)
    download_book.book_id_download_value = book.id
    links_to_download = []
    pdf_links_rs = []
    else_links = []
    
    context["author_download"] = book.author
    context["title_download"] = book.title
    context["search_title_download"] = book.title
    context["language_download"] = book.language
    title_docer_pdf = f'{book.author.split()[-1]}+{book.title.replace(" ", "+")}'
    context["title_read_last_chance"] = f"https://docer.pl/show/?q={title_docer_pdf}&ext=pdf" 
    url_pdf_bot = Book.objects.filter(pk=book.id).values_list("url_pdf")[0][0]
    if url_pdf_bot != "" and url_pdf_bot != None and url_pdf_bot.startswith("https://stream2.docer.pl/pdf_dummy/"):       
        print("599. url_pdf_bot =", url_pdf_bot) 
        # context["url_pdf_bot"] = url_pdf_bot
        #
        try:
            resp = requests.head(url_pdf_bot)
            if resp.status_code == 200:
                context["url_pdf_bot_yes"] = url_pdf_bot
                print(f"606. download_book YES {book.title} ")
                time.sleep(2.1)
            else:
                context["url_pdf_bot_yes"] = ""
                print(f"610. download_bookNO {book.title} docer.pl")
                try:                  
                    serializer = BookPdfUrlSerializer(book, data={'pdf_search_filename': "", 'url_pdf_search': "", "url_pdf": ""}, partial=True)
                    if serializer.is_valid():
                        serializer.save() 
                        time.sleep(2.1)
                        
                except Exception as e:
                    print(f"618 download_book serializer.save() Exception as {e}")
                    time.sleep(2.1)                 
        except Exception as e:
            print(f"621 download_book Exception as {e}")
            time.sleep(2.1)
        #
    else:
        context["url_pdf_bot_yes"] = ""
        
        
    if formlib_download.is_valid():
        book_id_download = formlib_download.cleaned_data['book_id_download_search']
        print("630. download_book book_id_download =", book_id_download)
        
        if book.language == "pl":
            try:
                wl_pdf_url = "https://wolnelektury.pl/media/book/pdf/" + slugify(book.title) + ".pdf"
                resp = requests.head(wl_pdf_url)
                if resp.status_code == 200:
                    context["wl_pdf_url"] = wl_pdf_url
                    print(f"YES {book.title} wolne-lektury")
                else:
                    context["wl_pdf_url"] = ""
                    print(f"NO {book.title} wolne-lektury")
            except Exception as e:
                print(f"643. download_book wolne-lektury Exception as {e}")
                
            context_gs = {}
            download_book_gs(book_download, context_gs)
            time.sleep(0.6)
            if context_gs:
                # print("context_gs =", context_gs)
                print("650. context_gs =", context_gs)
            else:
                print("652. NO context_gs")
            # print("download_book_gs(title_download) =", download_book_gs(title_download, context_gs))
            context.update(context_gs)
            print()
            return Response(context, template_name='download_book.html',)

        elif book.language != "pl":
            context_rs = {}           
            download_book_rs(book_download, context_rs)
            context.update(context_rs)
            if len(context["pdf_links_rs"]) > 0:
                return Response(context, template_name='download_book.html',)
            else:
                print("NO pdf_links_rs")
                context_gs = {}
                download_book_gs(book_download, context_gs) 
                context.update(context_gs)
                print()
                return Response(context, template_name='download_book.html',)                   

                

    context["search_title_download"] = BookDownload()

    return Response(context, template_name='download_book.html', )


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def download_path(request):
    # Sprawdzenie, czy żądanie jest metodą POST
    context = {}
    if request.method == "POST":
        # Pobranie ścieżki do folderu downloads na urządzeniu użytkownika z żądania
        # download_path = request.POST.get("download_path")
        # Zwrócenie odpowiedzi JSON z danymi o ścieżce do folderu downloads
        data_path_to_downloads = request.data
        path_to_downloads = data_path_to_downloads["str_download_path"]
        download_path.path_to_downloads = data_path_to_downloads["str_download_path"]
        print("download_path.path_to_downloads =", path_to_downloads)
        if path_to_downloads:
            return JsonResponse(
            {
                "status_download_path": path_to_downloads,
                "status_message": "Dane o ścieżce do folderu downloads zostały odebrane.",
            }
        )
    # Zwrócenie błędu, jeśli żądanie nie jest metodą POST
    else:
        return JsonResponse({"error": "Nieprawidłowa metoda żądania."})
    
    return render(request, 'download_path.html', context)
    
def def_book_scrap(pdf_url_download_docer, context, book_to_message):
    pdf_url_download_docer = book_scrap.pdf_url_download_found
    print("pdf_url_download_docer =", pdf_url_download_docer)

    if pdf_url_download_docer ==  "no link pdf docer":
        print("1a. pdf_url_download_docer =", pdf_url_download_docer)
        context["url_pdf_docer"] = "no link pdf docer"
        context["message_docer"] = f"NOT possible to download book {book_to_message}"

    elif pdf_url_download_docer == "link pdf unfinished":
        print("1b. pdf_url_download_docer =", pdf_url_download_docer)
        context["url_pdf_docer"] = "link pdf unfinished"
        context["message_docer"] = f"something went wrong searching book {book_to_message} unfinished, try later"

    elif pdf_url_download_docer == "link pdf exist":
        print("1c. pdf_url_download_docer =", pdf_url_download_docer)
        pdf_url_search = book_scrap.get_current_url
        print("pdf_url_search =", pdf_url_search)
        pdf_filename = book_scrap.link_first_filename
        context["url_pdf_docer"] = "link pdf exist"
        context["message_docer"] = f"something went wrong link to book {book_to_message} exist but download ufinished, try later"
    else:
        print("1d. pdf_url_download_docer =", pdf_url_download_docer)
        pdf_url_search = book_scrap.get_current_url
        print("pdf_url_search =", pdf_url_search)
        pdf_filename = book_scrap.link_first_filename
        context["url_pdf_docer_yes"] = pdf_url_download_docer
        context["message_docer"] = f"probably book {book_to_message} is downloaded, check folder downloads"
    return context

def def_book_scrap_ready(pdf_url_download_docer, context, book_to_message):
    if pdf_url_download_docer == "link pdf exist":
        print("pdf_url_download_docer = link pdf exist")
        context["url_pdf_docer"] = "link pdf exist"
        context["message_docer"] = f"something went wrong link to book {book_to_message} exist but download unfinished, try later"
    else:
        print("pdf_url_download =", pdf_url_download_docer)
        context["message_docer"] = f"probably book {book_to_message} is downloaded, check folder downloads"
    return context
    
    
books_values = []
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def download_docer(request):
    # book = get_object_or_404(Book, pk=id)       
        
    print("def download_docer")
    r_user = request.user
    current_url_name = request.path
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    author_book_libgen = ""
    title_download_libgen = ""
    language_download_libgen = ""
    book_to_message = ""
    context = context_main
    context['num_authors'] = num_authors
    context['num_books'] = num_books
    try:
        from booksmart.test_docer import book_scrap, book_scrap_ready
    except Exception as e:
        print(f"Exception as {e}")
        context["message_docer"] = f"This option does not work on server yet"
        return Response(context, template_name='download_book_bot.html', )     
    
    book_values_id = []
    context["message_docer"] = ""
    context["url_pdf_docer"] = ""
    context["url_pdf_docer_yes"] = ""
    context_book_scrap = {}
    download_bot = BookDownloadDocer(request.GET)
    if download_bot.is_valid():
        form_download_docer = download_bot.cleaned_data['book_download_bot']
        print("form_download_docer =", form_download_docer)
        book_values_id.append(form_download_docer)
        # book_docer(author_book_docer, title_download_docer)
        # if download_book.author_download_value == "" or download_book.author_download_value == None:
        try:
            
            if download_book.book_id_download_value:
                book_id_docer = download_book.book_id_download_value
                print("book_id_docer =", book_id_docer)
                if book_id_docer == "" or book_id_docer == None:
                    print("download_book.book_id_download_value =", download_book.book_id_download_value)
                    book_id_docer = book_values_id[-1]
                    # author_book_docer = book_values_id[-3]
                    book_to_download = Book.objects.filter(pk=book_id_docer).first()
                    # url_pdf_docer_search = Book.objects.filter(pk=book_id_docer).values_list("url_pdf_search")[0][0]
                    # url_pdf_docer = Book.objects.filter(pk=book_id_docer).values_list("url_pdf")[0][0]
                    book_to_download_values = Book.objects.filter(pk=book_id_docer).values()[0]
                    book_to_download_title = book_to_download_values["title"]
                    book_to_download_author = book_to_download_values["author"]
                    book_to_message = f'<p><span style="line-height: 1.2;" id="a_submit_t"> "{book_to_download_title}" </p> {book_to_download_author} </p><br>'
                    url_pdf_docer_search = book_to_download_values["url_pdf_search"]
                    url_pdf_docer = book_to_download_values["url_pdf"]
                    
                    if url_pdf_docer != "" and url_pdf_docer != None and url_pdf_docer.startswith("https://stream2.docer.pl/pdf_dummy/"):
                        # context["url_pdf_docer_yes"] = url_pdf_docer
                        # print("url_pdf_docer_yes =", url_pdf_docer)
                        #
                        try:
                            resp = requests.head(url_pdf_docer)
                            if resp.status_code == 200:
                                context["url_pdf_docer_yes"] = url_pdf_docer
                                print(f"763 download_docer YES {book_to_download.title} docer.pl")
                                time.sleep(2.1)
                            else:
                                context["url_pdf_bot"] = ""
                                print(f"773 download_docer NO {book_to_download.title} docer.pl")
                                try:                  
                                    serializer = BookPdfUrlSerializer(book_to_download, data={'pdf_search_filename': "", 'url_pdf_search': "", "url_pdf": ""}, partial=True)
                                    if serializer.is_valid():
                                        serializer.save() 
                                        time.sleep(2.1)
                                        try:
                                            book_scrap(context_book_scrap, book_id_docer)
                                            pdf_url_download_docer = book_scrap.pdf_url_download_found
                                            def_book_scrap(pdf_url_download_docer, context, book_to_message)
                                        except Exception as e:
                                            print(f"777 download_docer Exception as {e}")
                                        
                                except Exception as e:
                                    print(f"780 download_docer serializer.save() Exception as {e}")
                                    time.sleep(2.1)                 
                        except Exception as e:
                            print(f"783 download_docer Exception as {e}")
                            time.sleep(2.1) 
                        #
                                                   
                    elif url_pdf_docer_search != "" and url_pdf_docer_search != None and url_pdf_docer_search.startswith("https://docer.pl/doc/"):
                        
                        # book_scrap_ready(context_book_scrap, book_id_docer)
                        # pdf_url_download_docer = book_scrap_ready.pdf_url_download_found
                        # print("pdf_url_download_docer =", pdf_url_download_docer)                        
                        # if pdf_url_download_docer == "link pdf exist":
                        #     print("pdf_url_download_docer = link pdf exist")
                        #     context["url_pdf_docer"] = "link pdf exist"
                        #     context["message_docer"] = f"something went wrong link to book {book_to_message} exist but download unfinished, try later"
                        # else:
                        #     print("pdf_url_download =", pdf_url_download_docer)
                        #     # serializer = BookPdfUrlSerializer(book_to_download, data={'url_pdf': pdf_url_download_docer}, partial=True)
                        #     # if serializer.is_valid():
                        #     #     serializer.save()
                        #     context["message_docer"] = f"probably book {book_to_message} is downloaded, check folder downloads"                        
                        
                        book_id_book_scrap_ready = book_id_docer
                        #
                        try:
                            resp = requests.head(url_pdf_docer_search)
                            if resp.status_code == 200:
                                context["url_pdf_docer_search"] = url_pdf_docer_search
                                print(f"852. download_docer YES {book_to_download.title} url_pdf_docer_search")
                                time.sleep(2.1)
                                book_scrap_ready(context_book_scrap, book_id_docer)
                                pdf_url_download_docer = book_scrap_ready.pdf_url_download_found
                                print("pdf_url_download_docer =", pdf_url_download_docer)
                                if pdf_url_download_docer == "link pdf exist":
                                    print("858. pdf_url_download_docer = link pdf exist")
                                    context["url_pdf_docer"] = "link pdf exist"
                                    context["message_docer"] = f"something went wrong link to book {book_to_message} exist but download unfinished, try later"
                                else:
                                    print("862. pdf_url_download =", pdf_url_download_docer)
                                    context["message_docer"] = f"probably book {book_to_message} is downloaded, check folder downloads"                                
                            else:
                                print(f"2. NO {book_to_download.title} docer.pl url_pdf_docer_search")
                                try:                  
                                    serializer = BookPdfUrlSerializer(book_to_download, data={'pdf_search_filename': "", 'url_pdf_search': "", "url_pdf": ""}, partial=True)
                                    if serializer.is_valid():
                                        serializer.save() 
                                        time.sleep(2.1)
                                        try:
                                            book_scrap(context_book_scrap, book_id_docer)
                                            pdf_url_download_docer = book_scrap.pdf_url_download_found
                                            def_book_scrap(pdf_url_download_docer, context, book_to_message)
                                        except Exception as e:
                                            print(f"879 download_docer Exception as {e}")
                                        
                                except Exception as e:
                                    print(f"882 download_docer serializer.save() Exception as {e}")
                                    time.sleep(2.1)                 
                        except Exception as e:
                            print(f"885 download_docer Exception as {e}")   
                        #                     
                        
                    else:
                        print("1. url_pdf_docer =", url_pdf_docer)
                        
                        if url_pdf_docer == "no link pdf docer":
                            print("1a. url_pdf_docer =", url_pdf_docer)
                            context["url_pdf_docer"] = "no link pdf docer"
                            context["message_docer"] = f"NOT possible to download book{book_to_message}"

                        elif url_pdf_docer == "" or url_pdf_docer == None or url_pdf_docer == "link pdf unfinished":
                            book_id_book_scrap = book_id_docer

                            book_scrap(context_book_scrap, book_id_book_scrap)
                            
                            pdf_url_download_docer = book_scrap.pdf_url_download_found
                            print("pdf_url_download_docer =", pdf_url_download_docer)

                            if pdf_url_download_docer ==  "no link pdf docer":
                                print("1a. pdf_url_download_docer =", pdf_url_download_docer)
                                context["url_pdf_docer"] = "no link pdf docer"
                                context["message_docer"] = f"NOT possible to download book {book_to_message}"

                            elif pdf_url_download_docer == "link pdf unfinished":
                                print("1b. pdf_url_download_docer =", pdf_url_download_docer)
                                context["url_pdf_docer"] = "link pdf unfinished"
                                context["message_docer"] = f"something went wrong searching book {book_to_message} unfinished, try later"

                            elif pdf_url_download_docer == "link pdf exist":
                                print("1c. pdf_url_download_docer =", pdf_url_download_docer)
                                pdf_url_search = book_scrap.get_current_url
                                print("pdf_url_search =", pdf_url_search)
                                pdf_filename = book_scrap.link_first_filename
                                context["url_pdf_docer"] = "link pdf exist"
                                context["message_docer"] = f"something went wrong link to book {book_to_message} exist but download ufinished, try later"
                            else:
                                print("1d. pdf_url_download_docer =", pdf_url_download_docer)
                                pdf_url_search = book_scrap.get_current_url
                                print("pdf_url_search =", pdf_url_search)
                                pdf_filename = book_scrap.link_first_filename
                                context["url_pdf_docer_yes"] = pdf_url_download_docer
                                context["message_docer"] = f"probably book {book_to_message} is downloaded, check folder downloads"
                        else:
                            context["url_pdf_docer_yes"] = url_pdf_docer
                            print("url_pdf_docer_yes =", url_pdf_docer)

                elif book_id_docer != "" and book_id_docer != None:
                    book_id_libgen = download_book.book_id_download_value
                    print("book_id_libgen =", book_id_libgen)
                    book_values_id.append(book_id_libgen)
                    book_to_download = Book.objects.filter(pk=book_id_libgen).first()
                
                    book_to_download_values = Book.objects.filter(pk=book_id_libgen).values()[0]
                    book_to_download_title = book_to_download_values["title"]
                    book_to_download_author = book_to_download_values["author"]
                    book_to_message = f'<br><span style="line-height: 1;" id="a_submit_t"> "{book_to_download_title}" <br>{book_to_download_author}</span><br>'
                    url_pdf_docer_search = book_to_download_values["url_pdf_search"]
                    url_pdf_docer = book_to_download_values["url_pdf"]
                    print("1. url_pdf_docer =", url_pdf_docer)
                    pdf_search_filename = book_to_download_values["pdf_search_filename"]
                    
                    if url_pdf_docer != "" and url_pdf_docer != None and url_pdf_docer.startswith("https://stream2.docer.pl/pdf_dummy/"):
                        context["url_pdf_docer_yes"] = url_pdf_docer
                        print("url_pdf_docer_yes =", url_pdf_docer)
                        
                        try:
                            resp = requests.head(url_pdf_docer)
                            if resp.status_code == 200:
                                context["url_pdf_docer_yes"] = url_pdf_docer
                                print(f"763 download_docer YES {book_to_download.title} docer.pl")
                                time.sleep(2.1)
                            else:
                                context["url_pdf_bot"] = ""
                                print(f"773 download_docer NO {book_to_download.title} docer.pl")
                                try:                  
                                    serializer = BookPdfUrlSerializer(book_to_download, data={'pdf_search_filename': "", 'url_pdf_search': "", "url_pdf": ""}, partial=True)
                                    if serializer.is_valid():
                                        serializer.save() 
                                        time.sleep(2.1)
                                        try:
                                            book_scrap(context_book_scrap, book_id_docer)
                                            pdf_url_download_docer = book_scrap.pdf_url_download_found
                                            def_book_scrap(pdf_url_download_docer, context, book_to_message)
                                        except Exception as e:
                                            print(f"777 download_docer Exception as {e}")
                                        
                                except Exception as e:
                                    print(f"780 download_docer serializer.save() Exception as {e}")
                                    time.sleep(2.1)                 
                        except Exception as e:
                            print(f"783 download_docer Exception as {e}")
                            time.sleep(2.1) 
                        #                     
                        
                    # elif url_pdf_docer != "" and url_pdf_docer != None and url_pdf_docer_search != "" and url_pdf_docer_search != None and not url_pdf_docer.startswith("https://stream2.docer.pl/pdf_dummy/") and url_pdf_docer_search.startswith("https://docer.pl/doc/"):
                    elif url_pdf_docer_search != "" and url_pdf_docer_search != None and url_pdf_docer_search.startswith("https://docer.pl/doc/"):
                        book_id_book_scrap_ready = book_id_libgen
                        
                        # book_scrap_ready(context_book_scrap, book_id_book_scrap_ready)
                        # pdf_url_download_docer = book_scrap_ready.pdf_url_download_found
                        # print("pdf_url_download_docer =", pdf_url_download_docer)
                        # if pdf_url_download_docer == "link pdf exist":
                        #     print("pdf_url_download_docer = link pdf exist")
                        #     context["url_pdf_docer"] = "link pdf exist"
                        #     context["message_docer"] = f"something went wrong link to book {book_to_message} exist but download unfinished, try later"
                        # else:
                        #     print("pdf_url_download =", pdf_url_download_docer)
                        #     context["message_docer"] = f"probably book {book_to_message} is downloaded, check folder downloads"
                            
                        try:
                            resp = requests.head(url_pdf_docer_search)
                            if resp.status_code == 200:
                                context["url_pdf_docer_search"] = url_pdf_docer_search
                                print(f"995. download_docer YES {book_to_download.title} url_pdf_docer_search")
                                time.sleep(2.1)
                                book_scrap_ready(context_book_scrap, book_id_book_scrap_ready)
                                pdf_url_download_docer = book_scrap_ready.pdf_url_download_found
                                print("pdf_url_download_docer =", pdf_url_download_docer)
                                if pdf_url_download_docer == "link pdf exist":
                                    print("858. pdf_url_download_docer = link pdf exist")
                                    context["url_pdf_docer"] = "link pdf exist"
                                    context["message_docer"] = f"something went wrong link to book {book_to_message} exist but download unfinished, try later"
                                else:
                                    print("862. pdf_url_download =", pdf_url_download_docer)
                                    context["message_docer"] = f"probably book {book_to_message} is downloaded, check folder downloads"                                
                            else:
                                print(f"1008 NO {book_to_download.title} docer.pl url_pdf_docer_search")
                                try:                  
                                    serializer = BookPdfUrlSerializer(book_to_download, data={'pdf_search_filename': "", 'url_pdf_search': "", "url_pdf": ""}, partial=True)
                                    if serializer.is_valid():
                                        serializer.save() 
                                        time.sleep(2.1)
                                        try:
                                            book_scrap(context_book_scrap, book_id_book_scrap_ready)
                                            pdf_url_download_docer = book_scrap.pdf_url_download_found
                                            def_book_scrap(pdf_url_download_docer, context, book_to_message)
                                        except Exception as e:
                                            print(f"879 download_docer Exception as {e}")
                                        
                                except Exception as e:
                                    print(f"882 download_docer serializer.save() Exception as {e}")
                                    time.sleep(2.1)                 
                        except Exception as e:
                            print(f"885 download_docer Exception as {e}")
                        #                            
                        
                    else:
                        if url_pdf_docer == "no link pdf docer":
                            context["url_pdf_docer"] = "no link pdf docer"
                            context["message_docer"] = f"NOT possible to find to download book {book_to_message}"

                        elif url_pdf_docer == "" or url_pdf_docer==None or url_pdf_docer == "link pdf unfinished":

                            book_to_download = Book.objects.filter(pk=book_id_libgen).first()

                            book_id_book_scrap = book_id_libgen
                            # book_scrap(author_book_docer, title_download_docer)
                            book_scrap(context_book_scrap, book_id_book_scrap)
                            pdf_url_search = book_scrap.get_current_url
                            pdf_filename = book_scrap.link_first_filename
                            pdf_url_download_docer = book_scrap.pdf_url_download_found
                            print("pdf_url_download_docer =", pdf_url_download_docer)
                            
                            if pdf_url_search == "" or pdf_url_search == None:
                                context["message_docer"] = f"something went wrong with searching book {book_to_message} probably captcha, try later"

                            elif pdf_url_download_docer ==  "no link pdf docer":
                                print("")
                                context["url_pdf_docer"] = "no link pdf docer"
                                context["message_docer"] = f"NOT possible to download book {book_to_message}"

                            elif pdf_url_download_docer == "link pdf unfinished":
                                print("pdf_url_download_docer = link pdf unfinished")
                                context["message_docer"] = f"Something went wrong searching book {book_to_message} unfinished, try later"

                            elif pdf_url_download_docer == "link pdf exist":
                                print("pdf_url_download_docer = link pdf exist")
                                pdf_url_search = book_scrap.get_current_url
                                print("pdf_url_search =", pdf_url_search)
                                pdf_filename = book_scrap.link_first_filename

                                context["url_pdf_docer"] = "link pdf exist"
                                context["message_docer"] = "Something went wrong link exist but download unfinished, try later"
                            else:
                                print("pdf_url_download =", pdf_url_download_docer)
                                pdf_url_search = book_scrap.get_current_url
                                print("pdf_url_search =", pdf_url_search)
                                pdf_filename = book_scrap.link_first_filename

                                context["message_docer"] = f"Probably book {book_to_message} is downloaded, check folder downloads"
        except Exception as e:
            print(f"book_id_docer Exception: {e}")
            context["message_docer"] = f"Exception but probably book {book_to_message} is downloaded, if not try later"
            return Response(context, template_name='download_book_bot.html', )

    # return Response(context, template_name='download_book_doc.html', )
    # return HttpResponseRedirect(reverse('booksmart:downloadbook'))
    return Response(context, template_name='download_book_bot.html', )

