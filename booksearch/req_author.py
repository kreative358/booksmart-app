import booksmart.views as views
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from os import environ
from booksearch.forms import BookSearch, GBAuthor
import os, re, json, time, requests, datetime
from booksmart.models import url_img, url_img_author, Book, Author, BackgroundPoster, BackgroundVideo
from booksmart.forms import BookForm, AuthorForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.utils.html import format_html
from accounts.views_authorization import *
from booksearch.reqs import *

key=os.environ.get('API_KEY')

context_main = {}

context_main['no_date'] = datetime.date(3000, 1, 1)
context_main['no_date_start'] = datetime.date(3000, 1, 1)
context_main['no_date_end'] = datetime.date(3000, 1, 1)
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

def addx_author(request):

    r_user = request.user
    current_url_name = request.path
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    context = context_main

    context['num_authors'] = num_authors
    context['num_books'] = num_books
    context['current_url'] = current_url_name
    context['author'] = ""
    context['message_a'] = ""
    
    no_date = '3000-01-01'
    context['no_date'] = r'3000-01-01'
    context['no_date_start'] = r'3000-01-01'
    context['no_date_end'] = r'3000-01-01'
    book_dict = {}
    author_search_form = GBAuthor(request.GET)
    
    if author_search_form.is_valid():
        author = author_search_form.cleaned_data['author']
        context["author"] = author
        book_dict['author'] = author
        language = author_search_form.cleaned_data['language']
        book_dict['language'] = language
        
    # else:
    #     context['message'] = f'Sorry, probably something went wrong, error {e}'
    #     return render(request, 'addx_author.html', context)
    author = book_dict['author']
    language = book_dict['language']
        
    req_author_id(author, language, book_dict)
    wiki_idx = book_dict['author_c']['wiki_idx']
    if wiki_idx ==  'no wiki_idx':
        author = book_dict['author']
        language = 'en'
        req_author_id(author, language, book_dict)
        wiki_idx = book_dict['author_c']['wiki_idx']
        if wiki_idx == 'no wiki_idx':
            a_reverse = author.split()
            author = ' '.join(a_reverse[::-1])
            req_author_id(author, language, book_dict)
            wiki_idx = book_dict['author_c']['wiki_idx']
            if wiki_idx == 'no wiki_idx':
                context['message_a'] = f'Sorry, probably there is no author {author} in wiki database'
                return render(request, 'addx_author.html', context)  
            else:
                book_dict['author_c']['author_name'] = author
                book_dict['author_c']['wiki_idx'] = wiki_idx
                book_dict['language'] = 'en'
                book_dict['author'] = book_dict['author_c']['author_name']
        else:
            book_dict['author_c']['wiki_idx'] = wiki_idx
            book_dict['language'] = 'en'
    else:    
        book_dict['author_c']['wiki_idx'] = wiki_idx

    # print('491 wiki_idx', wiki_idx)            
    if wiki_idx.startswith('Q'):
        req_author_date(wiki_idx, book_dict)
        # r_author_date = req_author_date(wiki_idx, book_dict)
        book_lang = book_dict['language']
        book_author = book_dict['author']#.replace(' ', '_')
        
        req_author_wiki_details(book_author, book_lang, book_dict)
        author_details = book_dict['author_c']['author_wiki_link']
        if author_details == 'no wikidata':
            book_lang = book_dict['language']
            book_author = book_dict['author_c']['full_name']
            req_author_wiki_details(book_author, book_lang, book_dict)
            author_details = book_dict['author_c']['author_wiki_link']
            if author_details == 'no wikidata':
                book_lang = 'en'
                book_author = book_dict['author_c']['full_name']
                req_author_wiki_details(book_author, book_lang, book_dict)
                author_details = book_dict['author_c']['author_wiki_link']
                if author_details == 'no wikidata':
                    book_lang = 'en'
                    book_author = book_dict['author_c']['author_name']
                    req_author_wiki_details(book_author, book_lang, book_dict)
                    author_details = book_dict['author_c']['author_wiki_link']
                    if author_details == 'no wikidata':
                        book_dict['author_c']['author_wiki_link'] == 'no wikidata'
                    else:
                        book_dict['author_c']['author_wiki_link'] = author_details
                    
                else:
                    book_dict['author_c']['author_wiki_link'] = author_details

            else:
                book_dict['author_c']['author_wiki_link'] = author_details
        else:
            book_dict['author_c']['author_wiki_link'] = author_details


        book_lang = book_dict['language']
        book_author = book_dict['author']
        req_author_img(book_author, book_lang, book_dict)
        author_img = book_dict['author_c']['author_wiki_img']
        if author_img == 'no img':
            book_lang = book_dict['language']
            book_author = book_dict['author_c']['full_name']
            req_author_img(book_author, book_lang, book_dict)
            author_img = book_dict['author_c']['author_wiki_img']
            if author_img == 'no img':
                book_lang = 'en'
                book_author = book_dict['author_c']['full_name']
                req_author_img(book_author, book_lang, book_dict)
                author_img = book_dict['author_c']['author_wiki_img']
                if author_img == 'no img':
                    book_lang = 'en'
                    book_author = book_dict['author_c']['author_name']
                    req_author_img(book_author, book_lang, book_dict)
                else:
                    book_dict['author_c']['author_wiki_img'] = author_img
            else:
                book_dict['author_c']['author_wiki_img'] = author_img

        else:
            book_dict['author_c']['author_wiki_img'] = author_img

        context['book_dict'] = book_dict
        return render(request, 'addx_author.html', context)
        
    elif not wiki_idx.startswith('Q'):
        book_dict['author_c'] = 'no author in wikidata'
        
        context['message_a'] = f'Sorry, probably there is no details about {book_author} in wiki database'
        return render(request, 'addx_author.html', context)  


    return render(request, 'addx_author.html', context)



