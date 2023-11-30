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
from accounts.views_authorization import *

from rest_framework import filters as base_filters

import datetime

from django.utils.text import slugify


from booksmart.search_download_gs import SearchRequestGS
from booksmart.search_download_is import SearchRequestIS
from booksmart.search_download_pm import SearchRequestPM,SearchRequestPM_my
from bs4 import BeautifulSoup

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

MIRROR_SOURCES = ["GET", "Cloudflare", "IPFS.io", "Infura"]
MIRROR_SOURCE_GET = ["GET"]

class LibgenSearch:
    def search_title(self, query):
        # search_request = SearchRequestGS(query, search_type="title")
        search_request = SearchRequestPM(query, search_type="title")
        return search_request.aggregate_request_data()

    def search_author(self, query):
        # search_request = SearchRequestGS(query, search_type="author")
        search_request = SearchRequestPM(query, search_type="author")
        return search_request.aggregate_request_data()

    def search_title_filtered(self, query, filters, exact_match=True):
        # search_request = SearchRequestGS(query, search_type="title")
        search_request = SearchRequestPM(query, search_type="title")
        results = search_request.aggregate_request_data()
        filtered_results = filter_results(
            results=results, filters=filters, exact_match=exact_match
        )
        print("search_title_filtered =", filtered_results)
        return filtered_results

    def search_author_filtered(self, query, filters, exact_match=True):
        # search_request = SearchRequestGS(query, search_type="author")
        search_request = SearchRequestPM(query, search_type="author")
        results = search_request.aggregate_request_data()
        filtered_results = filter_results(
            results=results, filters=filters, exact_match=exact_match
        )
        return filtered_results

    def resolve_download_links(self, item):
        mirror_1 = item["Mirror_1"]
        print("\nmirror_1 =", mirror_1)
        # page = requests.get(f'https://libgen.gs{mirror_1}')
        page = requests.get(f'https://libgen.pm{mirror_1}')
        # page = requests.get(mirror_1)
        soup = BeautifulSoup(page.text, "html.parser")
        
        links = soup.find_all("a", string=MIRROR_SOURCES)
        download_links = {link.string: link["href"] for link in links}
        
        print(f"\n1. download_links = {download_links}\n")

        return download_links

class LibgenSearch_my:
    def search_title(self, query):
        # search_request = SearchRequestGS(query, search_type="title")
        search_request = SearchRequestPM_my(query, search_type="title")
        return search_request.aggregate_request_data()

    def search_author(self, query):
        # search_request = SearchRequestGS(query, search_type="author")
        search_request = SearchRequestPM_my(query, search_type="author")
        return search_request.aggregate_request_data()

    def search_title_filtered(self, query, filters, exact_match=True):
        # search_request = SearchRequestGS(query, search_type="title")
        search_request = SearchRequestPM_my(query, search_type="title")
        results = search_request.aggregate_request_data()
        filtered_results = filter_results(
            results=results, filters=filters, exact_match=exact_match
        )
        print("search_title_filtered =", filtered_results)
        return filtered_results

    def search_author_filtered(self, query, filters, exact_match=True):
        # search_request = SearchRequestGS(query, search_type="author")
        search_request = SearchRequestPM_my(query, search_type="author")
        results = search_request.aggregate_request_data()
        filtered_results = filter_results(
            results=results, filters=filters, exact_match=exact_match
        )
        return filtered_results

    def resolve_download_links(self, item):
        
        mirror_1 = item["Mirror_1"]
        print("\nmirror_1 =", mirror_1)
        # page = requests.get(f'https://libgen.gs{mirror_1}')
        page = requests.get(f'https://libgen.pm{mirror_1}')
        # page = requests.get(mirror_1)
        soup = BeautifulSoup(page.text, "html.parser")
        
        links = soup.find_all("a", string=MIRROR_SOURCES)
        download_links = {link.string: link["href"] for link in links}
        
        print(f"\n1. download_links = {download_links}\n")

        return download_links

    def resolve_download_links_my(self, item):
        
        mirror_1 = item["Mirror_1"]
        page = requests.get(mirror_1)
        soup = BeautifulSoup(page.text, "html.parser")
        
        links = soup.find_all("a", string=MIRROR_SOURCE_GET)
        download_links_my = {link.string: link["href"] for link in links}
        
        # print(f"\n1. download_links_my = {download_links_my}\n")

        return download_links_my


