from accounts.models import Account, MyAccountManager
import os, requests, json, re, datetime, requests.api
from booksmart.models import context_bm, url_img, Book, Author
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


def account_view_form(request):
    context = context_bm
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
    context = context_bm
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
    context = context_bm
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
    context = context_bm
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
