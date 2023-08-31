from django.urls import path
from booksearch.req_author import addx_author, addauthor
from booksearch.req_book import addx_book, addbook

from booksearch.views import (
    gbsearch_book, )

app_name = 'booksearch'

urlpatterns = [

    path('gbsearch_book/', gbsearch_book, name='gbsearch_book'),
    path('addx_author/', addx_author, name='addx_author'),
    path('addx_book/', addx_book, name='addx_book'),
    path('addx_book/addbook/', addbook, name='addbook'),
    path('addx_author/addauthor/', addauthor, name='addauthor'),

   # path('addx_author/ajax_info/', addauthor, name='addauthor'),
]