from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from booksearch.api.serializers import NewAuthorSerializer
def addauthor_serializer(request):
    r_user = request.user
    authors_instances = []
    author_c = {
    'author_wiki_link_d': request.POST['author_wiki_link_d'],
    'author_wiki_link': request.POST['author_wiki_link'],
    'first_name': request.POST['first_name'],
    'middle_name': request.POST['middle_name'] ,
    'last_name': request.POST['last_name'],
    # author_name = f'{first_name} {last_name}'
    # author_name = f'{first_name} {middle_name} {last_name}' if middle_name != '' else f'{first_name} {last_name}'
    'author_name': request.POST['author_name'],
    'date_of_birth': request.POST['date_of_birth'],
    'date_of_death': request.POST['date_of_death'],
    'wiki_idx': request.POST['wiki_idx'],
    'author_wiki_img': request.POST['author_wiki_img'],
    'user_num_a': request.POST['user_num_a'],
    'owner': r_user.id,
    }

    # print("\nauthor_c =", author_c)
    new_author_c = author_c
    serializer = NewAuthorSerializer(data=new_author_c)
    initial_val = serializer.initial_data
    new_author_wiki_idx = initial_val["wiki_idx"]
    # print("new_author_wiki_idx =", new_author_wiki_idx)
    new_author_name = initial_val["author_name"]
    # print("new_author_name =", new_author_name)
    if serializer.is_valid():
        try:
            books_author_c=Author.objects.filter(wiki_idx=new_author_wiki_idx)
            if books_author_c:
                print('req_author line 256')
                messages.info(request, "This author is in database, you can try save with different wiki_idx ID")
                return redirect('booksmart:allauthors')
            else:
                author_instance = serializer.save()
                print("author_instance.author_name =", author_instance.author_name)
                new_author_name_instance = author_instance.author_name
                books = Book.objects.filter(author=new_author_name_instance)
                if books:
                    for book in books:
                        if book.author_c:
                            print('req_author line 272')

                        else:
                            #if book.author == books_author_c.author_name:
                            book_author_c = book.author
                            author_author_c = Author.objects.filter(author_name=book_author_c).last()
                            book.author_c = author_author_c
                            # book.author_c = Author.objects.filter().last()
                            book.save()
                            # print('req_author line 278')
                else:
                    print('req_author line 280')

        except IntegrityError:
                messages.info(request, "Something went wrong, please try again later")
                print("300 IntegrityError")
                # book_instance = serializer.save()
                return redirect('booksmart:allrecords')
        except ValidationError:
                messages.info(request, "Something went wrong, please try again later")
                print("305 ValidationError")
                # book_instance = serializer.save()
                return redirect('booksmart:allrecords')

    return HttpResponseRedirect(reverse('booksmart:allauthors'))



