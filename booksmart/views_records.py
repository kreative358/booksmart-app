import os, re, json, time, requests, datetime, random
from os import environ
from booksmart.models import url_img, url_img_author, Book, Author, BackgroundPoster, BackgroundVideo
from booksmart.forms import BookForm, AuthorForm, SearchRecord, BookChange, ItemsSearchForm, LibrarySearch, BackgroundFormPoster, BackgroundFormVideo
from accounts.models import Account
from booksmart.api.permissions import IsOwnerOrReadOnly #, IsOwnerIsAdminOrReadOnly

from django.contrib import messages

from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework import permissions
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


# @api_view(['GET', 'POST'])
# # @authentication_classes([])
# @renderer_classes([TemplateHTMLRenderer, JSONRenderer])
# @permission_classes([permissions.IsAuthenticated, ])
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
    # return Response(context, template_name='read_book.html', )
    return render(request, "read_book.html", context )


# @api_view(['GET', 'POST'])
# # @authentication_classes([])
# @renderer_classes([TemplateHTMLRenderer, JSONRenderer])
# @permission_classes([permissions.IsAuthenticated, ])
def read_book_ol(request, id):

    r_user = request.user
    current_url_name = request.path
    book = get_object_or_404(Book, pk=id)
    
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
    identities = []

    identities_1 = []
    identities_1.clear()
    idents_1 = []
    idents_1.clear()
    idents_title_1 = []
    idents_title_1.clear()
    idents_author_1 = []
    idents_author_1.clear()
    titles_idents_1 = []
    titles_idents_1.clear()

    idents_2 = []
    idents_2.clear()
    idents_title_2 = []
    idents_2.clear()
    idents_author_2 = []
    idents_2.clear()
    identities_2 = []
    idents_2.clear()
    titles_idents_2 = []
    idents_2.clear()

    if request.POST:
        formlib = LibrarySearch(request.POST)
        container = {}
        container.clear()
        context['cont'] = ""
        context['conts'] = ""


        use_title_author(context, formlib, book, identities_1, idents_title_1, idents_author_1, idents_1, titles_idents_1, identities)
        
        time.sleep(2)
        # container = {}
        # container.clear()
        container['mail'] = context['mail']
        container['pass'] = context['pass']
        container['searching'] = 'https://openlibrary.org/account/login'
        # container['title'] = title_to_search
        container['title'] = book.title
        if len(identities_1) > 0:
            # print('identities_1: ', identities_1) 
            ids = list(set(identities_1))
            # print('ids', ids)

            if len(ids) == 1:
                container_one = container
                container_one['link'] = f'https://openlibrary.org/borrow/ia/{ids[0]}?ref=ol'
                context['cont'] = container_one
                # print("context['cont']: ", context['cont'])
                # return Response(context, template_name='read_book.html', )

                # return Response(context, template_name='read_book_ol.html', )
                return render(request, "read_book_ol.html", context )

            elif len(ids) > 1:
                containers_many = []
                links = [f'https://openlibrary.org/borrow/ia/{ident}?ref=ol' for ident in ids]
                for link in links:
                    container_many = container
                    container_many['link'] = link   
                    containers_many.append(container_many)

                context['conts'] = containers_many
                # print("context['conts'][0]", context['conts'][0])
                # return Response(context, template_name='read_book.html', )

                # return Response(context, template_name='read_book_ol.html', )
                return render(request, "read_book_ol.html", context )
            else:
                print('6 no links')

                # context['message'] = 'Sorry, probably no this title to read for free'
                # return Response(context, template_name='read_book.html', ) 

        elif len(identities_1)==0:
            # print("len(identities)==0")
            titles_idents_2 = []
            # print("134 idents_1", idents_1)
            
            try:
                if len(idents_1) > 1:
                    try:
                        include_ident_1(idents_1, titles_idents_1, container, context, titles_idents_2)
                        if context_i1:
                            # print('143 context_i1')
                            context = context + context_i1
                            # return Response(context, template_name='read_book.html', )
                            
                            # return Response(context, template_name='read_book_ol.html', )
                            return render(request, "read_book_ol.html", context )
                        elif text:
                            print("145 NO context")

                    except Exception as e:
                        print("151 Exception as e:", e)
                    try:
                        include_ident_2(idents_1, titles_idents_2, container, context)
                        if context_i2:
                            context = context + context_i2
                            # return Response(context, template_name='read_book.html', )

                            # return Response(context, template_name='read_book_ol.html', )
                            return render(request, "read_book_ol.html", context )
                        elif text:
                            print("158 NO context")
                    except Exception as e:
                        print("160 Exception as e:", e)
            except Exception as e:
                print("127 Exception as e:", e)
        
            try:
                print("176 try")
                if idents_title_1 and indets_author_1:
                    idents_title_author_1(idents_title_1, indets_author_1)
                    if context_ta:
                        context = context + context_ta
                        # return Response(context, template_name='read_book.html', )

                        # return Response(context, template_name='read_book_ol.html', )
                        return render(request, "read_book_ol.html", context )
                    elif text:
                        print("172 NO context")
            except Exception as e:
                print("138 Exception as e:", e)

            # if len(idents_1) == 0:
            try:
                # print("use_title")
                use_title(context, formlib, book, identities_1, idents_title_1, idents_author_1, idents_1, titles_idents_1, identities)
                if len(identities_1) > 0:
                    # print('identities_1: ', identities_1) 
                    ids = list(set(identities_1))
                    # print('ids', ids)

                    if len(ids) == 1:
                        container_one = container
                        container_one['link'] = f'https://openlibrary.org/borrow/ia/{ids[0]}?ref=ol'
                        context['cont'] = container_one
                        # print("context['cont']: ", context['cont'])
                        # return Response(context, template_name='read_book.html', )

                        # return Response(context, template_name='read_book_ol.html', )
                        return render(request, "read_book_ol.html", context )

                    elif len(ids) > 1:
                        containers_many = []
                        links = [f'https://openlibrary.org/borrow/ia/{ident}?ref=ol' for ident in ids]
                        for link in links:
                            container_many = container
                            container_many['link'] = link   
                            containers_many.append(container_many)

                        context['conts'] = containers_many
                        # print("context['conts'][0]", context['conts'][0])
                        # return Response(context, template_name='read_book.html', )

                        # return Response(context, template_name='read_book_ol.html', )
                        return render(request, "read_book_ol.html", context )
                    else:
                        print('6 no links')
                #
                elif len(identities_1)==0:
                    # print("len(identities_1)==0")
                    titles_idents_2 = []
                    # print("134 idents_1", idents_1)
                    if len(idents_1) > 1:
                        try:
                            include_ident_1(idents_1, titles_idents_1, container, context, titles_idents_2)
                            if context_i1:
                                context = context + context_i1
                                # return Response(context, template_name='read_book.html', )

                                # return Response(context, template_name='read_book_ol.html', )
                                return render(request, "read_book_ol.html", context )

                            elif text:
                                print("204 NO context")
                        except Exception as e:
                            print("127 Exception as e:", e)

                        try:
                            include_ident_2(idents_1, titles_idents_2, container, context)
                            if context_i2:
                                context = context + context_i2
                                # return Response(context, template_name='read_book.html', )

                                # return Response(context, template_name='read_book_ol.html', )
                                return render(request, "read_book_ol.html", context )

                            else:
                                print("213 NO context")
                        except Exception as e:
                            print("131 Exception as e:", e)

                    # if idents_title_1 and indets_author_1:
                        # try:
                            # idents_title_author(idents_title_1, indets_author_1)
                        # except Exception as e:
                            # print("138 Exception as e:", e) 

            except Exception as e: 
                print("190 Exception", e)
                

            # else:
            try:
                # print("use_meta_title_author")
                use_meta_title_author(context, formlib, book, identities_2, idents_title_2, idents_author_2, idents_2, identities)

                if len(identities_2) > 0:
                    # print('identities_2: ', identities_2) 
                    ids = list(set(identities_2))
                    # print('2 ids', ids)

                    if len(ids) == 1:
                        container_one = container
                        container_one['link'] = f'https://openlibrary.org/borrow/ia/{ids[0]}?ref=ol'
                        context['cont'] = container_one
                        # print("context['cont']: ", context['cont'])
                        # return Response(context, template_name='read_book.html', )

                        # return Response(context, template_name='read_book_ol.html', )
                        return render(request, "read_book_ol.html", context )

                    elif len(ids) > 1:
                        containers_many = []
                        links = [f'https://openlibrary.org/borrow/ia/{ident}?ref=ol' for ident in ids]
                        for link in links:
                            container_many = container
                            container_many['link'] = link   
                            containers_many.append(container_many)

                        context['conts'] = containers_many
                        # print("context['conts'][0]", context['conts'][0])
                        # return Response(context, template_name='read_book.html', )

                        # return Response(context, template_name='read_book_ol.html', )
                        return render(request, "read_book_ol.html", context )

                    else:
                        print('6b no links')
                        
                        # context['message'] = 'Sorry, probably no this title to read for free'
                        # return Response(context, template_name='read_book.html', ) 

                elif len(identities_2)==0:
                    # print("len(identities_1)==0")
                    titles_idents_2 = []
                    # print("134 idents_1", idents_1)
                    if len(idents_1) > 1:
                        try:
                            include_ident_1(idents_1, titles_idents_1, container, context, titles_idents_2)
                            if context_i1:
                                context = context + context_i1
                                # return Response(context, template_name='read_book.html', )

                                # return Response(context, template_name='read_book_ol.html', )
                                return render(request, "read_book_ol.html", context )

                            elif text:
                                print("204 NO context")
                        except Exception as e:
                            print("127 Exception as e:", e)

                        try:
                            include_ident_2(idents_1, titles_idents_2, container, context)
                            if context_i2:
                                context = context + context_i2
                                # return Response(context, template_name='read_book.html', )

                                # return Response(context, template_name='read_book_ol.html', )
                                return render(request, "read_book_ol.html", context )

                            else:
                                print("213 NO context")
                        except Exception as e:
                            print("131 Exception as e:", e)

                    # if idents_title_1 and indets_author_1:
                    try:
                        print("300 try")
                        if idents_title_2 and indets_author_2:
                            idents_title_author_2(idents_title_2, indets_author_2)
                            if context_ta:
                                context = context + context_ta
                                # return Response(context, template_name='read_book.html', )

                                # return Response(context, template_name='read_book_ol.html', )
                                return render(request, "read_book_ol.html", context )

                            elif text:
                                print("172 NO context")
                        else:
                            # print("344 no book")
                            context['message_read'] = 'Sorry, probably no this title to read for free in openlibrary'
                            # return Response(context, template_name='read_book_ol.html', )

                    except Exception as e:
                        print("138 Exception as e:", e)
                    
            except Exception as e: 
                print("249 Exception", e)
            #context['message_read'] = 'Sorry, probably no this title to read for free'
            # print("209 no links")
        else:
            # print("6a no links")
            context['message_read'] = 'Sorry, probably no this title to read for free'
            # return Response(context, template_name='read_book.html', )

            # return Response(context, template_name='read_book_ol.html', )
            return render(request, "read_book_ol.html", context )

            # context['message'] = 'Sorry, probably no this title to read for free yet.'
            # return Response(context, template_name='read_book.html', ) 
        
        # else:
            # print('7 no links')
            # context['message'] = 'Sorry, probably no this title to read for free'
            # return Response(context, template_name='read_book.html', )

               
    else:
        formlib = LibrarySearch()
        context['search_title'] = formlib
    # return render(request, 'read_book.html', context_a)
    # return Response(context, template_name='read_book.html', )

    # return Response(context, template_name='read_book_ol.html', )
    return render(request, "read_book_ol.html", context )


@api_view(['POST', 'GET'])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([permissions.IsAuthenticated, ])
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


@api_view(['POST', 'GET'])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrReadOnly,])
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
    

@api_view(['POST', 'GET'])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrReadOnly,])
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

@api_view(['POST', 'GET'])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([permissions.IsAuthenticated,])
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
    


@api_view(['POST', 'GET'])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrReadOnly]) # ,permissions.IsAdminUser
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

@api_view(['POST', 'GET'])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrReadOnly]) #, permissions.IsAdminr_user
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


