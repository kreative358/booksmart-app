from django.conf.urls import url, include
from django.urls import path

from rest_framework import routers
from booksmart.api import views


# # from rest_framework.authtoken.views import obtain_auth_token

# router = routers.DefaultRouter()
# router.register(r'books', views.BookViewSet)
# router.register(r'authors', views.AuthorViewSet)


# # router.register('books', BookViewSet, basename='book')
# # router.register('authors', AuthorViewSet, basename='author')
# urlpatterns = [
#     path('', include(router.urls,)),
#     ]