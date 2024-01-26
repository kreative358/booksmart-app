from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# from crum import get_current_user
from django.conf.global_settings import LANGUAGES
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from accounts.models import Account
from django.db.utils import OperationalError
from sqlite3 import OperationalError as qlite3_OperationalError
#import requests

# import uuid
# from browserapi.models import ActivityLog
# from pygments import highlight
# from pygments.formatters.html import HtmlFormatter
# from pygments.lexers import get_all_lexers, get_lexer_by_name
# from pygments.styles import get_all_styles
# from rest_framework.reverse import reverse
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser


from django.db.models.signals import class_prepared

# def add_field(sender, **kwargs):
#     """
#     class_prepared signal handler that checks for the model named
#     MyModel as the sender, and adds a CharField
#     to it.
#     """
#     if sender.__name__ == "BackgroundPoster":
#         field = models.CharField("link_poster_2", max_length=100)
#         field.contribute_to_class(sender, "link_poster_2")

# class_prepared.connect(add_field)



url_img = r'http://books.google.com/books/content?id=YS7eSh0hbDEC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'

url_img_author = r"https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Typist_using_Corona_folding_typewriter.jpg/356px-Typist_using_Corona_folding_typewriter.jpg"

# from django_currentuser.middleware import (
#     get_current_user, get_current_authenticated_user)

# if get_current_user:
#     print('booksmart models get_current_user', get_current_user)
#     print('booksmart models settings get_current_user()', get_current_user())
# else:
#     pass
# class CharField(verbose_name: Optional[Union[str, bytes]]=..., name: Optional[str]=..., primary_key: bool=..., max_length: Optional[int]=..., unique: bool=..., blank: bool=..., null: bool=..., db_index: bool=..., default: Any=..., editable: bool=..., auto_created: bool=..., serialize: bool=..., unique_for_date: Optional[str]=..., unique_for_month: Optional[str]=..., unique_for_year: Optional[str]=..., choices: Optional[_FieldChoices]=..., help_text: str=..., db_column: Optional[str]=..., db_tablespace: Optional[str]=..., validators: Iterable[_ValidatorCallable]=..., error_messages: Optional[_ErrorMessagesToOverride]=...)

# class CurrentUser(models.Model):
#     current_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, default=None)

#     def save(self, *args, **kwargs):
#         current_user = get_current_user()
#         if current_user and not current_user.pk:
#             current_user = None
#         if not self.pk:
#             self.current_user = current_user
#         super(CurrentUser, self).save(*args, **kwargs)


class BackgroundPoster(models.Model):
    link_poster_1 = models.URLField(max_length=100, null=True, blank=True,)
    link_poster_2 = models.URLField(max_length=100, null=True, blank=True,)
    def __str__(self):
        """String for representing the Model object."""
        return self.link_poster_1

# class BackgroundVideo(models.Model):
#     pass
class BackgroundVideo(models.Model):
    link_video = models.URLField(max_length=100, null=True, blank=True)
    type_video = models.CharField(max_length=6, null=True, blank=True )
    def __str__(self):
        """String for representing the Model object."""
        return self.link_video
    #link_video = models.CharField(max_length=100, blank=True, null=True)

# class BackgroundMusic(models.Model):
#     pass
class BackgroundMusic(models.Model):
    link_music_1 = models.URLField(max_length=100, blank=True, null=True)
    type_music_1 = models.CharField(max_length=6, blank=True, null=True)
    link_music_2 = models.URLField(max_length=100, blank=True, null=True)
    type_music_2 = models.CharField(max_length=6, blank=True, null=True)


