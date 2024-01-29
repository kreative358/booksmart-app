from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from os import environ
from booksearch.forms import BookSearch
import os, re, json, time, requests, datetime
from booksmart.models import url_img, url_img_author, Book, Author, BackgroundPoster, BackgroundVideo, BackgroundMusic
from accounts.models import Account
from booksmart.forms import BookForm, AuthorForm
from booksearch.reqs import *
#from booksmart.views_acc import *
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib import messages

from django.utils.regex_helper import _lazy_re_compile

from django.utils.html import format_html
from django.urls import reverse

from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication

key=os.environ.get('API_KEY')

def context_bm_booksearch():
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
        print(f"req_book no Book.objects.all(): except Exception as {err}")
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
        print(f"req_book no Author.objects.all(): Exception as {err}")
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
        print(f"req_book no BackgroundPoster.objects.filter().last(): Exception as {err}")
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
        print(f"req_book no BackgroundVideo.objects.filter().last(): Exception as {err}")
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
        print(f"req_book no BackgroundMusic.objects.filter().last(): Exception as {err}")        
        context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_main['music_type_1'] = "mp3"
        context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_main['music_type_2'] = "mp3"
        
    context_bm_booksearch.context_main = context_main
    return context_main 


@api_view(['GET', ])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication]) 
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def addx_book(request): 
    
    r_user = request.user

    current_url_name = request.path
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    # context = context_main
    context_bm_booksearch()    
    context = context_bm_booksearch.context_main

    context['num_books'] = num_books
    context['num_authors'] = num_authors
    
    context['current_url'] = current_url_name

    # context['no_date'] = datetime.date(3000, 1, 1)
    no_date = '3000-01-01'
    # context['no_date'] = *no_date
    context['no_date'] = r'3000-01-01'
    key=os.environ.get('API_KEY')
        
    form = BookSearch(request.GET)
    context['form_search_gb'] = "no"
    context['parameters'] = ""
    context['message'] = ""
    params_str = ""

    if form.is_valid():
        context['form_search_gb'] = "yes"
        search_title = form.cleaned_data['intitle']
        search_author = form.cleaned_data['inauthor']
        search_query = form.cleaned_data['search_query']
        search_volumeId = form.cleaned_data["volumeId"]
        search_download = form.cleaned_data["download"]
        search_filter = form.cleaned_data["search_filter"]
        search_Languages = form.cleaned_data['langRestrict']
        search_maxResults = form.cleaned_data["search_maxResults"]
        search_orderBy = form.cleaned_data['orderBy']
        search_startIndex = form.cleaned_data["search_startIndex"]
        search_inpublisher = form.cleaned_data["search_inpublisher"]
        search_bl_volumeId = form.cleaned_data["bl_volumeId"]
        
       
    googleapikey = os.environ.get('API_KEY')
    keywords_fields = {
        'intitle': search_title,
        'inauthor': search_author,
        'query': search_query,
        'volumeId': search_volumeId,
        'download': search_download,
        'filter': search_filter,
        'langRestrict': search_Languages,
        'maxResults': search_maxResults,
        'orderBy': search_orderBy,
        'startIndex': search_startIndex,
        'inpublisher': search_inpublisher,
        'bl_volumeId':search_bl_volumeId, 
    }  


    b_link = []
    bl_link = []
    if keywords_fields["volumeId"] != '':
        # print('len(keywords_fields["bl_volumeId"])', len(keywords_fields["bl_volumeId"]))
        if len(keywords_fields["volumeId"]) == 12:
            b_link.append(keywords_fields["volumeId"])
            

    elif keywords_fields["bl_volumeId"] != '':
        url = keywords_fields["bl_volumeId"]
        reg = r"^http:\/\/?\/|.*id=([A-Za-z0-9._-]{12})+?[\/].*|.*id=([A-Za-z0-9._-]{12})+?[&].*|.*\/([A-Za-z0-9._-]{12})\/.*|.*\/([A-Za-z0-9._-]{12})?.*$"
        serch_text = r"[A-Za-z0-9._-]{12}"
        try:
            id_book = ''.join(''.join(el for el in i if el != '') for i in re.findall(reg, url))
            # id_book = ''.join(''.join(el for el in i if el != '') for i in re.findall(reg, txt))
            if id_book != '' and len(id_book) == 12:
                bl_link.append(keywords_fields["bl_volumeId"])
                # keywords_fields["bl_volumeId"] = f'"{id_book}"'

            else:
                context['message'] = f'Incorrect link, error description: {e}'
                return Response(context, template_name='addx_book.html', )
            """
            if re.findall("id=.+?[&]", url):
                id_book = re.findall("id=.+?[&]", url)
                key_book = id_book[0][3:-1]
                b_link.append(key_book)
                keywords_fields["bl_volumeId"] = key_book
            elif not re.findall("id=.+?[&]", url):
                id_book = url[-12:]
                key_book = id_book
                # print('key_book', key_book)
                b_link.append(key_book)
                keywords_fields["bl_volumeId"] = key_book """
        except Exception as e:
            context['message'] = f'Incorrect link, error description: {e}'
            return Response(context, template_name='addx_book.html', )
            # return render(request, 'addx_book.html', context)
    
    
    keywords_fields_items = list(keywords_fields.items())
    keywords_fields_values = list(keywords_fields.values())
        
    parameters_list = []
    print('218 parameters_list =', parameters_list)
    # print('b_link', b_link)
    if b_link != []:
        parameters_list.append(('volumeId', b_link[0]))
    
    for key, value in keywords_fields_items:
        if value != '' and value != None:
            parameters_list.append((key, value))
        else:
            pass

    parameters_dict = dict(parameters_list)
    if len(parameters_list)==0:      
        context['message'] = 'It is necessary to fill in at least one field'
        return Response(context, template_name='addx_book.html', )


    elif len(parameters_list) == 1:
        context['parameters'] = ""
        context['message'] = ""
        if parameters_list[0][0] == 'intitle':
            params_str = f'q={parameters_list[0][0]}:"{parameters_list[0][1].replace(" ", "+")}"'
            # params_str = f'q="{parameters_list[0][1].replace(" ", "+")}"'

        elif parameters_list[0][0] == 'inauthor':
            params_str = f'q={parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "+")}'
            
        elif parameters_list[0][0] == 'query':
            params_str = f'q={parameters_list[0][1].replace(" ", "+")}'
        
        # else:
        #     params_str = f'q={parameters_list[0][1]}'
        else:
            context['message'] = 'Probably something was wrong with parameters try again'
            return Response(context, template_name='addx_book.html', )
    
    elif len(parameters_list) == 2:
        context['parameters'] = ""
        context['message'] = ""
        if parameters_list[0][0] =='intitle' and parameters_list[1][0] == 'inauthor':
            params_pre_1 = f'q=intitle:{parameters_list[0][1].replace(" ", "+")}' 
            params_pre_2 = f'&{parameters_list[1][0]}={parameters_list[1][1].replace(" ", "+")}'
            params_str = params_pre_1 + params_pre_2 

        elif parameters_list[0][0] =='intitle' and parameters_list[1][0] != 'inauthor' and parameters_list[1][0] != 'query' :
            # params_pre_1 = f'q={parameters_list[0][1].replace(" ", "_")}' 
            params_pre_1 = f'q=intitle:{parameters_list[0][1].replace(" ", "+")}&'
            params_pre_2 = f'{parameters_list[1][0]}={parameters_list[1][1]}'
            params_str = params_pre_1 + params_pre_2

        elif parameters_list[0][0] =='intitle' and parameters_list[1][0] == 'query':
            params_pre_1 = f'q=intitle:{parameters_list[1][1].replace(" ", "+")}'# + f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}'
            # params_pre_2 =  f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "+")}'
            params_str = params_pre_1

        elif parameters_list[0][0] == 'inauthor' and parameters_list[1][0] == 'query':
            params_pre_1 = f'q={parameters_list[1][1].replace(" ", "+")}' #+ f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}'
            params_pre_2 = f'+{parameters_list[0][0]}:{parameters_list[0][1]}' 
            params_str = params_pre_1 + params_pre_2

        elif parameters_list[0][0] !='intitle' and parameters_list[0][0] != 'inauthor' and parameters_list[0][0] == 'query' :
            params_pre_1 = f'q={parameters_list[0][1].replace(" ", "+")}'
            params_pre_2 = f'&{parameters_list[1][0]}:{parameters_list[1][1]}'
            params_str = params_pre_1 + params_pre_2


        elif parameters_list[0][0] == 'inauthor' and parameters_list[1][0] != 'query' :
            params_pre_1 = f'q={parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "+")}'
            # params_pre_1 = f'q={parameters_list[0][1].replace(" ", "_")}' #+ f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}'
            # params_pre_1 =  f'q={parameters_list[0][0]}:{parameters_list[0][1].replace(" ", f"+{parameters_list[0][0]}:")}'
            params_pre_2 = f'&{parameters_list[1][0]}={parameters_list[1][1]}'
            params_str = params_pre_1 + params_pre_2

        elif parameters_list[0][0] != 'inauthor' and parameters_list[0][0] !='intitle' and parameters_list[0][0] != 'query' :
            params_pre_1 = f'q={parameters_list[0][1]}'#:{parameters_list[0][1]}'
            params_pre_2 = f'&{parameters_list[1][0]}:{parameters_list[1][1]}'
            params_str = params_pre_1 + params_pre_2
        # else:
        #     params_pre_1 = f'q={parameters_list[0][1]}'
        #     params_pre_2 = f'&{parameters_list[1][0]}={parameters_list[1][1]}'
        #     params_str = params_pre_1 + params_pre_2
        else:
            context['message'] = 'Probably something was wrong with parameters try again'
            return Response(context, template_name='addx_book.html', )
    
    # parameters_list=[(k, f'{v.replace(" ", "+")}') if type(v) is str and k != 'bookList' else (k, v) for k, v in parameters_list 
    elif len(parameters_list) == 3:
        context['parameters'] = ""
        context['message'] = ""
        params_str = ""
        if parameters_list[0][0] =='intitle' and parameters_list[1][0] == 'inauthor' and parameters_list[2][0] == 'query' :
            params_pre_1 = f'q=intitle:{parameters_list[0][1].replace(" ", "+")}'
            params_pre_2 = f'&inauthor={parameters_list[1][1].replace(" ", "+")}'  
            # params_pre_3 = f'+{parameters_list[1][0]}:{parameters_list[1][1].replace(" ", "_")}'
            params_str = params_pre_1 + params_pre_2 # + params_pre_3
            #params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[2:]])
            # print('3a.', params_str)

        elif parameters_list[0][0] =='intitle' and parameters_list[1][0] == 'inauthor' and parameters_list[2][0] != 'query':
            params_pre_1 = f'q=intitle:{parameters_list[0][1].replace(" ", "+")}'

            # params_pre_1 = f'q={parameters_list[0][0]}:"{parameters_list[0][1].replace(" ", "+")}"&'
            # params_pre_2 = f'+{parameters_list[1][0]}:{parameters_list[1][1].replace(" ", "_")}'

            params_pre_2 = f'&inauthor={parameters_list[1][1].replace(" ", "+")}'
            params_pre_3 = f'&{parameters_list[2][0]}={parameters_list[2][1]}'
            # params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            params_str = params_pre_1 + params_pre_2 + params_pre_3
            # print('3b.', params_str)

        elif parameters_list[0][0] == 'intitle' and parameters_list[1][0] != 'inauthor' and  parameters_list[1][0] != 'query':
            # params_pre_1 = f'q={parameters_list[0][1].replace(" ", "_")}' + f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}&'
            params_pre_1 = f'q=intitle:{parameters_list[0][1].replace(" ", "+")}&' #+ f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}&'
            params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            # params_pre_1 = f'+{parameters_list[0][0]}:{parameters_list[0][1]}&'
            # params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            params_str = params_pre_1 + params_pre_2
            # print('3c.', params_str)
        # elif parameters_list[0][0] !='intitle' and parameters_list[0][0] == 'inauthor':
        elif parameters_list[0][0] == 'inauthor' and  parameters_list[1][0] != 'query':
            # params_pre_1 = f'q={parameters_list[0][1].replace(" ", "_")}' + f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}&'
            params_pre_1 = f'q=inauthor:{parameters_list[0][1].replace(" ", "+")}&' #+ f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}&'
            params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            # params_pre_1 = f'+{parameters_list[0][0]}:{parameters_list[0][1]}&'
            # params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            params_str = params_pre_1 + params_pre_2
            # print('3c.', params_str)


        elif parameters_list[0][0] == 'query':
            params_pre_1 = f'q={parameters_list[0][1].replace(" ", "+")}&'
            params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            params_str = params_pre_1 + params_pre_2
            # print('3e.', params_str)

        # !!!
        elif parameters_list[0][0] =='intitle' and parameters_list[1][0] == 'query':
            params_pre_1 = f'q=intitle:{parameters_list[0][1].replace(" ", "+")}' #+ f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}'
            # params_pre_2 = f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}&'
            params_pre_3 = f'&{parameters_list[2][0]}:{parameters_list[2][1]}'
            params_str = params_pre_1 + params_pre_3

        elif parameters_list[0][0] == 'inauthor' and parameters_list[1][0] == 'query':
            params_pre_1 = f'q=inauthor:{parameters_list[0][1].replace(" ", "+")}' #+ f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}'
            # params_pre_2 = f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "+")}&'
            params_pre_3 = f'{parameters_list[2][0]}={parameters_list[2][1]}'
            params_str = params_pre_1 + params_pre_3

        elif parameters_list[0][0] !='intitle' and parameters_list[0][0] != 'inauthor' and parameters_list[0][0] != 'query':
            params_pre_1 = f'q={parameters_list[0][1].replace(" ", "+")}&'
            params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            params_str = params_pre_1 + params_pre_2
            # print('3e.', params_str)
        else:
            context['message'] = 'Probably something was wrong with parameters try again'
            return Response(context, template_name='addx_book.html', )


    elif len(parameters_list) > 3:
        context['parameters'] = ""
        context['message'] = ""
        params_str = ""

        if parameters_list[0][0] =='intitle' and parameters_list[1][0] == 'inauthor' and parameters_list[2][0] == 'query' :
            params_pre_1 = f'q=intitle:{parameters_list[0][1].replace(" ", "+")}' 
            # params_pre_2 = f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "+")}'  
            params_pre_3 = f'&inauthor={parameters_list[1][1].replace(" ", "+")}&'
            params_pre_4 = '&'.join([f'{k}={v}' for k, v in parameters_list[3:]])
            params_str = params_pre_1 + params_pre_3 + params_pre_4
            #params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[2:]])
            # print('4a.', params_str)

        elif parameters_list[0][0] =='intitle' and parameters_list[1][0] == 'inauthor' and parameters_list[2][0] != 'query':
            params_pre_1 = f'q=intitle:{parameters_list[0][1].replace(" ", "+")}'
            params_pre_2 = f'&inauthor={parameters_list[1][1].replace(" ", "+")}&'            
            
            # params_pre_1 = f'q={parameters_list[1][0]}:"{parameters_list[1][1].replace(" ", "+")}"'
            # params_pre_2 = f'+{parameters_list[0][1].replace(" ", "+")}&'
            # params_pre_3 = f'&{parameters_list[2][0]}:{parameters_list[2][1]}'
            params_pre_3 = f'&'.join([f'{k}={v}' for k, v in parameters_list[2:]])
            # params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            params_str = params_pre_1 + params_pre_2 + params_pre_3
            # print('4b.', params_str)

        # elif parameters_list[0][0] !='intitle' and parameters_list[0][0] == 'inauthor':
        elif parameters_list[0][0] == 'intitle' and  parameters_list[1][0] != 'query':
            params_pre_1 = f'q=intitle:{parameters_list[0][1].replace(" ", "+")}&'         
            # params_pre_1 = f'q={parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "+")}&' #+ f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}&'
            params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            # params_pre_1 = f'+{parameters_list[0][0]}:{parameters_list[0][1]}&'
            # params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            params_str = params_pre_1 + params_pre_2
            # print('4c.', params_str)

        # !!!
        elif parameters_list[0][0] == 'inauthor' and  parameters_list[1][0] != 'query':
            params_pre_1 = f'q=inauthor:{parameters_list[0][1].replace(" ", "+")}&' #+ f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}&'
            params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            # params_pre_1 = f'+{parameters_list[0][0]}:{parameters_list[0][1]}&'
            # params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            params_str = params_pre_1 + params_pre_2
            # print('4c.', params_str)

        elif parameters_list[0][0] == 'inauthor' and parameters_list[1][0] == 'query' :
            # params_pre_1 = f'q={parameters_list[0][0]}:"{parameters_list[0][1].replace(" ", "+")}"+'
            params_pre_1 = f'q=inauthor:{parameters_list[0][1].replace(" ", "+")}' #+ f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "_")}'
            # params_pre_2 = f'&inauthor={parameters_list[0][1].replace(" ", "+")}&'
            params_pre_3 = '&'.join([f'{k}={v}' for k, v in parameters_list[2:]])
            params_str = params_pre_1 + params_pre_3

        elif parameters_list[0][0] == 'query':
            params_pre_1 = f'q={parameters_list[0][1].replace(" ", "+")}&'
            params_pre_2 = '&'.join([f'{k}={v}' for k, v in parameters_list[1:]])
            params_str = params_pre_1 + params_pre_2
            # print('4d.', params_str)

        elif parameters_list[0][0] =='intitle' and parameters_list[1][0] == 'query':
            params_pre_1 = f'q={parameters_list[1][0]}&intitle={parameters_list[1][1].replace(" ", "+")}'
            params_pre_2 = f'+{parameters_list[0][0]}:{parameters_list[0][1].replace(" ", "+")}&' 

            # params_pre_2 = f'+{parameters_list[0][0]}:"{parameters_list[0][1].replace(" ", "+")}"&'
            params_pre_3 = f'&'.join([f'{k}={v}' for k, v in parameters_list[2:]])
            params_str = params_pre_1 + params_pre_2 + params_pre_3
            # print('4e.', params_str)


        elif parameters_list[0][0] !='intitle' and parameters_list[0][0] != 'inauthor' and parameters_list[0][0] != 'query':
            params_pre_1 = f'q={parameters_list[0][1]}' + f'+{parameters_list[0][0]}:{parameters_list[0][1]}&'
            params_pre_2 = f'&'.join([f'{k}={v}' for k, v in parameters_list[2:]])
            params_str = params_pre_1 + params_pre_2
        else:
            context['message'] = 'Probably something was wrong with parameters try again'
            return Response(context, template_name='addx_book.html', )
    
    else:
    #     params_pre_1 = f'q="{parameters_list[0][1].replace(" ", "+")}"&'
    #     params_pre_2 = f'&'.join([f'{k}={v}' for k, v in parameters_list[2:]])
    #     params_str = params_pre_1 + params_pre_2
            # raise ValidationError('3. It is necessary to fill in at least one field')
        parameters = ',<br>'.join([': '.join([str(e) for e in el]) for el in parameters_list])
        context['parameters'] = parameters
        context['message'] = 'Probably something was wrong with parameters try again'
        return Response(context, template_name='addx_book.html', )
        # return render(request, 'addx_book.html', context)
        
    # if 'volumeId' in parameters_dict.keys():
        # params_string = f'q="{b_link[0]}"&maxResults=10'
        # parameters = f'"{parameters_list[0][0]}: {parameters_list[0][1]}",<br>maxResults:10"'
    if 'volumeId' in parameters_dict.keys():
        params_string = f'q="{b_link[-1]}"&maxResults=4'
        parameters_str = f'{parameters_list[0][0]}: {parameters_list[0][1]}'
        # parameters = ', '.join([': '.join([str(e) for e in el]) for el in parameters_list])
        parameters = parameters_str.replace('volumeId', 'googlebooks-id')
        context['parameters'] = parameters
    if 'bl_volumeId' in parameters_dict.keys():
        params_string = f'q="{bl_link[-1]}"&maxResults=4'
        parameters = 'googlebooks-link: pasted link'
        context['parameters'] = parameters
        # params_string = f"{'/'}{b_link[0]}"
    elif 'volumeId' not in parameters_dict.keys() and 'bl_volumeId' not in parameters_dict.keys():
        parameters_str = ',<br>'.join([': '.join([str(e) for e in el]) for el in parameters_list])
        parameters = parameters_str.replace('intitle', 'title').replace('inauthor', 'author').replace('query', 'search').replace('download', 'epub').replace('langRestrict', 'language').replace('maxResults', 'max-results').replace('orderBy', 'in-order').replace('inpublisher', 'publisher')
        try:
            if parameters_list != [] and parameters_list[0][0] != 'volumeId':
                # print("602 parameters_list", parameters_list)
                print("487 params_str =", params_str)
                params_string = params_str.replace('"', '')
                #parameters = ',<br>'.join([': '.join([str(e) for e in el]) for el in parameters_list])
                context['parameters'] = parameters
            else:
                context['parameters'] = parameters
                context['message'] ='Something was wrong try again, incorrect parameters to check'
                return Response(context, template_name='addx_book.html', )
                # return render(request, 'addx.html', context)
            
        except:
            context['parameters'] = parameters
            context['message'] = 'Sorry, probably no books match that search terms in googlebooks.'
            return Response(context, template_name='addx_book.html', )
            # return render(request, 'addx_book.html', context)    


    # print('params_string', params_string)

    search_url = f"https://www.googleapis.com/books/v1/volumes?{params_string}"

    googleapikey=os.environ.get('API_KEY')
    print('search_url', search_url)
    r = requests.get(url=search_url, params = {'key': googleapikey})

    if r.status_code != 200:
        context['message'] = f'Sorry, there seems to be an issue with Google Books right now, r.status_code = {r.status_code}'
        return Response(context, template_name='addx_book.html', )
        # return render(request, 'addx_book.html', context)
        
    data = r.json()    
    
    # if data == None:
    if not data:
        context['totalItems'] = 0
        context['val_total'] = 0
        context['message'] = 'Sorry, probably threre is no books in google books match that search terms: '
        return Response(context, template_name='addx_book.html', )
        # return render(request, 'addx_book.html', context)
    elif data:    
        try:
            context["data_items"] = data["items"]
            if len(context["data_items"]) == 0:
                context['totalItems'] = 0
                context['val_total'] = 0
                context['message'] = 'Sorry, probably there is no books match that search term in google books'
                return render(request, 'addx.html', context)
            elif len(context["data_items"]) > 0:
                founded_books=context["data_items"]
                # # print("data['totalItems']", data['totalItems'])
                context['totaItems'] = data['totalItems']
                context['val_total'] = data['totalItems']

        except:       
            # # print('no data["items"]')
            context['message'] = 'Sorry, probably threre is no books in google books match that search term.'
            return Response(context, template_name='addx_book.html', )
            # return render(request, 'addx_book.html', context)
            
    
    # # print("data['totalItems']", data['totalItems'])

    # # print("data['totalItems']", data['totalItems'])
    context['totaItems'] = data['totalItems']
    context['val_total'] = data['totalItems']

    
    founded_books_number = data['totalItems']
    # # print('founded_books_number', founded_books_number)
    
    # # print(f"\nlen(data['items']) = {len(data['items'])}\n")
    
    founded_books = data['items']

    books = []
    books_list = []
    books_out = []
    books_dict_list = []

    
    if founded_books:
        try:  
            i=0  
            for book in founded_books:
                i+=1
                # # print('\n466 req_book(book, founded_books_number)')
                req_book(book, founded_books_number)
                # r_book = req_book(book, founded_books_number)
                book_dict = req_book(book, founded_books_number)
                if book_dict == {}:
                    pass
                else:
                    book_dict['user_num_ba'] = r_user.id
                    books.append(book_dict)
                

            book_info = json.dumps(books[0], indent=4, sort_keys=False)
            # # print('\nbook_info', book_info)
            num_books_result = len(books)
            filtered_books = books

            context['filtered_books'] = filtered_books
            context['num_books_result'] = num_books_result

            paginated_filtered_books = Paginator(filtered_books, 40)  # filtered_books.qs
            page_number = request.GET.get('page')
            book_page_obj = paginated_filtered_books.get_page(page_number)
            context['book_page_obj'] = book_page_obj
            return Response(context, template_name='addx_book.html', )
            # return render(request, 'addx_book.html', context)
                
        except Exception as e:
            print(f'Error req addx line 544: {e}')
            context['message'] = f'Sorry, probably something went wrong, error {e}'
            return Response(context, template_name='addx_book.html', )
            # return render(request, 'addx_book.html', context)


    elif not founded_books:
        print('no books[0]')
        context['message'] = 'Sorry, probably threre is no books in google books match that search term'
        return Response(context, template_name='addx_book.html', )
        # return render(request, 'addx_book.html', context)

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from booksearch.api.serializers import NewBookSerializer
def addbook_serializer(request):
    r_user = request.user
    all_books = Book.objects.all()
    book = {
    'google_id': request.POST['google_id'],
    'title': request.POST['title'],
    'author': request.POST['author'],
    'category': request.POST['category'],
    'summary': request.POST['summary'],
    'published': request.POST['published'],
    'preview_link': request.POST['preview_link'],
    'language': request.POST['language'],
    'imageLinks': request.POST['imageLinks'],
    'selfLink': request.POST['selfLink'],
    'isbn': request.POST['isbn'],
    'epub':  request.POST['epub'],
    'embeddable': request.POST['embeddable'],
    'preview_link_new': request.POST['preview_link_new'],
     'user_num_b': str(r_user.id),
     'surname': request.POST['author'].split()[-1] if request.POST['author'] else '',
     'owner': r_user.id,
    }
    # print("\nbook =", book)
    new_book = book
    # print("\nnew_book =", new_book)
    serializer = NewBookSerializer(data=new_book)
    # print("serializer =", serializer)
    initial_val = serializer.initial_data
    new_book_google_id = initial_val["google_id"]
    # print("new_book_google_id =", new_book_google_id)
    if serializer.is_valid():
        
        try:
            check_new_book = Book.objects.filter(google_id=new_book_google_id)
            # check_new_book = Book.objects.filter(google_id=initial_val.google_id)
            if check_new_book:
                messages.warning(request, "1. This book is already in the database.")
                return redirect('booksmart:allrecords')
            else:
                book_instance = serializer.save()
                print("book_instance.title =", book_instance.title)
                new_book_google_id_instance = book_instance.google_id

                try:
                    new_book_add = Book.objects.filter(google_id=new_book_google_id_instance).last()
                    # new_book_add = Book.objects.filter().last()
                    new_book_add_author = new_book_add.author
                    author_c_new_book = Author.objects.filter(author_name=new_book_add_author).last()
                    if author_c_new_book:
                        book_instance.author_c = author_c_new_book
                        book_instance.save()
                        print('req_book line 578')
                    else:
                        print('req_book line 580')
                        
                    
                except Exception as e:
                    print(f'req_book line 602, error {e}')

                # try:
                #     new_book_add = Book.objects.filter(google_id=new_book_google_id_instance).last()
                #     new_book_add = Book.objects.filter().last()
                #     new_book_add_author = new_book_add.author
                #     author_c_new_book = Author.objects.filter(author_name=new_book_add_author).last()
                #     if author_c_new_book:
                #         new_book_add.author_c = author_c_new_book
                #         new_book_add.save()
                #         print('req_book line 578')
                #     else:
                #         print('req_book line 580')
                        
                    
                # except Exception as e:
                #     print(f'req_book line 602, error {e}')


        except IntegrityError:
            if Book.objects.filter(google_id=new_book_google_id):
                messages.info(request, "This book is in database")
                # return redirect('/booksmart/allrecords/')
                return redirect('booksmart:allrecords')
            else:
                book_instance = serializer.save()
                # messages.info(request, f"Something went wrong, reason {IntegrityError}")
                messages.info(request, "Something went wrong, please try again later")

                # book_instance = serializer.save()
                return redirect('booksmart:allrecords')
        except ValidationError:
            if Book.objects.filter(google_id=new_book_google_id):
                messages.info(request, "This book is in database")
                # return redirect('/booksmart/allrecords/')
                return redirect('booksmart:allrecords')
            else:
                # messages.info(request, f"Something went wrong, reason {ValidationError}")
                messages.info(request, "Something went wrong, please try again later")
                book_instance = serializer.save()
                return redirect('booksmart:allrecords')

    else:
        # print("serializer.data =", serializer.data)
        messages.info(request, "Something is wrong with book data")
        print("serializer.errors =", serializer.errors)
        return redirect('booksmart:allrecords')
    return HttpResponseRedirect(reverse('booksmart:allrecords'))
        


