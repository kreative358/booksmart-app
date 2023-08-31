from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from string import Template
from os import environ
from booksearch.forms import BookSearch
import os, re, json, time, requests, datetime
from booksmart.models import Book, Author, url_img
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
#  from booksearch.req_book import *
from django.utils.html import format_html
from django.urls import reverse


def req_book(book, founded_books_number):
    # false = "False"
    # true = "True"
    book_dict = {}
    book_dict_out = {}

    try:
        book_dict['val_total'] = founded_books_number
        # print("req_book book_dict['val_total']", book_dict['val_total'])
        book_dict['google_id'] = book['id']
    except:
        book_dict['google_id'] = "unknown"

    try:
        book_dict['title'] = book['volumeInfo']['title'].upper().replace('„', '').replace('”', '')
        book_dict['preview_link_new'] = f"https://www.google.com/books/edition/_/{book['id']}" 
    except:
        book_dict['title'] = "unknown"

    try:
        author = " ".join(re.sub(r"\([^()]*\)", "", book['volumeInfo']['authors'][0].title()).split())
        book_dict['author'] = f'{author}'
        book_dict['surname'] = f'{author.split()[-1]}'
        # book_dict['author_link'] =  f"https://{book['volumeInfo']['language']}.wikipedia.org/wiki/{author.replace(' ', '_')}"
        book_dict['author_link'] =  f"https://{book['volumeInfo']['language']}.wikipedia.org/wiki/{author.replace(' ', '_')}"
    except:
        book_dict['author'] = "unknown"

    try:
        book_dict['category'] = ", ".join(book['volumeInfo']['categories'])
    except:
        book_dict['category'] = 'no category'

    try:
        book_dict['summary'] = book['volumeInfo']['description'][:990]
    except:
        book_dict['summary'] = 'no summary'

    try:
        book_dict['preview_link'] = book['volumeInfo']['previewLink']
    except:
        book_dict['preview_link'] = 'no preview link to this book'

    try:
        if book['volumeInfo']['publishedDate']:
            book_pub_len = len(book['volumeInfo']['publishedDate'])
    
            if book_pub_len == 4:
                book_dict['published'] = book['volumeInfo']['publishedDate'] + '-07-01'
            elif book_pub_len == 7:
                book_dict['published'] = book['volumeInfo']['publishedDate'] + '-01'
            else:
                book_dict['published'] = book['volumeInfo']['publishedDate']
                book_date = book['volumeInfo']['publishedDate']
                # print('type(book_date)', type(book_date))
        else:
            book_dict['published'] = '000-01-01'
    except:
        book_dict['published'] = '3000-01-01'
        # book_dict['published'] = None

    try:
        book_dict['language'] = book['volumeInfo']['language']
    except:
        book_dict['language'] = 'no info'

    try:
        book_dict['imageLinks'] =  book['volumeInfo']['imageLinks']['thumbnail']
    except:
        book_dict['imageLinks'] = url_img

    try:
        book_dict['selfLink'] = book["selfLink"]
    except:
        book_dict['selfLink'] = "no json link"

    try:
        if book['volumeInfo']['industryIdentifiers']:
            Identifiers = book['volumeInfo']['industryIdentifiers']
            book_dict['identyfiers'] =  "".join([f'<br>{id["type"]}:{id["identifier"]}' for id in Identifiers])
            # book_dict['isbn'] = book_dict['identyfiers'].split(',')[0].split()[-1]
            book_dict['identyfiers_dict'] = {}
            book_dict['identyfiers_dict'] = {id["type"]: id["identifier"] for id in Identifiers}
            if 'ISBN_13' in book_dict['identyfiers_dict'].keys():
                book_dict['isbn'] =  book_dict['identyfiers_dict']['ISBN_13']
            else:
                book_dict['isbn'] = book_dict['identyfiers'].replace('<br>', '').replace('OTHER:', '').split(',')[0].split()[0]
                # book_dict['isbn'] = book_dict['identyfiers'].split(',')[0].split()[0]
                print("book_dict['isbn']", book_dict['isbn'])
                # book_dict['no_isbn'] = book_dict['identyfiers_dict']['no isbn']
                # print("book_dict['no_isbn']", book_dict['no_isbn'])
    except:
        book_dict['isbn'] = 'no industry identyfiers'

    try:
        if book['accessInfo']['embeddable'] != None:
            embeddable = str(book['accessInfo']['embeddable'])
            # embeddable = f"{book['accessInfo']['embeddable']}"
            #print('embeddable:', embeddable, type(embeddable))
            if embeddable == "True":
                book_dict['embeddable'] = "YES"
            elif embeddable == "False":
                book_dict['embeddable'] = "NO"
    except:
        book_dict['embeddable'] = 'no'

    try:
        if book['accessInfo']['epub']['isAvailable'] != None:
            # embeddable = str(book['accessInfo']['embeddable'])
            epub = f"{book['accessInfo']['epub']['isAvailable']}"
            # print('epub:', epub, type(epub))
            if epub == "True":
                book_dict['epub'] = "YES"
            elif epub == "False":
                book_dict['epub'] = "NO"
    except:
        book_dict['epub'] = 'no EPUB'

    try:
        if  Book.objects.filter(google_id=book['id']):
            book_dict['avaliable'] = "avaliable"
        else:
            book_dict['avaliable'] = 'NOT avaliable'
    except:
        book_dict['avaliable'] = 'exNOT avaliable' 
                            
    founded_books_number = book_dict['val_total']
    if founded_books_number > 50 and "unknown" in book_dict.values(): # and book_dict['epub'] == "false":
        book_dict_out = book_dict
        print("book_dict_out", book_dict_out)
        book_dict = {}
        return book_dict_out
    else:
        return book_dict


