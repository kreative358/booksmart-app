from django.conf.urls import include, url
from django.urls import include as pathinclude
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from accounts.api.views import AccountViewSet, UserDetailViewSet, UserViewSet
from booksmart.api.views import BooksEditViewSet, AuthorViewSet, BooksFullViewSet, BooksUserViewSet
# from browserapi import views

app_name = 'browserapi'

router = DefaultRouter()
# router = SimpleRouter()-shortinfo
router.register('books', BooksEditViewSet, basename="book")
router.register('books-detail', BooksFullViewSet, basename="books-detail")
router.register('books-user', BooksUserViewSet, basename="books-user")
# router.register('book-detail', BookViewSet,)
router.register('authors', AuthorViewSet)
router.register('accounts', AccountViewSet)
router.register(r'users-detail', UserViewSet, basename= 'users-detail')
# router.register(r'user-detail', views.UserDetailViewSet, basename='user-detail')

# router.register('books', BookViewSet, basename='book')
# router.register('authors', AuthorViewSet, basename='author')


urlpatterns = [
    path('', include(router.urls)),

    ] 
