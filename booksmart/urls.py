from django.urls import path

from booksmart.book_download import (

    download_book
)

from booksmart.infoview import (
    app_users,
    pdf_reader,
    background_poster,
    background_video,
    read_page,
    )

from booksmart.views_records import (
    new_book, 
    edit_book, 
    delete_book, 
    delete_author, 
    new_author, 
    edit_author,  
    read_book, 
    read_book_ol,
    )

from booksmart.views_apiview import (
    # gbsearch,
    # RecordsView,
    all_authors, 
    all_records,
    all_records_title,
    # all_records_sort,
    all_records_author,
    authors_last,
    books_author,
    account_records,

    records_view_post,
    records_view_get
    )

from django.conf.urls import include, url
from django.urls import include as pathinclude
from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.api.views import AccountViewSet, UserDetailViewSet, UserViewSet
# from booksmart.api.views import BooksEditViewSet, AuthorViewSet, BooksFullViewSet
from booksmart import views
from django.views.generic import TemplateView as TemplateViewIndex
from django.views.generic import TemplateView as TemplateViewDemo
from django.views.generic import TemplateView



# router = DefaultRouter()

# router.register(r'books', BookViewSet, 'book')
# router.register(r'authors', AuthorViewSet, 'author')
# router.register(r'accounts', AccountViewSet, 'account')
# router.register(r'users', UserDetailViewSet,'user')
# router.register(r'user', UserViewSet, 'user-account')

# router.register('books', BookViewSet, basename='book')
# router.register('authors', AuthorViewSet, basename='author')



from booksmart.forms import userid

# from rest_framework.authtoken.views import obtain_auth_token

# router = routers.DefaultRouter()
# router.register(r'books', views.BookViewSet)
# router.register(r'authors', views.AuthorViewSet)


# router.register('books', BookViewSet, basename='book')
# router.register('authors', AuthorViewSet, basename='author')

app_name = 'booksmart'

urlpatterns = [
    # path('', include(router.urls)),
    path('app_users/', app_users, name='app_users'),
    path('app_users_login/', TemplateView.as_view(template_name="app_users_login.html"), name='app_users_login'),
    path('index/', TemplateViewIndex.as_view(template_name="index.html"),name='index'),
    path('readapi_demo/', TemplateViewDemo.as_view(template_name="readapi_demo.html"), name='readapi_demo'),
    url(r'^ajax/user_id/$', userid, name='user_id'),
    # path('gbsearch_book/', gbsearch_book, name='gbsearch_book'),
    # path('addx_author/', addx_author, name='addx_author'),
    # path('addx_book/', addx_book, name='addx_book'),
    # #path('addx/addrecord/', addrecord, name='addrecord'),
    # #path('addx/addAuthor/', addAuthor, name='addAuthor'),
    # #path('home/', home_screen_view, name='home'),
    # path('addx_book/addrecord_b/', addrecord_b, name='addrecord_b'),
    # path('addx_author/addAuthor_a/', addAuthor_a, name='addAuthor_a'),
    path('allrecords/', all_records, name='allrecords'),
    path('allrecords_title/', all_records_title, name='allrecords_title'),
    # path('allrecords_sort/', all_records_sort, name='allrecords_sort'),
    path('allrecords_author/', all_records_author, name='allrecords_author'),
    # path('records/', RecordsView.as_view(), name='records'),
    # path('records_post/', RecordsView.as_view(), {"action": "POST"}, name='records-post'),
    # path('records_get/', RecordsView.as_view(), {"action": "GET"}, name='records-get'),
    path('records_post/', records_view_post, name='records-post'),
    path('records_get/', records_view_get, name='records-get'),

    path('all_authors/', all_authors, name="allauthors"),
    path('authors_last/', authors_last, name="authorslast"),
    path('books_author/', books_author, name="booksauthor"),
    path('account-records/', account_records, name="account-records"),
    path('new_book/', new_book, name = "newbook"), 
    path('new_author/', new_author, name = "newauthor"),

    path('edit_book/<int:id>', edit_book, name = "editbook"),
    path('edit_author/<int:id>', edit_author, name="editauthor"),
    # path('submit/<int:id>', delete_book, name = "deletebook"),
    path('delete_book/<int:id>', delete_book, name = "deletebook"),
    # path('submita/<int:id>', delete_author, name = "deleteauthor"),
    path('delete_author/<int:id>', delete_author, name = "deleteauthor"),
    path('read_book/<int:id>', read_book, name = "readbook"),
    
    path('read_book_ol/<int:id>', read_book_ol, name = "readbook-ol"),

    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',
         views.AuthorDetailView.as_view(), name='author-detail'),

    path('pdf_reader/', pdf_reader, name='pdf_reader'),
    path('new_poster/', background_poster, name='newposter'),
    path('new_video/', background_video, name='newvideo'),
    path('read_page/', read_page, name='readpage'),
    # path('download_book/<int:id>', download_book, name='downloadbook'),
    path('download_book/', download_book, name='downloadbook'),

]