def req_author_id(author, language, book_dict):

    try:
        book_dict['author_c'] = {}
        url1 = "https://www.wikidata.org/w/api.php" 
        book_dict['author_c']['author_name'] = author
        author=author.replace(" ","_")
        lang = language
        params = {   
        "action" : "wbsearchentities",
        "language" : lang,
        "format" : "json",
        "search" : author,
        }

        r = requests.get(url1,params=params)
        datas = r.json()

        if datas:

            try:
                wiki_idx = datas["search"][0]["id"]
                print('185 req_author_id wiki_idx', wiki_idx)  
                if wiki_idx:
                    book_dict['author_c']['wiki_idx'] = wiki_idx
                    
                    if Author.objects.filter(wiki_idx=wiki_idx):
                        book_dict['author_c']['avaliable'] = "avaliable"
                        # return book_dict['author_c']                
                    elif not Author.objects.filter(wiki_idx=wiki_idx):
                        book_dict['author_c']['avaliable'] = "NOT avaliable"
                elif not wiki_idx:
                    print("elif not wiki_idx: 184 reqs.py")
                    book_dict['author_c']['wiki_idx'] = 'none wiki_idx'
            except:
                print('no wiki_idx for', author)
                book_dict['author_c']['wiki_idx'] = 'no wiki_idx'
                return book_dict

            try:
                label_name = datas["search"][0]["label"]
                if label_name:
                    full_name = label_name.replace("\xa0", "") #
                    book_dict['author_c']['full_name'] = full_name #.replace(' ', '_')
                    name = full_name.split()
                    
                    if len(name) == 1:
                        print('2. name:', name)
                        book_dict['author_c']['first_name'] = f'{name[0]}'
                        # book_dict['author_c']['last_name'] = f'{name[-1]}'
                        # book_dict['author_c']['last_name']

                    elif len(name) == 2:
                        book_dict['author_c']['first_name'] = f'{name[0]}'
                        book_dict['author_c']['last_name'] = f'{name[-1]}'

                    elif len(name) > 2:
                        book_dict['author_c']['first_name']= f'{name[0]}'
                        book_dict['author_c']['middle_name'] = f'{" ".join(name[1:-1])}'
                        book_dict['author_c']['last_name'] = f'{name[-1]}'
            except:
                full_name = book_dict['author']
                book_dict['author_c']['full_name'] = full_name
                name = full_name.split()
                book_dict['author_c']['first_name'] = f'{name[0]}'
                book_dict['author_c']['last_name'] = f'{name[-1]}'

        return book_dict

    except Exception as e:
        print(f'Error line author wiki: {e}')
        book_dict['author_c']['error'] = f'{e}'
        return book_dict
        

