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
from booksmart.test_docer import *
from booksmart.api.serializers import BookPdfUrlSerializer


# from booksmart.search_download_gs import SearchRequestGS
# from booksmart.search_download_gs import SearchRequestRS
# from booksmart.search_download_is import SearchRequestIS
# from booksmart.search_download_pm import SearchRequestPM, SearchRequestPM_my
from booksmart.search_download_rs import SearchRequestRS
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
        search_request = SearchRequestRS(query, search_type="title")
        return search_request.aggregate_request_data()

    def search_author(self, query):
        search_request = SearchRequestRS(query, search_type="author")
        return search_request.aggregate_request_data()

    def search_title_filtered(self, query, filters, exact_match=True):
        search_request = SearchRequestRS(query, search_type="title")
        results = search_request.aggregate_request_data()
        filtered_results = filter_results(
            results=results, filters=filters, exact_match=exact_match
        )
        print("search_title_filtered =", filtered_results)
        return filtered_results

    def search_author_filtered(self, query, filters, exact_match=True):
        search_request = SearchRequestRS(query, search_type="author")
        results = search_request.aggregate_request_data()
        filtered_results = filter_results(
            results=results, filters=filters, exact_match=exact_match
        )
        return filtered_results

    def resolve_download_links(self, item):
        mirror_1 = item["Mirrors"]
        print("\nmirror_1 =", mirror_1)
        # page = requests.get(f'https://libgen.pm{mirror_1}')
        # page = requests.get(f'https://libgen.rs{mirror_1}')
        page = requests.get(mirror_1)
        soup = BeautifulSoup(page.text, "html.parser")
        
        links = soup.find_all("a", string=MIRROR_SOURCES)
        download_links = {link.string: link["href"] for link in links}
        
        print(f"\n1. download_links = {download_links}\n")

        return download_links



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
    # search_libgen = LibgenSearch()
    search_libgen = LibgenSearch()
    
    # print("search_libgen_all =", search_libgen_all)
    # search_libgen = search_libgen_all["output_data"]
    # if request.method == "POST":
    #     if request.POST.get('title_download_search', False):

    # results = s.search_title("Harry Potter i zakon feniksa")
    # print('results', results)
    pdf_links = []
    else_links = []
    title_download = ""
    context["title_download"] = ""
    context["language_download"] = ""
    context["title_read_last_chance"] = ""
    context["download_links_1a"] = ""
    context["download_links_2a"] = ""
    context["title_read_last_chance"] = ""
    context["message_read_download"] = ""
    context["message_read_download_not_pdf"] = ""

    if formlib_download.is_valid():
        # pdf_url_download=formlib_download.cleaned_data['pdf_url_download_search']
        book_id_download = formlib_download.cleaned_data['book_id_download_search']
        # author_download=formlib_download.cleaned_data['author_download_search']
        # title_download=formlib_download.cleaned_data['title_download_search']
        # language_download=formlib_download.cleaned_data['language_download_search']
        print("1. book_id_download =", book_id_download)
        author_download = Book.objects.filter(pk=book_id_download).values_list("author")[0][0]
        title_download = Book.objects.filter(pk=book_id_download).values_list("title")[0][0]
        language_download = Book.objects.filter(pk=book_id_download).values_list("language")[0][0]
        # print("1. author_download =", author_download)
        # print("1. title_download =", title_download)
        # print("1. language_download =", language_download)
        # download_book.pdf_url_download_value = pdf_url_download
        
        # download_book.author_download_value = author_download
        # download_book.title_download_value = title_download
        # download_book.language_download_value = language_download

        download_book.book_id_download_value = book_id_download
        context["author_download"] = author_download
        context["title_download"] = title_download
        context["language_download"] = language_download
        title_docer_pdf = f'{author_download.split()[-1]}+{title_download.replace(" ", "+")}'
        context["title_read_last_chance"] = f"https://docer.pl/show/?q={title_docer_pdf}&ext=pdf" 
        results = search_libgen.search_title(title_download)

        if results:
            print("results =", results[:2])
            items_to_download = results
            
            try:
                pdf_links = [search_libgen.resolve_download_links(item_to_download) for item_to_download in items_to_download if item_to_download["Extension"] == "pdf"] 
                if len(pdf_links) > 0:

                    print("1 pdf_links", pdf_links)
                    context["pdf_links"] = pdf_links
                    context["len_pdf_links"] = len(pdf_links)
                    
                    pdf_links_id = [[pdf_links.index(pdf_link), pdf_link] for pdf_link in pdf_links]
                    context["pdf_links_id"] = pdf_links_id

                    if len(pdf_links) >= 2:
                        # download_links_pdf_1a = pdf_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        download_links_pdf_1a = pdf_links[0]["GET"]
                        context["download_links_1a"] = download_links_pdf_1a
                        context["extension_1a"] = "pdf"
                        print("download_links_pdf_1a =", download_links_pdf_1a)
                        # download_links_pdf_2a = pdf_links[1]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        download_links_pdf_2a = pdf_links[1]["GET"]
                        context["download_links_2a"] = download_links_pdf_2a
                        context["extension_2a"] = "pdf"
                        print("download_links_pdf_2a =", download_links_pdf_2a)

                        return Response(context, template_name='download_book.html',)

                    elif len(pdf_links) == 1:
                        # download_links_1a = pdf_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        download_links_1a = pdf_links[0]["GET"]
                        context["download_links_1a"] = download_links_1a
                        context["extension_1a"] = "pdf"
                        print("download_links_pdf_1a =", download_links_pdf_1a)
                    return Response(context, template_name='download_book.html',)

                elif len(pdf_links) == 0:
                    print("elif len(pdf_links) == 0:")
                    context["message_read_download"] = "This book is probably not available for download"
                    # try:
                    #     # items_to_download = results
                    #     else_links = [search_libgen.resolve_download_links(item_to_download) for item_to_download in items_to_download] 

                    #     if len(else_links) > 0:
                    #         print("else_links", else_links)
                    #         context["pdf_links"] = else_links
                    #         context["len_pdf_links"] = len(else_links)
                    
                    #         # else_links_id = [[else_links.index(else_link), else_link] for else_link in else_links]
                    #         # context["else_links_id"] = else_links_id
                    #         extentions = [val['Ext.'] for val in items_to_download]
                    #         if len(else_links) >= 2:

                    #             download_links_else_1a = else_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                    #             print("download_links_else_1a =", download_links_else_1a)
                    #             context["download_links_1a"] = download_links_else_1a
                    #             context["extention_1a"] = extentions[0]

                    #             download_links_else_2a = else_links[1]["GET"].replace("get.php", "https://libgen.pm/get.php")
                    #             context["download_links_2a"] = download_links_else_2a
                    #             context["extention_2a"] = extentions[1]
                                
                    #             print("else download_links_2a =", download_links_else_2a)
                    #             context["message_read_download_not_pdf"] = "This book is probably not available for download in pdf, press buttons below to download in differt format."
                    #             return Response(context, template_name='download_book.html',)

                    #         elif len(else_links) == 1:
                    #             download_links_else_1a = else_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                    #             context["download_links_1a"] = download_links_else_1a
                    #             context["extention_1a"] = extentions[0]
                    #             print("download_links_else_1a =", download_links_else_1a)
                    #             context["message_read_download_not_pdf"] = "This book is probably not available for download in pdf, press button below to download in other format."
                    #             return Response(context, template_name='download_book.html',)

                    #         elif len(else_links) == 0:
                    #             context["message_read_download"] = "This book is probably not available for download, below is the last chance for those who persevere"
                    #             # print("2. title_download", title_download)
                    #             # title_slugify = slugify(title_download).replace(" ", "+").replace(" ", "-")
                    #             return Response(context, template_name='download_book.html',)

                    # except Exception as e:
                    #     print(f'Exception as e else_links, reason: {e}')
                    #     context["message_read_download"] = "This book is probably not available for download"
                    #     # print("3. title_download", title_download)
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

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# @authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
# @renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
# def download_docer_loader(request, *args):
#     return Response(template_name='download_book_bot.html', )

