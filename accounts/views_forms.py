from accounts.models import Account, MyAccountManager
import os, requests, json, re, datetime, requests.api
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib import messages
from rest_framework.authtoken.models import Token
from booksmart.models import Book, Author, BackgroundPoster, BackgroundVideo, BackgroundMusic, url_img, url_img_author #, context_bm_models
import datetime

def context_bm_models():    
    print("views_forms context_bm_models()")
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


def account_view_form(request):
    context_bm_models()
    context = context_bm_models.context_bm
    r_user = request.user
    if not request.user.is_authenticated:
        return redirect("index")

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['message'] = "account update successfully"
            # context['account_form'] = form
            # return render(request, 'account_update.html', context)
            messages.success(request, 'account update successfully')
            # return redirect('/booksmart/accounts/account')
            return redirect(f"{request.path}")
        else:
            # for msg in form.errors:
            #     messages.error(request, f"{msg}: {form.errors[msg]}")
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            messages.error(request, f'{error_string}')
            errors = form.errors
            print(f'errors: {errors}')
            # return redirect('/booksmart/account/account')
            return redirect(f"{request.path}")
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
        context['account_form'] = form
        # return render(request, 'account_update.html', context)
    context['account_form'] = form
    print('context[message]:', context['message'])
    # return render(request, 'account_update.html', context)
    # return redirect('/booksmart/account/account')
    return redirect(f"{request.path}")


def register_view_form(request):
    context_bm_models()    
    context = context_bm_models.context_bm
    r_user = request.user
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            
            account = authenticate(email=email, password=raw_password)
            if account:
                login(request, account)
                try:
                    token = Token.objects.get(user=account)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=account)

                if token:
                    print('token.key', token.key)
                else:
                    print('no token')
                messages.success(request, 'Account created successfully')
                # return redirect('index')
                return redirect(f"{request.path}")
            else:
                error_string = ' '.join(['<br>'.join(x for x in l) for l in list(form.errors.values())])
                messages.error(request, f'{error_string}')
                # return redirect('/booksmart/account/register')
                return redirect(f"{request.path}")

        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            messages.error(request, f'{error_string}')
            return redirect('index')
    else:
        form = RegistrationForm()
        context['registration_form'] = form
        # return HttpResponse(content_a) 
        # return redirect("/", content_a) 

    return redirect('index')

def A_account_view_form(request):
    # user = request.user
    # initial_email = request.user.email
    context_bm_models()    
    context = context_bm_models.context_bm
    r_user = request.user
    # initial_user = request.user.username
    if not request.user.is_authenticated:
        return redirect("/")

    if "account_f" in request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
	            "email": request.POST['email'],
	            "username": request.POST['username'],
		}
			
            form.save()
            messages.success(request, "ACCOUNT UPDATE SUCCESSFULLY")
            context['message'] = "ACCOUNT UPDATE SUCCESSFULLY"
            context['account_form'] = form
            context_account = context
            print('form.is_valid():', context_account)
            return context_account

        elif not form.is_valid():
            form = AccountUpdateForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username,
            }
        )
            context['message'] = "ACCOUNT UPDATE SUCCESSFULLY, MAIL or USERNAME IS ALREADY IN USE"
            context['account_form'] = form
            context_account = context
            print('not form.is_valid():', context_account)
            return context_account
        
    else:
        form = AccountUpdateForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username,
            }
        )
        # form = ContactForm(initial={'user':request.user,'otherstuff':'otherstuff'})
        # messages.info(request, "Invalid choice")
    
    context['account_form'] = form
    #print(type(context['account_form']), context['account_form'])
    context_account = context['account_form']
    print('\ncontext', context)
    print('\ncontext_account', context_account)
    return redirect('index')

@api_view(['GET', 'POST'])
@permission_classes([AllowAny,])  #IsAuthenticated
# @authentication_classes([]) # authentication.TokenAuthentication
@renderer_classes([TemplateHTMLRenderer])
def registration_view(request):
    context_bm_models()    
    context = context_bm_models.context_bm
    r_user = request.user
    if request.GET:
        form = RegistrationForm()
        return Response(context, template_name='register_view.html', )
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('index')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return Response(context, template_name='register_view.html', )
    # return HttpResponse(content_a) 
    # return redirect("/", content_a) 
    # return render(request, 'register.html', context)