class Author(models.Model):
    """Model representing an author."""
    url = models.URLField(blank=True, null=True)
    
    author_name = models.CharField(max_length=100, default='unknown')
    author_wiki_link = models.TextField(max_length=1200, blank=True)
    author_wiki_link_d = models.TextField(max_length=1200, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    wiki_idx = models.CharField(max_length=10, blank=True)
    author_wiki_img = models.URLField(max_length=300, blank=True)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    # author_book = models.OneToOneField(Book, related_name='author_books', on_delete=models.SET_NULL, blank=True, null=True)
    # book_author_title = models
    user_num_a = models.PositiveSmallIntegerField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authors', on_delete=models.SET_NULL, blank=True, null=True) # related_query_name #auto_created=True, default=serializers.CurrentUserDefault()
    created_at = models.DateTimeField(auto_now_add= True, verbose_name='date_add_author')
    modified_at = models.DateTimeField(auto_now_add= True, verbose_name='date_update_author')
    slug = models.SlugField(blank=True, null=True)
    # slug = models.SlugField(unique=True, default=uuid.uuid1)
    
    #highlighted = models.TextField()
    # activity_logs = GenericRelation(ActivityLog ,content_type_field='content_type',
    #     object_id_field='object_id', related_query_name='reader')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}'.format(self.author_name)

    def author_name_plus(self):
        return '{0}'.format(self.author_name.replace(' ', '+'))

    # def save(self, *args, **kwargs):
    #     user = get_current_user()
    #     if user and not user.pk:
    #         user = None
    #     if not self.pk:
    #         self.created_by_crum = user
    #     self.modified_by_crum = user
    #     super(Author, self).save(*args, **kwargs)

    # def save_highlighted(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code author.
    #     """
    #     lexer = get_lexer_by_name(self.language)
    #     linenos = self.linenos and 'table' or False
    #     options = self.title_highlighted and {'title': self.title_highlighted} or {}
    #     formatter = HtmlFormatter(
    #         style=self.style, linenos=linenos, full=True, **options)
    #     self.highlighted = highlight(self.code, lexer, formatter)
    #     super(Book, self).save(*args, **kwargs)
    

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    language_name = models.CharField(max_length=20,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)", blank=True)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.language_name

# def get_default_author_c():
#     return Author.objects.get_or_create(author_name="author_class")[0]


class Book(models.Model):
    url = models.URLField(blank=True, null=True)
    url_pdf = models.CharField(max_length=320, blank=True, null=True, default='')
    url_pdf_search = models.CharField(max_length=320, blank=True, null=True, default='')
    pdf_search_filename = models.CharField(max_length=120, blank=True, null=True, default='')
    google_id = models.CharField(max_length=24, default="")
    title = models.CharField(max_length=100)

    author_c = models.ForeignKey(Author, related_name='books_author', related_query_name='book_author', on_delete=models.SET_NULL, blank=True, null=True) # author_object , name="author_name"
    # content_type = models.ForeignKey(Author, related_name='content_author', on_delete=models.SET_NULL, blank=True, null=True)
    # obiect_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')

    author = models.CharField(max_length=100, blank=True) # required=True, defalult='author-unknown'
    author_wiki_idx = models.CharField(max_length=10, blank = True)
    surname = models.CharField(max_length=100, blank=True) # required=True, defalult='surname-unknown'
    published = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=48, default='unknown')
    summary = models.TextField(max_length=1200, default = 'no description')
    isbn = models.CharField('ISBN', max_length=24, unique=False,)
    language = models.CharField(max_length=12, blank=True, choices=LANGUAGES)
    epub = models.CharField('EPUB', max_length=10, blank = True)
    embeddable = models.CharField(max_length=14, blank = True)
    imageLinks = models.URLField(max_length=300, default= url_img)
    preview_link = models.URLField(max_length=300, default='no new book preview link')
    preview_link_new = models.URLField(max_length=300, blank=True, default='no new book preview link')
    selfLink = models.URLField(max_length=200, blank=True, default = 'no google apis json link')
    # accessInfo = models.CharField(max_length=24)
    
    # CATEGORY_CHOICES = [("ART", "Art"), ("ADVENTURE", "Adventure"), ("BIOGRAPHY", "Biography"), ("CHILDREN's", "Children's") , ("COMICS", "Comics"), ("COOKING", "Cooking"), ("DRAMA", "Drama"), ("ECONOMICS", "Economics"), ("FANTASY", "Fantasy"), ("FICTION", "Fiction"), ("GARDENING", "Gardending"), ("HISTORY", "History"), ("HUMAN", "Human"), ("HUMOR", "Humor"), ("LAW", "Low"), ("MEDICINE", "Medicine"), ("MUSIC", "Music"), ("NATURE", "Nature"), ("PETS", "Pets"), ("PHILOSOPHY", "Philosophy"), ("POETRY", "Poetry"), ("POLITICAL", "Political"), ("PSYCHOLOGY", "Psychology"), ("RElIGION", "Religion"), ("ROMANS", "Romans"), ("SCIENCE", "Science"), ("SPORTS", "Sports"), ("STOCKS", "Stocks"), ("TECHNOLOGY", "Technology"), ("TRAVEL", "Travel")]
    
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_by_book', on_delete=models.SET_NULL, blank=True, null=True) # auto_created=True
    # slug = models.SlugField(blank=True, unique=True)
    user_num_b = models.PositiveSmallIntegerField(blank=True, null=True) # editable=False
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='books', on_delete=models.SET_NULL, blank=True, null=True)
    # created_by_crum = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_by_crum_book', on_delete=models.SET_NULL, blank=True, null=True)
    # modified_by_crum = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_by',on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add= True, verbose_name='date add book')
    modified_at = models.DateTimeField(auto_now_add= True, verbose_name='date update book')
    slug = models.SlugField(blank=True, null=True) # unique=True
    url_libgen = models.CharField(max_length=120, blank=True, null=True, default='')
    ## pełna nazwa klasy w liczbie pojedynczej i mnogiej
    # verbose_name = 'BetterName'
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='apibooks', on_delete=models.SET_NULL, blank=True, null=True) #hidden=True
    # activity_logs = GenericRelation(ActivityLog ,content_type_field='content_type',
    #     object_id_field='object_id', related_query_name='reader')
    class Meta:
        ordering = ['title', 'surname']
        # indexes = [ 
        #     models.Index(fields=["content_type", "object_id"]),
        # ]

    def natural_key(self):
        return (self.title,) + self.author_c.natural_key()

        #permisions = [(['add','view'], 'user.is_authenticated'), (['change', 'delete', 'view',], 'owner')]

    # def save(self, *args, **kwargs):
    #     user = get_current_user()
    #     if self.author:
    #         self.surname = self.author.split()[-1]
    #     if user and not user.pk:
    #         user = None
    #     if not self.pk:
    #         self.created_by_crum = user
    #     self.modified_by_crum = user
    #     super(Book, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     """Returns the url to access a particular book instance."""
    #     # url = reverse('book-detail', args=[str(self.id)])
    #     # print('url', str(url))
    #     return reverse('book-detail', args=[str(self.id)])
        # return reverse('book-detail', kwargs={'pk' : self.pk})

    # @property
    # def author_class(self):
    #     self.book_author_c = {}
    #     book_author_c['pk'] = self.author_c.pk
    #     book_author_c['author_name'] = self.author_c.author_name
    #     book_author_c['author_wiki_link'] = self.author_c.author_wiki_link
    #     book_author_c['author_wiki_link_d'] = self.author_c.author_wiki_link_d
    #     book_author_c['first_name'] = self.author_c.first_name
    #     book_author_c['middle_name'] = self.author_c.middle_name
    #     book_author_c['last_name'] = self.author_c.last_name
    #     book_author_c['date_of_birth'] = self.author_c.date_of_birth
    #     book_author_c['date_of_death'] = self.author_c.date_of_death
    #     book_author_c['wiki_idx'] = self.author_c.wiki_idx
    #     book_author_c['author_wiki_img'] = self.author_c.wiki_img
    #     book_author_c['author_url'] = self.author_c.get_absolute_url
    #     return self.book_author_c 

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    # def save_highlighted(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    #     lexer = get_lexer_by_name(self.language)
    #     linenos = self.linenos and 'table' or False
    #     options = self.title_highlighted and {'title': self.title_highlighted} or {}
    #     formatter = HtmlFormatter(
    #         style=self.style, linenos=linenos, full=True, **options)
    #     self.highlighted = highlight(self.code, lexer, formatter)
    #     super(Book, self).save(*args, **kwargs)

    # def surname(self):
    #     surname = author.split()[-1]
    #     return surname

    # def display_genre(self):
    #     """Creates a string for the Genre. This is required to display genre in Admin."""
    #     return ', '.join([self.category.split()[0] for genre in self.genre.all()])
    #     # return ', '.join([genre.name for genre in self.genre.all()[:3]])

    # display_genre.short_description = 'Genre'

    # def user_add_book(instance)
        # user_add_id=str(instance.user_add.id)
        # return user_add_id
        