# def addbook(request):
#     r_user = request.user
    
#     all_books = Book.objects.all()
    
#     book = {
#     'google_id': request.POST['google_id'],
#     'title': request.POST['title'],
#     'author': request.POST['author'],
#     'category': request.POST['category'],
#     'summary': request.POST['summary'],
#     'published': request.POST['published'],
#     'preview_link': request.POST['preview_link'],
#     'language': request.POST['language'],
#     'imageLinks': request.POST['imageLinks'],
#     'selfLink': request.POST['selfLink'],
#     'isbn': request.POST['isbn'],
#     'epub':  request.POST['epub'],
#     'embeddable': request.POST['embeddable'],
#     'preview_link_new': request.POST['preview_link_new'],

#     }
#     # print("book['published']", book['published'])
#     # book_pub = book['published']
#     # new_book_pub = book_pub.strftime('%m/%d/%Y')
#     # book['published'] = new_book_pub
#     print("\naddbook book =", book)
#     new_book = Book(
#         google_id=book['google_id'],
#         title=book['title'],
#         author=book['author'],
#         category=book['category'],
#         summary=book['summary'],
#         published=book['published'],
#         preview_link=book['preview_link'],
#         language=book['language'],
#         imageLinks=book['imageLinks'],
#         selfLink=book['selfLink'],
#         isbn=book['isbn'],
#         epub=book['epub'],
#         embeddable=book['embeddable'],
#         preview_link_new=book['preview_link_new'],
#         user_num_b=r_user.id,
#         surname=book['author'].split()[-1] if book['author'] else '',
#         # created_by=Account.objects.filter(id=user.id).first(),
#         # owner=Account.objects.filter(id=user.id).first(),
#         owner=r_user,
#         )
#     #Account.objects.filter(id=user.id).first()
#     new_book_google_id = new_book.google_id
#     print("\naddbook new_book =", new_book)
#     try:
#         check_new_book = Book.objects.filter(google_id=new_book_google_id)
#         if check_new_book:
#             messages.warning(request, "1. This book is already in the database, if you want to save it again you need to change the value of google-id.")
#             return redirect('booksmart:allrecords')
#             # return redirect('booksmart:allrecords')
#         else:
#             new_book.save()
#             try:
#                 new_book_add = Book.objects.filter(google_id=new_book_google_id).last()
#                 # new_book_add = Book.objects.filter().last()
#                 new_book_add_author = new_book_add.author
#                 author_c_new_book = Author.objects.filter(author_name=new_book_add_author).last()
#                 if author_c_new_book:
#                     new_book_add.author_c = author_c_new_book
#                     new_book_add.save()
#                     # print('req_book line 578')
#                 else:
#                     print('req_book line 580')
                    
                
#             except Exception as e:
#                 print(f'req_book line 602, error {e}')
                
