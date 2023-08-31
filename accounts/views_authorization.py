from accounts.models import Account, MyAccountManager
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
# from .views_v import *
from django.core.exceptions import ValidationError
import os, requests, json, re, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import resolve
from django.contrib.auth.models import User
from booksmart.models import context_bm

def a_registration_view(request):
    # context = {}
    context_a_r = context_bm
    if "registration_f" in request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect("/")
        else:
            context_a_r['registration_form'] = form

    else:
        form = RegistrationForm()
        context_a_r['registration_form'] = form

    content_a_r = context_a_r['registration_form']
    print("context['registration_form']", context_a_r['registration_form'])
    # return context
    print('content_r', content_a_r)
    return content_a_r

content_re = a_registration_view

def a_logout_view(request, url="/"):
    logout(request)
    return redirect(url)

content_out = a_logout_view

def a_login_view(request):

    context_a_l = context_bm
    r_user = request.user
    if r_user.is_authenticated:
        return redirect("/")

    if "login_f" in request.POST:
        form = AccountAuthenticationForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            r_user = authenticate(username=username, password=password)
            
            if r_user:
                login(request, r_user)
                return redirect("/")

    else:
        form = AccountAuthenticationForm()

    context_a_l['login_form'] = form
    content_a_l = context_a_l['login_form']
    print('content_l', content_a_l)
    return content_a_l

content_in = a_login_view


def a_account_view(request):
    r_user = request.user
    context_a_a = context_bm
    # initial_email = request.user.email
    # initial_user = request.user.username
    if not r_user.is_authenticated:
        return redirect("/")

    if "account_f" in request.POST:
        form = AccountUpdateForm(request.POST, instance=r_user)
        if form.is_valid():
            form.initial = {
	            "email": request.POST['email'],
	            "username": request.POST['username'],
		}
			
            form.save()
            messages.success(request, "ACCOUNT UPDATE SUCCESSFULLY")
            context_a_a['success_message'] = "ACCOUNT UPDATE SUCCESSFULLY"
        
    else:
        form = AccountUpdateForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username,
            }
        )
        # form = ContactForm(initial={'user':request.user,'otherstuff':'otherstuff'})
        # messages.info(request, "Invalid choice")
    
    context_a_a['account_form'] = form
    #print(type(context['account_form']), context['account_form'])
    content_a_a = context_a_a['account_form']
    print('\ncontext', context_a_a)
    print('\ncontent_a', content_a_a)
    return content_a

content_ac = a_account_view

def must_authenticate_view(request):
	return render(request, 'registration/must_authenticate.html', {})

def delete_account(request):
    r_user = request.user
    context_d = context_bm
    if request.method == 'POST':
        delete_form = AccountrDeleteForm(request.POST, instance=r_user)
        # r_user = request.user
        r_user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('/')
    else:
        delete_form = AccountDeleteForm(instance=r_user)

    context_d = {
        'delete_form': delete_form
    }

    return render(request, 'delete_account.html', context_d)

# def request_user_id(request):
#     request.user = user
#     user_id = user.id
#     print(f'views_acc line 137 user_id: {user_id}')
#     return user_id
context_a = context_bm

context_a['registration_form'] = a_registration_view
context_a['login_form'] = a_login_view
context_a['account_form'] = a_account_view
# context_a['user_id'] = request_user_id

class AuthenticationFunctions():
    context_A = context_bm
    def a_registration_view(self, request):
        context_A_r = context_bm
        if "registration_f" in request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                login(request, account)
                return redirect("/")
            else:
                context_A_r['registration_form'] = form

        else:
            form = RegistrationForm()
            context_A_r['registration_form'] = form

        content_A_r = context_A_r['registration_form']
        #print("context['registration_form']", context['registration_form'])
        # return context
        # print('content_r', content_r)
        context_A['registration_form'] =  content_A_r
        return content_A_r

    content_re = a_registration_view

    def a_logout_view(request, url="/"):
        logout(request)
        return redirect(url)

    content_out = a_logout_view

    def a_login_view(self, request):

        context_a_l_v = context_bm
        r_user = request.user
        if r_user.is_authenticated:
            return redirect("/")

        if "login_f" in request.POST:
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

        context_a_l_v['form'] = form
        content_a_l_v = context_a_l_v['form']
        context_a_l_v['login_form'] = content_a_l_v
        return context_a_l_v


    def a_account_view(self, request):
        # user = request.user
        # initial_email = request.user.email
        # initial_user = request.user.username
        context_a_a_v = context_bm
        r_user = request.user
        if not request.user.is_authenticated:
            return redirect("/")

        # context = {}

        if "account_f" in request.POST:
            form = AccountUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
            }
                
                form.save()
                messages.success(request, "ACCOUNT UPDATE SUCCESSFULLY")
                # context['success_message'] = "update successfully"
        else:
            form = AccountUpdateForm(
                initial = {
                    "email": request.user.email,
                    "username": request.user.username,
                }
            )
            # form = ContactForm(initial={'user':request.user,'otherstuff':'otherstuff'})
            # messages.info(request, "Invalid choice")
        
        context_a_a_v['form'] = form
        #print(type(context['account_form']), context['account_form'])
        content_a_a_v = context_a_a_v['form']
        context_a_a_v['account_form'] = content_a_a_v
        return context_a_a_v

    content_ac = a_account_view

    def must_authenticate_view(self, request):
        return render(request, 'registration/must_authenticate.html', {})

    def delete_account(self, request):
        context_d_a = context_bm
        r_user = request.user
        if request.method == 'POST':
            delete_form = AccountrDeleteForm(request.POST, instance=request.user)
            # r_user = request.user
            r_user.delete()
            messages.info(request, 'Your account has been deleted.')
            return redirect('/')
        else:
            delete_form = AccountDeleteForm(instance=request.user)

        # context = {
            # 'delete_form': delete_form
        # }
        # context['form'] = delete_form
        # print(type(context['account_form']), context['account_form'])

        context_d_a['delete_form'] =  delete_form
        content_d_a = context_d_a['form']
        context_d_a['delete_form'] = content_d_a
        return context_d_a
        #return render(request, 'delete_account.html', context)