books_values = []
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer])
def download_docer(request, *args):
    r_user = request.user
    current_url_name = request.path
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    author_book_libgen = ""
    title_download_libgen = ""
    language_download_libgen = ""

    context = context_main
    context['num_authors'] = num_authors
    context['num_books'] = num_books
    book_values = []
    context["message_docer"] = ""
    context["url_pdf_docer"] = ""
    context["url_pdf_docer_yes"] = ""
    # # author_book_docer = download_book.author_download_value.split()[-1]
    # author_book_libgen = download_book.title_download_value.split()[-1]
    # book_values.append(author_book_libgen)
    #  # author_book_docer_full = "Oscar Wilde"
    # print("author_book_docer =", author_book_docer)

    # # title_download_docer = download_book.title_download_value
    # title_download_libgen = download_book.title_download_value
    # book_values.append(title_download_docer)
    # # title_download_docer = "Portret Doriana Graya"
    # print("title_download_docer =", title_download_docer)

    # language_download_libgen = download_book.language_download_value
    # book_values.append(language_download_docer)
    # # language_download_docer = "pl"
    # print("language_download_docer =", language_download_docer)

    download_bot = BookDownloadDocer(request.GET)
    if download_bot.is_valid():
        # form_download_docer=formlib_download.cleaned_data['book_download_bot']
        # book_docer(author_book_docer, title_download_docer)
        print("download_book.book_id_download_value =", download_book.book_id_download_value)

        # if download_book.author_download_value == "" or download_book.author_download_value == None:
        if download_book.book_id_download_value == "" or download_book.book_id_download_value == None:
            book_id_docer = book_values[-1]
            # author_book_docer = book_values[-3]
            url_pdf_docer = Book.objects.filter(pk=book_id_docer).values_list("url_pdf")[0][0]
            print("1. url_pdf_docer =", url_pdf_docer)
            if url_pdf_docer == "no pdf link docer":
                print("1a. url_pdf_docer =", url_pdf_docer)
                context["url_pdf_docer"] = "no pdf link docer"
                context["message_docer"] = "NOT possible to download this book"

            elif url_pdf_docer == "no pdf link" or url_pdf_docer == "pdf link unfinished" or url_pdf_docer == "pdf link exist":
                print("1b. url_pdf_docer =", url_pdf_docer)
                author_book_docer = Book.objects.filter(pk=book_id_docer).values_list("author")[0][0]
                print("1. author_book_docer =", author_book_docer)
                # title_download_docer = book_values[-2]
                title_book_docer = Book.objects.filter(pk=book_id_docer).values_list("title")[0][0]
                print("1. title_download_docer =", title_download_docer)
                # language_download_docer = book_values[-1]
                language_book_docer = Book.objects.filter(pk=book_id_docer).values_list("language")[0][0]
                print("1. language_download_docer =", language_download_docer)

                book_scrap(author_book_docer, title_download_docer)
                pdf_url_download_docer = book_scrap.pdf_url_download_found
                print("pdf_url_download_docer =", pdf_url_download_docer)
                pdf_url_before = book_scrap.get_current_url
                print("pdf_url_before =", pdf_url_before)
                if pdf_url_download_docer ==  "no pdf link docer":
                    print("1a. pdf_url_download_docer =", pdf_url_download_docer)
                    serializer = BookPdfUrlSerializer(data={'url_pdf': pdf_url_download_docer}, partial=True)
                    serializer.save()
                    context["url_pdf_docer"] = "no pdf link docer"
                    context["message_docer"] = "NOT possible to download this book"

                elif pdf_url_download_docer == "pdf link unfinished":
                    print("1b. pdf_url_download_docer =", pdf_url_download_docer)
                    serializer = BookPdfUrlSerializer(data={'url_pdf': 'pdf link unfinished'}, partial=True)
                    serializer.save()
                    context["url_pdf_docer"] = "pdf link unfinished"
                    context["message_docer"] = "something went wrong searching unfinished, try later"

                elif pdf_url_download_docer == "pdf link exist":
                    print("1c. pdf_url_download_docer =", pdf_url_download_docer)
                    serializer = BookPdfUrlSerializer(data={'url_pdf': 'pdf link exist'}, partial=True)
                    serializer.save()
                    context["url_pdf_docer"] = "pdf link exist"
                    context["message_docer"] = "something went wrong link exist but download ufinished, try later"
                else:
                    print("1d. pdf_url_download_docer =", pdf_url_download_docer)
                    serializer = BookPdfUrlSerializer(data={'url_pdf': pdf_url_download_docer}, partial=True)
                    serializer.save()
                    context["url_pdf_docer_yes"] = pdf_url_download_docer
                    context["message_docer"] = "probably book downloaded, check folder downloads"
            else:
                context["url_pdf_docer_yes"] = url_pdf_docer
                print("url_pdf_docer_yes =", url_pdf_docer)

        else:
            book_id_libgen = download_book.book_id_download_value
            print("book_id_libgen =", book_id_libgen)
            book_values.append(book_id_libgen)
            url_pdf_docer = Book.objects.filter(pk=book_id_libgen).values_list("url_pdf")[0][0]
            if url_pdf_docer == "no pdf link docer":
                context["url_pdf_docer"] = "no pdf link docer"
                context["message_docer"] = "NOT possible to download this book"
            elif url_pdf_docer == "no pdf link" or url_pdf_docer == "pdf link unfinished" or url_pdf_docer == "pdf link exist":
                # author_book_libgen = download_book.author_download_value.split()[-1]
                author_book_libgen = Book.objects.filter(pk=book_id_libgen).values_list("author")[0][0].split()[-1]
                # book_values.append(author_book_libgen)
                # author_book_docer_full = "Oscar Wilde"
                author_book_docer = author_book_libgen
                print("2. author_book_docer =", author_book_docer)

                # title_download_libgen = download_book.title_download_value
                title_download_libgen = Book.objects.filter(pk=book_id_libgen).values_list("title")[0][0]
                # book_values.append(title_download_libgen)
                # title_download_docer = "Portret Doriana Graya"
                title_download_docer = title_download_libgen
                print("2. title_download_docer =", title_download_docer)

                # language_download_libgen = download_book.language_download_value
                language_download_libgen = Book.objects.filter(pk=book_id_libgen).values_list("language")[0][0]
                # book_values.append(language_download_libgen)
                # language_download_docer = "pl"
                language_download_docer = language_download_libgen
                print("2. language_download_docer =", language_download_docer)

                book_scrap(author_book_docer, title_download_docer)
                print("pdf_url_download_docer =", pdf_url_download_docer)
                if pdf_url_download_docer ==  "no pdf link docer":
                    print("")
                    serializer = BookPdfUrlSerializer(data={'url_pdf': pdf_url_download_docer}, partial=True)
                    serializer.save()
                    context["url_pdf_docer"] = "no pdf link docer"
                    context["message_docer"] = "NOT possible to download this book"

                elif pdf_url_download_docer == "pdf link unfinished":
                    print("pdf_url_download_docer = pdf link unfinished")
                    serializer = BookPdfUrlSerializer(data={'url_pdf': 'pdf link unfinished'}, partial=True)
                    serializer.save()
                    context["url_pdf_docer"] = "pdf link unfinished"
                    context["message_docer"] = "something went wrong searching unfinished, try later"

                elif pdf_url_download_docer == "pdf link exist":
                    print("pdf_url_download_docer = pdf link exist")
                    serializer = BookPdfUrlSerializer(data={'url_pdf': 'pdf link exist'}, partial=True)
                    serializer.save()
                    context["url_pdf_docer"] = "pdf link exist"
                    context["message_docer"] = "something went wrong link exist but download unfinished, try later"
                else:
                    print("pdf_url_download =", pdf_url_download_docer)
                    serializer = BookPdfUrlSerializer(data={'url_pdf': pdf_url_download_docer}, partial=True)
                    serializer.save()
                    context["message_docer"] = "probably book downloaded, check folder downloads"
            else:
                context["url_pdf_docer_yes"] = url_pdf_docer
                print("url_pdf_docer_yes =", url_pdf_docer)
    # return Response(context, template_name='download_book_doc.html', )
    # return HttpResponseRedirect(reverse('booksmart:downloadbook'))
    return Response(context, template_name='download_book_bot.html', )