#     except IntegrityError:
#         if Book.objects.filter(google_id=new_book_google_id):
#             messages.info(request, "2. This book is in database")
#             return redirect('booksmart:allrecords')
#             # return redirect('booksmart:allrecords')
#         else:
#             new_book.save()
#     except ValidationError:
#         if Book.objects.filter(google_id=new_book_google_id):
#             messages.info(request, "3. This book is in database")
#             # return redirect('/booksmart/allrecords/')
#             return redirect('booksmart:allrecords')
#         else:
#             new_book.save()


#     return HttpResponseRedirect(reverse('booksmart:allrecords'))

# H:\BOOKSMART\.venv\Lib\site-packages\rest_auth\registration\serializers.py
# H:\BOOKSMART\.venv\Lib\site-packages\rest_auth\registration\views.py
# H:\BOOKSMART\.venv\Lib\site-packages\rest_framework\authtoken\serializers.py
# H:\BOOKSMART\.venv\Lib\site-packages\rest_framework\authtoken\models.py
# H:\BOOKSMART\.venv\lib\site-packages\rest_auth\views.py
# H:\BOOKSMART\.venv\lib\site-packages\django\contrib\auth\views.py
# H:\BOOKSMART\.venv\Lib\site-packages\django\contrib\auth\tokens.py
# H:\BOOKSMART\.venv\lib\site-packages\django\contrib\auth\__init__.py
# H:\BOOKSMART\.venv\lib\site-packages\django\contrib\auth\models.py
# H:\BOOKSMART\.venv\lib\site-packages\django\contrib\auth\base_user.py
# H:\BOOKSMART\.venv\lib\site-packages\django\contrib\auth\forms.py
# H:\BOOKSMART\.venv\lib\site-packages\django\contrib\auth\__init__.py
# H:\BOOKSMART\.venv\Lib\site-packages\django\contrib\auth\tokens.py
# H:\BOOKSMART\.venv\Lib\site-packages\django\contrib\auth\forms.py
# H:\BOOKSMART\.venv\Lib\site-packages\django\contrib\auth\urls.py
# H:\BOOKSMART\.venv\Lib\site-packages\django\contrib\auth\views.py

 