# @receiver(book_delete, sender=Book)
# def submission_delete(sender, instance, **kwargs):
#     instance.book.delete(False) 

# def pre_save_book_receiver(sender, instance, *args, **kwargs):
# 	return instance.book

# pre_save.connect(pre_save_book_receiver, sender=Book)  ## pre save receiver**

    # def save(self, *args, **kwargs):

    #     if self.google_id == "Yoko Ono's blog":
    #         return # Yoko shall never have her own blog!
    #     else:
    #         super().save(*args, **kwargs)

# class ProfileAuthor(models.Model):
#     author_class = OneToOneField(Author, on_delete=models.CASCADE)
#     author_book = GenericRelation(Book, related_query_name='author-book')
#     def __str__(self):
#         relation_author_book = f'{self.author_class.author_name-self.self.author_book.title}'
#         return relation_author_book.replace(' ', '_')
import datetime

context_bm = {}
context_list = []

context_bm['no_date'] = datetime.date(3000, 1, 1)
context_bm['url_img_book'] = url_img
context_bm['url_img_author'] = url_img_author

try:
    if Book.objects.all():
    # if Book.objects.filter().all():
        all_books = Book.objects.all()
        context_list.append(all_books)
        num_books = Book.objects.all().count()
        context_bm['allbooks'] = all_books
        context_bm['num_books'] = num_books
    elif not Book.objects.all():
    # elif not Book.objects.filter().all():
        context_bm['allbooks'] = None
        context_bm['num_books'] = 0
except Exception as err:
    print(f"booksmart models 335 no Book.objects.all(): except Exception as {err}")
    context_bm['allbooks'] = None
    context_bm['num_books'] = 0    
    

try:
    if Author.objects.all():
    # if Author.objects.filter().all():
        all_authors = Author.objects.all()
        context_list.append(all_authors)
        num_authors = Author.objects.all().count()
        context_bm['allauthors'] = all_authors
        context_bm['num_authors'] = num_authors
    elif not Author.objects.all():
    #elif not Author.objects.filter().all():
        context_bm['allauthors'] = None
        context_bm['num_authors'] = 0
except Exception as err:
    print(f"booksmart models 351 no Author.objects.all(): Exception as {err}")
    print("")
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

# def get_user(request):
#     user=request.user
#     if user:
#         print('models user.username', user.username)
#     elif not user:
#         print('models Anonymus')
#     global context_gm
#     context_gm = {}
#     if user.is_authenicated:
#         context_bm['person_id'] = user.id
#         context_bm['person_name'] = user.username
#         return context_gm
#     else:
#         context_bm['person_id'] = None
#         context_bm['person_name'] = "Anonymus"
#         return context_gm



