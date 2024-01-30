from accounts.models import Account

from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm #, UrlPathForm
from booksmart.forms import PdfReader, BackgroundFormPoster, BackgroundFormVideo, BackgroundFormMusic
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from accounts.views import *
import os, requests, json, re, datetime, requests.api
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import resolve, reverse, translate_url
from django.contrib.sites.shortcuts import get_current_site
from django.urls import *
from booksmart.models import Book, Author, BackgroundPoster, BackgroundVideo, BackgroundMusic, url_img, url_img_author#, context_bm_models
import datetime

def context_bm_models():    
    print("views_infoview context_bm_models()")
    context_bm = {}
    context_list = []

    context_bm['no_date'] = datetime.date(3000, 1, 1)
    context_bm['url_img_book'] = url_img
    context_bm['url_img_author'] = url_img_author

    try:
        if Book.objects.all().count() > 0:
        # if Book.objects.filter().all():
            # all_books = Book.objects.all()
            # context_list.append(all_books)
            num_books = Book.objects.all().count()
            # context_bm['allbooks'] = all_books
            context_bm['num_books'] = num_books
        elif Book.objects.all().count() == 0:
        # elif not Book.objects.filter().all():
            # context_bm['allbooks'] = None
            context_bm['num_books'] = 0
    except Exception as err:
        print(f"booksmart models 335 no Book.objects.all(): except Exception as {err}")
        context_bm['allbooks'] = None
        context_bm['num_books'] = 0  

    try:
        if Author.objects.all().count() > 0:
        # if Author.objects.filter().all():
            # all_authors = Author.objects.all()
            # context_list.append(all_authors)
            num_authors = Author.objects.all().count()
            # context_bm['allauthors'] = all_authors
            context_bm['num_authors'] = num_authors
        elif Author.objects.all() == 0:
        #elif not Author.objects.filter().all():
            # context_bm['allauthors'] = None
            context_bm['num_authors'] = 0
    except Exception as err:
        print(f"booksmart models 351 no Author.objects.all(): Exception as {err}")
        context_bm['allauthors'] = None
        context_bm['num_authors'] = 0

    try:
        if BackgroundPoster.objects.filter().last():
            poster = BackgroundPoster.objects.filter().last()
            context_bm['poster_url_1'] = poster.link_poster_1
            context_bm['poster_url_2'] = poster.link_poster_2
        elif not BackgroundPoster.objects.filter().last():
            context_bm['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
            context_bm['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
    except Exception as err:
        print(f"booksmart models 367 no BackgroundPoster.objects.filter().last(): Exception as {err}")
        context_bm['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
        context_bm['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"

    try:
        if BackgroundVideo.objects.filter().last():   
            video = BackgroundVideo.objects.filter().last()
            context_bm['video_url'] = video.link_video
            context_bm['video_type'] = video.type_video
        elif not BackgroundVideo.objects.filter().last():
            context_bm['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
            context_bm['video_type'] = "mp4"
    except Exception as err:
        print(f"booksmart models no BackgroundVideo.objects.filter().last(): Exception as {err}")
        context_bm['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
        context_bm['video_type'] = "mp4"

    try:
        if BackgroundMusic.objects.filter().last():   
            music = BackgroundMusic.objects.filter().last()
            context_bm['music_url_1'] = music.link_music_1
            context_bm['music_type_1'] = music.type_music_1
            context_bm['music_url_2'] = music.link_music_2
            context_bm['music_type_2'] = music.type_music_2
        elif not BackgroundMusic.objects.filter().last(): 
            context_bm['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
            context_bm['music_type_1'] = "mp3"
            context_bm['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
            context_bm['music_type_2'] = "mp3"
    except Exception as err:
        print(f"booksmart models 400 BackgroundMusic.objects.filter().last(): except Exception as {err}")    
        context_bm['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_bm['music_type_1'] = "mp3"
        context_bm['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_bm['music_type_2'] = "mp3"
    
    context_bm_models.context_bm = context_bm
    # context_bm = context_bm_models.copy()
    return context_bm
# from internetarchive import configure, download

# download(identifier: str, files: files.File | list[files.File] | None = None, formats: str | list[str] | None = None, glob_pattern: str | None = None, dry_run: bool = False, verbose: bool = False, ignore_existing: bool = False, checksum: bool = False, destdir: str | None = None, no_directory: bool = False, retries: int | None = None, item_index: int | None = None, ignore_errors: bool = False, on_the_fly: bool = False, return_responses: bool = False, no_change_timestamp: bool = False, **get_item_kwargs) → list[requests.Request | requests.Response][source]

# from internetarchive import get_item, get_username
# from internetarchive import item
# from bookmain.settings import config_ar
# # http://127.0.0.1:8000/

# import internetarchive
# from internetarchive import ArchiveSession

# try:
# 	configure('kreative358@hotmail.com', 'Bonum12o')
# 	arsesion = ArchiveSession()
# 	print('arsesion', arsesion)

# 	username = get_username('ZA2XJs2aXBt6OQLq', 'M1PEtZXOrXZhVsAG')
# 	print('infoview username', username)
# except Exception as e:
# 	print(f"Exception infoview line 35 error: {e}")
# 	pass

# def background(request):
# 	context = {}
# 	background_form = BackgroundForm()
#     if request.GET:
# 		background_form = BackgroundForm(request.GET)
# 		if background_form.is_valid():
# 			poster_url = background_form.cleaned_data['link_poster_1']
# 			context['poster'] = poster_url
# 			video_url = pbackground_form.cleaned_data['link_video']
# 			context['video'] = video_url
# 			return render(request, "background_view.html", context)
			# return render(request, "allrecord.html", context)
    # if request.POST:
	# 	background_form = BackgroundForm(request.POST, or None, request.FILES or None)
	# 	if background_form.is_valid():
	# 		poster_url = background_form.cleaned_data['link_poster_1']
	# 		video_url = pbackground_form.cleaned_data['link_video']
	# return render(request, "background_view.html", context)

from booksmart.forms import PageForm
@api_view(['POST', 'GET'])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([permissions.IsAuthenticated, ])
def read_page(request):
	context_bm_models()
	context = context_bm_models.context_bm
	r_user = request.user

	if not r_user.is_authenticated:
		return redirect('index')

	if request.GET:
		page_form = PageForm()
		
	if request.POST:
		page_form = PageForm(request.POST or None, request.FILES or None)
		if page_form.is_valid():
			needed_page = page_form.cleaned_data['page_number']
			book_id = page_form.cleaned_data['book_google_id']
			book_page_link = f"https://books.google.com/books?id={book_id}&amp;pg=PA{needed_page}&amp;hl=tw&amp;source=gbs_toc_r&amp;output=embed#%257B%257D" 
			print("book_page_link", book_page_link)
			context['page_form']=book_page_link
			return render(request, 'read_page.html', context)

	return render(request, 'read_page.html', context)

# from rest_framework import permissions
# permissions.IsAdminUser
@api_view(['GET', 'POST'])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([permissions.IsAdminUser, ])
def background_poster(request):
	context_bm_models()    
	context = context_bm_models.context_bm
	if request.GET:
		poster_form = BackgroundFormPoster()
		
	if request.POST:
		poster_form = BackgroundFormPoster(request.POST or None, request.FILES or None)
		if poster_form.is_valid():
			poster = poster_form.save()
			return redirect('booksmart:allrecords')

	context['poster'] = poster_form
	context['new'] = True
	return render(request, 'new_poster.html', context)


def background_video(request):
	context_bm_models()       
	context = context_bm_models.context_bm
	video_form = BackgroundFormVideo()

	if request.POST:
		video_form = BackgroundFormVideo(request.POST or None, request.FILES or None)
		if video_form.is_valid():
			video_url = video_form.save()
			return redirect('booksmart:allrecords')

	context['video'] = video_form
	context['new'] = True

	return render(request, 'new_video.html', context)

# def background_music(request):
#     context = context_bm
#     video_form = BackgroundFormMusic()

#     if request.POST:
#         video_form = BackgroundFormMusic(request.POST or None, request.FILES or None)
#         if video_form.is_valid():
#             video_url = video_form.save()
#             return redirect('booksmart:allrecords')

#     context['video'] = video_form
#     context['new'] = True

#     return render(request, 'new_video.html', context)

		


def pdf_reader(request):
	context_bm_models()      
	context = context_bm_models.context_bm

	# books = Book.objects.all()
	# authors = Author.objects.all()
	pdf_form = PdfReader()
	# context['books'] = books
	# context['authors'] = authors
	context['pdf_form'] = pdf_form
	book_link_h='https://drive.google.com/file/d/1MG3P-Tdr5iR9zJTE4SeWpBLqO380hbEm/preview?usp=sharing'
	context['book_link_h'] = book_link_h
	if request.POST:
		pdf_form = PdfReader(request.POST)
		if pdf_form.is_valid():
			book_to_read_gd = pdf_form.cleaned_data['link_book_gd']
		
			print('book_to_read_gd:', book_to_read_gd)
			book_to_read_gb = pdf_form.cleaned_data['link_book_gb']
			print('book_to_read_gb:', book_to_read_gb)
			book_to_read_dc = pdf_form.cleaned_data['link_book_dc']
			print('book_to_read_dc:', book_to_read_dc)
			book_to_read_sejda = pdf_form.cleaned_data['link_book_sejda']
			print('book_to_read:', book_to_read_sejda)
			if book_to_read_gd != "":
				try:

					if re.findall("/d/.+?[/]", book_to_read_gd):
						# if re.findall("/d/.+?[/]", book_to_read)[0][3:6]=='151':
						x = book_to_read_gd.rfind("/")
						print('x', x)
						book_link_gd = book_to_read_gd[:x+1] + "preview"
						print('book_link_gd', book_link_gd)
						context['book_link'] = book_link_gd

						return render(request, "pdf_reader.html", context)

					elif not re.findall("/d/.+?[/]", book_to_read_gd):
						context['message'] = f'This is not standard google drive pdf link'
						# context['book_link_gd'] = book_link
						context['book_link_gd'] = context['book_link']
						# context['book_link_gd'] = book_to_read_gd
						return render(request, "pdf_reader.html", context)
					
					else:
						context['message'] = f'Incorrect link not pdf'
						return render(request, "pdf_reader.html", context)

				except Exception as e:
					context['message'] = f'Incorrect link, error description: {e}'
					return render(request, "pdf_reader.html", context )

			if book_to_read_gb != "":
				try:
					# print('book_link_gb', book_link_gb)
					# context['book_link_gb'] = book_link_gb
					# print('book_link_gb', book_link_gb)		
					print('book_link_gb', book_to_read_gb)
					context['book_link_gb'] = book_to_read_gb
					print('book_link_gb', book_to_read_gb)		     			
					return render(request, "pdf_reader.html", context)
				except Exception as e:
					context['message'] = f'Incorrect link, error description: {e}'
					return render(request, "pdf_reader.html", context )

			if book_to_read_dc != "":
				try:
					
					# context['book_link_dc'] = f"https://docs.google.com/viewer?url={book_link_dc}&embedded=true"
					context['book_link_dc'] = f"https://docs.google.com/viewer?url={context['book_link']}&embedded=true"
					print(context['book_link_dc'])
					return render(request, "pdf_reader.html", context)
				except Exception as e:
					context['message'] = f'Incorrect link, error description: {e}'
					return render(request, "pdf_reader.html", context )

			if book_to_read_sejda != "":
				try:
					
					# context['book_link_sejda'] = f'https://www.sejda.com/sign-pdf?files=%5B%7B%22downloadUrl%22%3A%22{book_link_sejda}&%22%7D%5D'
					context['book_link_sejda'] = f'https://www.sejda.com/sign-pdf?files=%5B%7B%22downloadUrl%22%3A%22{book_to_read_sejda}&%22%7D%5D'     
					# book_to_read_sejda
					# context['book_link_sejda'] = f'https://www.sejda.com/sign-pdf?files=[\{"downloadUrl":"{book_link_dc}\"\}]'
					print(context['book_link_sejda'])
					return render(request, "pdf_reader.html", context)
				except Exception as e:
					context['message'] = f'Incorrect link, error description: {e}'
					return render(request, "pdf_reader.html", context )

	return render(request, "pdf_reader.html", context )

def app_users(request):
	# home_screen_view,
	# urlObject = request.get_host() + request.path
	# print("app_users urlObject", urlObject)
	# urlObject1 = request._current_scheme_host + request.path
	# print("app_users urlObject1", urlObject1)
	# print("app_users urlObject2", "request.path:", request.path, "request.get_full_path",request.get_full_path, "request.build_absolute_uri", request.build_absolute_uri)
	# print("app_users request.get_host()", request.get_host())
	# print("app_users request.resolver_match.url_name", request.resolver_match.url_name)
	# print("app_users get_current_site:", get_current_site )
	# print("resolve, reverse, translate_url:", resolve, reverse, translate_url )
	context_bm_models() 
	context = context_bm_models.context_bm  
	accounts = Account.objects.all()
	books = Book.objects.all()
	authors = Author.objects.all()
	identity = 'hobbitortherebac0000tolk_t0g2'
	# item_ar = get_item(identity)
	# print('infoview: item.exists', item_ar.exists)
	# print('item.item_metadata', item_ar.item_metadata)
	# item_file = item_ar.get_file('lccn_078073006991')
	# configure_ar = config_ar
	# try:
	# 	download_ar = download('lccn_078073006991_0050', formats='EPUB', on_the_fly=True) ## return_responses
	# # epub_ar = download('harrypotterdeath0000rowl_n2u6', verbose=True, formats='EPUB', on_the_fly=True)
	# except Exception as e:
	# 	print(f'error with download is: {e}')

	login_name = {"username": "kreative358@hotmail.com"}
	login_pass = {"password": "Bonum12o"}
	login_form = {"username": "kreative358@hotmail.com", "password": "Bonum12o"}
	app_users_login = 'snippets/app_users_login.html'
	# print('download_ar', download_ar)
	context['info'] = 'info'
	context['accounts'] = accounts
	context['allbooks'] = books
	#context['download_ar'] = download_ar
	context['login_form'] = login_form
	context['login_name'] = "kreative358@hotmail.com"
	context['login_pass'] = "Bonum12o"
	context['app_users_login'] = app_users_login
	i = 50
	# page = f'https://ia902307.us.archive.org/BookReader/BookReaderImages.php?zip=/18/items/{identity}/{identity}_jp2.zip&file={identity}_jp2/{identity}_00{i}.jp2&id={identity}crossorigin="anonymous|use-credentials%22"'
	# print('page', page)
	# context['page'] = page

	return render(request, "app_users.html", context )

# app_users urlObject 127.0.0.1:8001/booksmart-app/booksmart-app/app_users/
# app_users urlObject1 http://127.0.0.1:8001/booksmart-app/booksmart-app/app_users/
# app_users urlObject2 request.path: /booksmart-app/booksmart-app/app_users/ request.get_full_path <bound method HttpRequest.get_full_path of <WSGIRequest: GET '/booksmart-app/booksmart-app/app_users/'>> request.build_absolute_uri <bound method HttpRequest.build_absolute_uri of <WSGIRequest: GET '/booksmart-app/booksmart-app/app_users/'>>
# app_users request.get_host() 127.0.0.1:8001
# app_users request.resolver_match.url_name app_users

def must_authenticate_view(request):
	return render(request, 'registration/must_authenticate.html', {})


# def search_open(request, parameters):
# 	context = context_bm_models.context_bm
# 	context['message_no_ol'] = ""
# 	parameters = f'{title_plus}+{book.surname}'
# 	search_url = f'https://openlibrary.org/search/inside.json?q={title_plus}'
# 	r = requests.get(url=search_url)
# 	if r.status_code != 200:
# 		context['message_no_ol'] = f'Sorry, probably something went wrong, r.status_code = {r.status_code}'
# 		return Response(context, template_name='read_book.html', )

# 	data = r.json()
# 	# data = r
# 	# records = json.loads(data)
# 	records = data
# 	links = []

# 	# url = 'https://openlibrary.org/account/login'
# 	# context['searching'] = url

# 	# url = 'https://archive.org/account/login'
# 	# url = 'https://openlibrary.org/account/login'
# 	# searching = f'{url}'
	
# 	# idents = []
# 	# idents_title = []
# 	# idents_author = []
# 	# titles_jsplit = []
# 	# titles_jshort = []
# 	# authors_jname = []
# 	# authors_jsurname = []
	
# 	if records['hits']['hits']:
# 		recs = records['hits']['hits']
# 		print('len(recs)', len(recs))
# 		n_records = len(recs)
# 		print('titles_short[0]', titles_short[0])
# 		for i in range(n_records-1):
# 			try:
# 				if recs[i]['edition']['ocaid']:
# 					ident = recs[i]['edition']['ocaid']
# 					idents.append(ident)
# 			except Exception as e:
# 				print(f"151 {e}, i: {i}")
# 			try:
# 				if recs[i]['edition']['title']:
# 					title_jshort = recs[i]['edition']['title'].lower()
# 					print('title_jshort', title_jshort)
# 					# print('titles_short[0]', titles_short[0])
# 					titles_jshort.append(title_jshort)
# 					title_jsplit = recs[i]['edition']['title'].lower().split()
# 					titles_jsplit.append(title_jsplit)

# 					if title_jshort==titles_short[0] or set(title_jsplit).issubset(set(titles_split[0])) or set(titles_split[0]).issubset(set(title_jsplit)):
# 						idents_title.append(idents[-1])

# 					else:
# 						pass
# 			except Exception as e:
# 				print(f"168 {e}, i: {i}")
# 			try:
# 				if recs[i]['edition']['authors'][0]['name']:
# 					author_jname = recs[i]['edition']['authors'][0]['name']
# 					authors_jname.append(author_jname)
# 					author_jsurname = str(author_jname.split()[-1])
# 					authors_jsurname.append(author_jsurname)
# 					if author_jname == author_to_search or author_jsurname == author_surname:
# 						idents_author.append(idents[-1])
# 					else:
# 						print('1. no author')
# 						pass
# 				else:
# 					print('2. no author')
# 					pass
# 			except Exception as e:
# 				print(f"180 {e}, i: {i}")

# 		# print('idents', idents)
# 		# print('idents_title', idents_title)
# 		# print('idents_author', idents_author)
		

# 		if idents and idents_title and idents_author:
# 			identities_list_1 = list(set(idents).intersection(set(idents_title).intersection(set(idents_author))))
# 			# identities.extend(identities_list_1)
# 			if len(identities_list_1) > 0:
# 				identities.extend(identities_list_1)
# 				print('identities_list_1', identities_list_1)
# 			else:
# 				print('1. no links')


# 		elif idents and idents_title and not idents_author:
# 			identities_list_2 = list(set(idents).intersection(set(idents_title)))
# 			# identities.extend(identities_list_2)
# 			if len(identities_list_2) > 0:
# 				identities.extend(identities_list_2)
# 				print('identities_list_2', identities_list_2)
# 			else:
# 				print('2. no links')

# 		elif idents and idents_author and not idents_title:
# 			identities_list_3 = list(set(idents).intersection(set(idents_title)))
# 			# identities.extend(identities_list_3)
# 			if len(identities_list_3) > 0:
# 				identities.extend(identities_list_3)
# 				print('identities_list_3', identities_list_3)
# 			else:
# 				print('3. no links')

# 		elif not idents:
# 			print('4 no links')
# 			context['message_no_ol'] = 'Sorry, probably no free ebook on this title'
# 			return Response(context, template_name='read_book.html', )

