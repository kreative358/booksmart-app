import booksmart.views as views
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from os import environ
from booksearch.forms import BookSearch, GBAuthor
import os, re, json, time, requests, datetime
from booksmart.models import Book, Author, context_bm
from booksmart.forms import BookForm, AuthorForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.utils.html import format_html
from accounts.views_authorization import *
from booksearch.reqs import *
    

key=os.environ.get('API_KEY')
def addx_author(request):
    context = context_bm
 
    
    # form_a = a_account_view(request)
    # form_r = a_registration_view(request)
    # form_l = a_login_view(request)
    
    # context['login_form'] = form_l
    # context['registration_form'] = form_r
    # context['account_form'] = form_a
    current_url_name = request.path
    # currents.append(current_url_name)
    print('current_url_name', current_url_name)
    context['current_url'] = current_url_name
    context['author'] = ""
    context['message_a'] = ""
    
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

    print('491 wiki_idx', wiki_idx)            
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

def addauthor(request):
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
    }
    # print("\nauthor_c['author_name']:", author_c['author_name'])
    # new_author_name = author_c['author_name']
 
    new_author = Author(
            author_wiki_link_d = author_c['author_wiki_link_d'],
            author_wiki_link = author_c['author_wiki_link'],
            first_name = author_c['first_name'],
            middle_name = author_c['middle_name'],
            last_name = author_c['last_name'],
            author_name = author_c['author_name'],
            date_of_birth  = author_c['date_of_birth'],
            date_of_death = author_c['date_of_death'],
            wiki_idx = author_c['wiki_idx'],
            author_wiki_img = author_c['author_wiki_img'],
            user_num_a = author_c['user_num_a'],
            # created_by=Account.objects.filter(id=user.id).first(),
            owner=r_user,
    ) # middle_name = middle_name,

    
    new_author_name = new_author.author_name
    print(f'\nnew_author_name: {new_author_name}\n')
    try:
        books_author_c=Author.objects.filter(author_name=new_author_name)
        if books_author_c:
            print('req_author line 256')
            messages.info(request, "This author is in database")
            return redirect('booksmart:allauthors')
        else:
            new_author.save()
            print('req_author line 261')
            books = Book.objects.filter(author=new_author_name)
            # new_author_c = Author.objects.filter().last()
            # books = Book.objects.filter(author=new_author_name)
            # form_book = BookForm()
            if books:
                for book in books:
                    if book.author_c:
                        print('req_author line 272')
                        
                        # if book_form.is_valid:
                        #     book=form_book.save(commit=False)
                        #     book.author_c = new_author
                        #     book.save()
                        # else:
                        #     pass

                    else:
                        #if book.author == books_author_c.author_name:
                        book_author_c = book.author
                        author_author_c = Author.objects.filter(author_name=book_author_c).last()
                        book.author_c = author_author_c
                        # book.author_c = Author.objects.filter().last()
                        book.save()
                        print('req_author line 278')
            else:
                print('req_author line 280')

    except IntegrityError:
        new_author.save()
        print('req_author line 284')
    except ValidationError:
        new_author.save()
        print('req_author line 287')

    return HttpResponseRedirect(reverse('booksmart:allauthors'))
                