def req_author_date(wiki_idx, book_dict):
    try:
        key=os.environ.get('API_KEY')
        wiki_id = wiki_idx
        print("wiki_id", wiki_id)

        url2 = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&format=json".format(wiki_id)
        r_1 = requests.get(url2)
        data_wiki = r_1.json()
        time.sleep(0.2) #
        data_entities = data_wiki['entities'][wiki_id]
        
        try:
            if data_entities["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]:

                date_of_birth = data_entities["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"][1:11]
                book_dict['author_c']['date_of_birth'] = str(date_of_birth)
                    
                print("date_of_birth", type(date_of_birth), date_of_birth)
            else:
                book_dict['author_c']['date_of_birth'] = "0000-01-01"
        except:
            book_dict['author_c']['date_of_birth'] = "3000-01-01"

        try:

            if data_entities["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]:
                date_of_death = data_entities["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"][1:11]
                book_dict['author_c']['date_of_death'] = date_of_death
                    
                print("date_of_birth", type(date_of_death), date_of_death)
            else:
                book_dict['author_c']['date_of_death'] = "2500-01-01"
        except:
            book_dict['author_c']['date_of_death'] = "3000-01-01" # "3000-01-01"
        
        try:
            book_lang = book_dict['language']
            if data_entities['descriptions'][book_lang]['value']:
                wiki_data_auth = data_entities['descriptions'][book_lang]['value']
                print("wiki_data_auth",  wiki_data_auth)
                book_dict['author_c']['author_wiki_link_d'] =  wiki_data_auth
            # elif not data_entities['descriptions']['en']['value']:
            elif not data_entities['descriptions'][book_lang]['value']:
                
                try:
                    if data_entities['descriptions']['en']['value']:
                        book_dict['author_c']['author_wiki_link_d'] = data_entities['descriptions']['en']['value']
                    elif not data_entities['descriptions']['en']['value']:
                        book_dict['author_c']['author_wiki_link_d'] = 'no short info'
                except:
                    book_dict['author_c']['author_wiki_link_d'] = 'no author description in wikidata'    

        except Exception as e:
            print(f'Error line 270: {e}')
    
        return book_dict    

    except Exception as e:
        print(f'reqs Error line 328: {e}')
        return book_dict

      
def req_author_wiki_details(book_author, book_lang, book_dict):
    
    try:  
        S = requests.Session()
        url = f'https://{book_lang}.wikipedia.org/w/api.php'
        params = {
                'action': 'query',
                'format': 'json',
                'titles': book_author,
                'prop': 'extracts',
                'exchars': 1050,
                'explaintext': True,
            }

        print("wikipedia link", url)
        response = S.get(url, params=params)
        data = response.json()
        
        if data:
            print('\nndata', data)
            page = next(iter(data['query']['pages'].values()))
            print('len(page)', len(page))
            text3 = page['extract']
            text2 = re.sub(r'==.*?==+', '', text3)
            text1 = text2.replace('\n', '')
            text = text1[:1000]
            
            if len(text) == 0:
                book_dict['author_c']['author_wiki_link'] = 'no wikidata'
                print('no wikidata')
            elif len(text) > 0:
                print('text', text)
                if (len(text)-text.rfind('.')) > 50:
                    details = text[: text.rfind(',')]
                    book_dict['author_c']['author_wiki_link'] = f'{details}...'
                    print("1. book_dict['author_c']['author_wiki_link']", len(book_dict['author_c']['author_wiki_link']))
                elif (len(text)-text.rfind('.')) < 50:
                    details = text[: text.rfind(',')]
                    book_dict['author_c']['author_wiki_link'] = f'{details}.'
                    print("2. book_dict['author_c']['author_wiki_link']", len(book_dict['author_c']['author_wiki_link']))
                else:
                    details = text
                    book_dict['author_c']['author_wiki_link'] = f'{details}.'
                    print("3. book_dict['author_c']['author_wiki_link']", len(book_dict['author_c']['author_wiki_link']))
            else:
                book_dict['author_c']['author_wiki_link'] = 'no wikidata'

        elif not data:
            book_dict['author_c']['author_wiki_link'] = 'no wikidata'
            print("\n\nbook_dict['author_c']['author_wiki_link']", book_dict['author_c']['author_wiki_link'])

        return book_dict

    except Exception as e:
        print(f'reqs Error line 380: {e}')
        book_dict['author_c']['author_wiki_link'] = 'no wikidata'

        return book_dict
    

# book_lang = book_dict['language']
def req_author_img(book_author, book_lang, book_dict):
    
    try:
        URL = f"https://{book_lang}.wikipedia.org/w/api.php"
        S = requests.Session()
        params1 = {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "prop": "pageimages|pageterms",
            "piprop": "original",
            "titles": book_author,
        }

        r1 = S.get(url=URL, params=params1)
        data1 = r1.json()

        if data1:
            image1 = data1["query"]["pages"][0]["original"]["source"]
            book_dict['author_c']['author_wiki_img'] = image1
            print()
            print("image1", image1)
        elif not data1:
            book_dict['author_c']['author_wiki_img'] = 'no img'
            
        return book_dict

    except Exception as e:                       
        print('454 exception:', e)
        book_dict['author_c']['author_wiki_img'] = 'no img'
        
        return book_dict
    