# def addauthor(request):
#     r_user = request.user
#     authors_instances = []
#     author_c = {
#     'author_wiki_link_d': request.POST['author_wiki_link_d'],
#     'author_wiki_link': request.POST['author_wiki_link'],
#     'first_name': request.POST['first_name'],
#     'middle_name': request.POST['middle_name'] ,
#     'last_name': request.POST['last_name'],
#     # author_name = f'{first_name} {last_name}'
#     # author_name = f'{first_name} {middle_name} {last_name}' if middle_name != '' else f'{first_name} {last_name}'
#     'author_name': request.POST['author_name'],
#     'date_of_birth': request.POST['date_of_birth'],
#     'date_of_death': request.POST['date_of_death'],
#     'wiki_idx': request.POST['wiki_idx'],
#     'author_wiki_img': request.POST['author_wiki_img'],
#     'user_num_a': request.POST['user_num_a'],
#     }
#     # print("\nauthor_c['author_name']:", author_c['author_name'])
#     # new_author_name = author_c['author_name']
 
#     new_author = Author(
#             author_wiki_link_d = author_c['author_wiki_link_d'],
#             author_wiki_link = author_c['author_wiki_link'],
#             first_name = author_c['first_name'],
#             middle_name = author_c['middle_name'],
#             last_name = author_c['last_name'],
#             author_name = author_c['author_name'],
#             date_of_birth  = author_c['date_of_birth'],
#             date_of_death = author_c['date_of_death'],
#             wiki_idx = author_c['wiki_idx'],
#             author_wiki_img = author_c['author_wiki_img'],
#             user_num_a = author_c['user_num_a'],
#             # created_by=Account.objects.filter(id=user.id).first(),
#             owner=r_user,
#     ) # middle_name = middle_name,

    
#     new_author_name = new_author.author_name
#     # print(f'\nnew_author_name: {new_author_name}\n')
#     try:
#         books_author_c=Author.objects.filter(author_name=new_author_name)
#         if books_author_c:
#             print('req_author line 256')
#             messages.info(request, "This author is in database")
#             return redirect('booksmart:allauthors')
#         else:
#             new_author.save()
#             # print('req_author line 261')
#             books = Book.objects.filter(author=new_author_name)
#             # new_author_c = Author.objects.filter().last()
#             # books = Book.objects.filter(author=new_author_name)
#             # form_book = BookForm()
#             if books:
#                 for book in books:
#                     if book.author_c:
#                         print('req_author line 272')
                        
#                         # if book_form.is_valid:
#                         #     book=form_book.save(commit=False)
#                         #     book.author_c = new_author
#                         #     book.save()
#                         # else:
#                         #     pass

#                     else:
#                         #if book.author == books_author_c.author_name:
#                         book_author_c = book.author
#                         author_author_c = Author.objects.filter(author_name=book_author_c).last()
#                         book.author_c = author_author_c
#                         # book.author_c = Author.objects.filter().last()
#                         book.save()
#                         # print('req_author line 278')
#             else:
#                 print('req_author line 280')

#     except IntegrityError:
#         new_author.save()
#         print('req_author line 284')
#     except ValidationError:
#         new_author.save()
#         print('req_author line 287')

#     return HttpResponseRedirect(reverse('booksmart:allauthors'))
                