def filter_results(results, filters, exact_match):
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
    print(f"\nfiltered_list = {filtered_list}\n")
    return filtered_list



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def download_book(request):

    # book = get_object_or_404(Book, pk=id)
    # print("formlib_download:", formlib_download)
    r_user = request.user
    current_url_name = request.path
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main
    context['num_authors'] = num_authors
    context['num_books'] = num_books    

    formlib_download = BookDownload(request.GET)

    links_to_download = []
    search_libgen = LibgenSearch()
    # if request.method == "POST":
    #     if request.POST.get('title_download_search', False):

    # results = s.search_title("Harry Potter i zakon feniksa")
    # print('results', results)
    pdf_links = []
    else_links = []
    title_download = ""
    context["title_download"] = ""
    context["title_read_last_chance"] = ""
    context["download_links_1a"] = ""
    context["download_links_2a"] = ""
    context["title_read_last_chance"] = ""
    context["message_read_download"] = ""
    context["message_read_download_not_pdf"] = ""
    
    if formlib_download.is_valid():
        title_download=formlib_download.cleaned_data['title_download_search']
        print("1. title_download", title_download)
        context["title_download"] = title_download
        title_docer_pdf = title_download.replace(" ", "+")
        context["title_read_last_chance"] = f"https://docer.pl/show/?q={title_docer_pdf}&ext=pdf" 
        results = search_libgen.search_title(title_download)

        if results:
            items_to_download = results
            print("items_to_download =", items_to_download)
            try:
                pdf_links = [search_libgen.resolve_download_links(item_to_download) for item_to_download in items_to_download if item_to_download["Ext."] == "pdf"] 
                if len(pdf_links) > 0:

                    print("pdf_links", pdf_links)
                    context["pdf_links"] = pdf_links
                    context["len_pdf_links"] = len(pdf_links)
                    
                    pdf_links_id = [[pdf_links.index(pdf_link), pdf_link] for pdf_link in pdf_links]
                    context["pdf_links_id"] = pdf_links_id

                    if len(pdf_links) >= 2:
                        download_links_pdf_1a = pdf_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        print("download_links_pdf_1a =", download_links_pdf_1a)
                        context["download_links_1a"] = download_links_pdf_1a
                        context["extension_1a"] = "pdf"
                        download_links_pdf_2a = pdf_links[1]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        context["download_links_2a"] = download_links_pdf_2a
                        context["extension_2a"] = "pdf"
                        print("download_links_pdf_2a =", download_links_pdf_2a)

                        return Response(context, template_name='download_book.html',)

                    elif len(pdf_links) == 1:
                        download_links_1a = pdf_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        context["download_links_1a"] = download_links_1a
                        context["extension_1a"] = "pdf"
                        return Response(context, template_name='download_book.html',)

                elif len(pdf_links) == 0:
                    try:
                        # items_to_download = results
                        else_links = [search_libgen.resolve_download_links(item_to_download) for item_to_download in items_to_download] 

                        if len(else_links) > 0:
                            print("else_links", else_links)
                            context["pdf_links"] = else_links
                            context["len_pdf_links"] = len(else_links)
                    
                            # else_links_id = [[else_links.index(else_link), else_link] for else_link in else_links]
                            # context["else_links_id"] = else_links_id
                            extentions = [val['Ext.'] for val in items_to_download]
                            if len(else_links) >= 2:

                                download_links_else_1a = else_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                                print("download_links_else_1a =", download_links_else_1a)
                                context["download_links_1a"] = download_links_else_1a
                                context["extention_1a"] = extentions[0]

                                download_links_else_2a = else_links[1]["GET"].replace("get.php", "https://libgen.pm/get.php")
                                context["download_links_2a"] = download_links_else_2a
                                context["extention_2a"] = extentions[1]
                                
                                print("else download_links_2a =", download_links_else_2a)
                                context["message_read_download_not_pdf"] = "This book is probably not available for download in pdf, press buttons below to download in differt format."
                                return Response(context, template_name='download_book.html',)

                            elif len(else_links) == 1:
                                download_links_else_1a = else_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                                context["download_links_1a"] = download_links_else_1a
                                context["extention_1a"] = extentions[0]
                                print("download_links_else_1a =", download_links_else_1a)
                                context["message_read_download_not_pdf"] = "This book is probably not available for download in pdf, press button below to download in other format."
                                return Response(context, template_name='download_book.html',)

                            elif len(else_links) == 0:
                                context["message_read_download"] = "This book is probably not available for download, below is the last chance for those who persevere"
                                # print("2. title_download", title_download)
                                # title_slugify = slugify(title_download).replace(" ", "+").replace(" ", "-")
                                return Response(context, template_name='download_book.html',)

                    except Exception as e:
                        print(f'Exception as e else_links, reason: {e}')
                        context["message_read_download"] = "This book is probably not available for download"
                        # print("3. title_download", title_download)
                        return Response(context, template_name='download_book.html',)

            except Exception as e:
                context["message_read_download"] = "This book is probably not available for download in pdf, or any other format."
                # print("3. title_download", title_download)
                return Response(context, template_name='download_book.html',)

        else:
            # print("4. title_download", title_download)
            context["message_read_download"] = "This book is probably not available for download in pdf, below is the last chance for those who persevere."
            return Response(context, template_name='download_book.html',)

    context["search_title_download"] = BookDownload()
    return Response(context, template_name='download_book.html', )