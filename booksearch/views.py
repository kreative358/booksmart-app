from django.shortcuts import render, get_object_or_404, redirect
from booksearch.forms import BookSearch
from booksmart.models import url_img, Book, Author, context_bm #, BackgroundPoster, BackgroundVideo
import os, requests, json, re, datetime
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.authentication import TokenAuthentication
from accounts.views_authorization import *
from accounts.api.views import AccountViewSet, UserDetailViewSet, UserViewSet
from booksmart.api.views import BooksEditViewSet, AuthorViewSet, BooksFullViewSet




@api_view(['GET', 'POST'])
@permission_classes([])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer])
def gbsearch_book(request):
    r_user = request.user
    context = context_bm
    form = BookSearch()

    # form_a = a_account_view(request)
    # #form_out = a_logout_view(request)
    # form_r = a_registration_view(request)
    # form_l = a_login_view(request)

    # # user = request.user
    # # context['user_form'] = user
    
    # #context['logout_form'] = form_out
    # context['login_form'] = form_l
    # context['registration_form'] = form_r
    # context['account_form'] = form_a

    current_url_name = request.path

    # poster = BackgroundPoster.objects.last()
    # video = BackgroundVideo.objects.last()
    # context['poster_url'] = poster
    # context['video_url'] = video

    context['current_url'] = current_url_name
    
    context['form'] = form
    return Response(context, template_name='gbsearch_book.html', )   


# from internetarchive import get_item
# item = get_item('harrypotterdeath0000rowl_n2u6')
# print('item.exists', item.exists)   
  
