import os, re, json, time, requests, datetime
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer
from booksmart.models import url_img, url_img_author, Book, Author, BackgroundPoster, BackgroundVideo
from rest_framework.response import Response
from rest_framework.views import APIView
from booksmart.forms import ItemsSearchForm
from rest_framework.authentication import TokenAuthentication
from accounts.api.views import AccountViewSet, UserDetailViewSet, UserViewSet
from booksmart.api.views import BooksEditViewSet, AuthorViewSet, BooksFullViewSet
from django.views import generic

context_main = {}

context_main['no_date'] = datetime.date(3000, 1, 1)
context_main['url_img_book'] = url_img
context_main['url_img_author'] = url_img_author

try:
    if Book.objects.all():
    # if Book.objects.filter().all():
        all_books = Book.objects.all()
        # context_list.append(all_books)
        num_books = Book.objects.all().count()
        context_main['allbooks'] = all_books
        context_main['num_books'] = num_books
    elif not Book.objects.all():
    # elif not Book.objects.filter().all():
        context_main['allbooks'] = None
        context_main['num_books'] = 0
except:
    print("booksmart models 335 no Book.objects.all():")
    pass

try:
    if Author.objects.all():
    # if Author.objects.filter().all():
        all_authors = Author.objects.all()
        # context_list.append(all_authors)
        num_authors = Author.objects.all().count()
        context_main['allauthors'] = all_authors
        context_main['num_authors'] = num_authors
    elif not Author.objects.all():
    #elif not Author.objects.filter().all():
        context_main['allauthors'] = None
        context_main['num_authors'] = 0
except:
    print("booksmart models 351 no Author.objects.all():")
    pass

try:
    if BackgroundPoster.objects.filter().last():
        poster = BackgroundPoster.objects.filter().last()
        context_main['poster_url_1'] = poster.link_poster_1
        context_main['poster_url_2'] = poster.link_poster_2
    elif not BackgroundPoster.objects.filter().last():
        context_main['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
        context_main['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
except:
    print("booksmart models 367 no BackgroundPoster.objects.filter().last():")
    pass

try:
    if BackgroundVideo.objects.filter().last():   
        video = BackgroundVideo.objects.filter().last()
        context_main['video_url'] = video.link_video
        context_main['video_type'] = video.type_video
    elif not BackgroundVideo.objects.filter().last():
        context_main['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
        context_main['video_type'] = "mp4"
except:
    print("booksmart models 367 no BackgroundVideo.objects.filter().last():")
    pass

try:
    if BackgroundMusic.objects.filter().last():   
        music = BackgroundVideo.objects.filter().last()
        context_main['music_url_1'] = music.link_music_1
        context_main['music_type_1'] = music.type_music_1
        context_main['music_url_2'] = music.link_music_2
        context_main['music_type_2'] = music.type_music_2
    elif not BackgroundMusic.objects.filter().last(): 
        context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_main['music_type_1'] = "mp3"
        context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_main['music_type_2'] = "mp3"
except:
    context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
    context_main['music_type_1'] = "mp3"
    context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
    context_main['music_type_2'] = "mp3"

class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book


class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


# def get_user(request):
#     user=request.user
#     if user.is_authenicated:
#         get_id = {}
#         print('booksmar.views user.id:', user.id)
#         get_id['user_id']=user.id
#         print(" booksmar.views get_id['user_id']", get_id['user_id'])
#         userid = get_id['user_id']
#         print('booksmar.views userid', userid)
#         return userid
#     else:
#         print('booksmar.views None')
#         return None


# print(list(set(Book.objects.values_list('author', 'author'))))
# cont = {}

# user_recs =  [("", "")]

# @api_view(['GET', 'POST'])
# @permission_classes([])
# # @authentication_classes([]) # TokenAuthentication
# @renderer_classes([TemplateHTMLRenderer])
# def index_home(request, *args):
#     """View function for home page of site."""
#     user = request.user
#     context_a = {}

#     form_search = ItemsSearchForm()

#     context_a['user'] = user
#     context_a['form_search'] = form_search
#     context_a['gb_books'] = r"https://books.google.com/"


#     if user.is_authenticated:
#         cont['user_id'] = user.id
#         context_a['user'] = user
#         print('user.id', user.id)
#         if Book.objects.filter(owner__id=user.id):
#             global books_user
#             books_user = Book.objects.filter(owner__id=user.id)
#             context_a['books_user'] = str(books_user)
#             for book_user in books_user:
#                 user_recs.append((f'"{book_user.title}", "{book_user.author}"'))

#             user_books = Book.objects.filter(owner__id=user.id).values_list('title', 'author')    
#             print('user_books', user_books)
#             return Response(context_a, template_name='index_home.html', )
#         elif not Book.objects.filter(owner__id=user.id):
#             messages.info(request, 'you have any own books yet here')
            
#     else:
#         context_a['user'] = "Anonymuous"

#     if get_current_user():
#         print('get_current_user', get_current_user())
#     else:
#         print('no get_current_user')
#     # context_a['CustomAuthToken']= CustomAuthToken
#     return Response(context_a, template_name='index_home.html', )
#     # return render(request, 'index.html', context_a)



# from django.views import generic

# books_no = Book.objects.filter(author_c__isnull=True)
# books_no_id = [book.id for book in books_no]
# for book in books_no:
#     if Author.objects.filter(last_name=book_no.surname):
#         author_class = Author.objects.filter(last_name=book_no.surname).last()    
#         book.author_c = author_class
#         book.save()
#         print('yes')
#     elif not Author.objects.filter(last_name=book_no.surname):
        
#         print('no author_c for', book.surname)


# books_no = Book.objects.filter(author_c__isnull=True)
# books_no_id = [book.id for book in books_no]
# for book in books_no:
#     if Author.objects.filter(author_name=book_no.author):
#         author_class = Author.objects.filter(author_name=book_no.author).last()    
#         book.author_c = author_class
#         book.save()
#         print('yes')
#     elif not Author.objects.filter(author_name=book_no.author):
#         print('no author_c for', book.author)
#     else:
#         pass
# for book_id in books_no_id:
#     book_id = books_no_id.pop()
#     no_book = Book.objects.get(id=book_id)
#     try:
#         no_author = Author.objects.filter(author_name=no_book.author)
#         if no_author:
#             no_book.author_c = no_author
#             no_book.save()
#             print(no_book.title)
#         else:
#             print('no', no_book.title)
#     except:
#         print("no way")



    # book_no = Book.objects.get(id=book.id)
    # try:
    #     author_no = Author.objecs.filter(author_name = book_no.author)
    #     book_no.author_c = author_no
    #     book_no.save()
    #     print('yes')
    # except:
    #     print('no')

