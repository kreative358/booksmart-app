from django import forms
from django.db import models
from django.forms import ModelForm, Form
from booksmart.models import Book, Author, BackgroundPoster, BackgroundVideo #, BackgroundMusic
# from booksmart.models import CurrentUser
from django.utils.html import format_html
from django.conf.global_settings import LANGUAGES
#import django_filters
#from psycopg2.extras import DateRange
from django.db.models import Q
from django.forms.widgets import NumberInput, DateTimeBaseInput
from django.contrib.admin.widgets import AdminDateWidget
#import django_filters
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import Account, MyAccountManager
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import requests
# from crum import get_current_user

try:
    from booksmart.models import BackgroundMusic
except:
    pass


class MyFlatPickrDateStart(forms.DateInput):
    template_name = "my_flatpickr_date_start.html"

class MyFlatPickrDateEnd(forms.DateInput):
    template_name = "my_flatpickr_date_end.html"

class MyFlatPickrDatePubl(forms.DateInput):
    template_name = "my_flatpickr_date_publ.html"

class MyFlatPickrPureDateStart(forms.DateInput):
    template_name = "my_flatpickr_pure_date_start.html"

class MyFlatPickrPureDateEnd(forms.DateInput):
    template_name = "my_flatpickr_pure_date_end.html"


class MySelectWidget(forms.Select):
    template_name = "my_select_widget_new.html"



# user = get_current_user()
# if user:
#     print('user.pk:', user.pk)
# else:
#     print('error again')

# from django_currentuser.middleware import (
#     get_current_user, get_current_authenticated_user)
# from accounts.models import get_user

# print('get_user:', list(get_current_user))
class PdfReader(forms.Form):
    link_book_gd = forms.CharField(
        max_length=120, label='book in pdf from google drive', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'field to enter link to book in pdf from drive google', 'autofocus': True, 'id':'input_text_pdfreader_gd'})) 

    link_book_gb = forms.CharField(
        max_length=120, label='book in pdf from google books', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'field to enter link to book in pdf from google books', 'autofocus': True, 'id':'input_text_pdfreader_gb'})) 

    link_book_dc = forms.CharField(
        max_length=120, label='book in any format doc google', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'field to enter link to book in pdf from other sources', 'autofocus': True, 'id':'input_text_pdfreader_dc'})) 

    link_book_sejda = forms.CharField(
        max_length=120, label='book in pdf sejda', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'field to enter link to book in pdf from other sources', 'autofocus': True, 'id':'input_text_pdfreader_sejda'}))


class PdfReaderAdmin(forms.Form):
    link_book = forms.CharField(
        max_length=50, label='Search by book title', required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'field to enter part or full title of the book', 'autofocus': True, 'id':'pdfreader'}))  

class PageForm(forms.Form):
    page_number = forms.IntegerField(label='page number', required=False, widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': 'field to enter part or full title of the book', 'autofocus': True, 'id':'input_text_pageform'}))
    book_google_id = forms.CharField(widget=forms.HiddenInput())




# class BackgroundFormGet(forms.Form):
#  
#     url_poster = forms.URLField(max_length=100, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'poster', 'autofocus': True, 'id':'bs_input_lb'}))  
#     url_video = forms.URLField(max_length=100, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'video', 'autofocus': True, 'id':'bs_input_lb'})) 
 
class BackgroundFormPoster(forms.ModelForm):
    link_poster_1 = forms.URLField(max_length=100, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'poster 1', 'autofocus': True, 'id':'input_url_poster_1'}))
    link_poster_2 = forms.URLField(max_length=100, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'poster 2', 'autofocus': True, 'id':'input_url_poster_2'}))
    class Meta:
        model = BackgroundPoster
        fields = ['link_poster_1', 'link_poster_2']
  

class BackgroundFormVideo(forms.ModelForm):
    link_video = forms.URLField(max_length=100, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'link video', 'autofocus': True, 'id':'input_text_link_video'})) 
    type_video = forms.CharField(max_length=6, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'type video', 'autofocus': True, 'id':'input_text_type_video'}))
    class Meta:
        model = BackgroundVideo
        fields = ['link_video', 'type_video']

if BackgroundMusic:
    class BackgroundFormMusic(forms.ModelForm):
        link_music_1 = forms.URLField(max_length=100, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'link music 1', 'autofocus': True, 'id':'input_text_link_music_1'})) 
        type_music_1 = forms.CharField(max_length=6, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'type music 1', 'autofocus': True, 'id':'input_text_type_music_1'}))
        link_music_2 = forms.URLField(max_length=100, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'link music 2', 'autofocus': True, 'id':'input_text_link_music_2'})) 
        type_music_2 = forms.CharField(max_length=6, label='', required=False, widget=forms.TextInput(attrs={ 'placeholder': 'type music 2', 'autofocus': True, 'id':'input_text_type_music_1'}))
        class Meta:
            model = BackgroundMusic
            fields = ['link_music_1', 'type_music_1', 'link_music_2', 'type_music_2']
elif not BackgroundMusic:
    pass



class CurrentUserRecords(forms.Form):
    pass
    # # model_choices = forms.ModelMultipleChoiceField(
    # #     widget = forms.CheckboxSelectMultiple,
    # #     queryset = Book.objects.filter(owner=request.user),
    # #     initial = 0
    # #     )
    # user_books = forms.ChoiceField(
    #     widget = forms.CheckboxSelectMultiple,
    #     queryset = Book.objects.filter(owner__id=get_current_user.id) if get_current_user else Book.objects.all() ,
    #     initial = 0
    #     )

from django.http import JsonResponse
def userid(request):
    user_id = request.GET.get('user_id', None)
    data = {'get_user_books': Book.objects.filter(user_num_b=user_id)}
    # print('JsonResponse(data):', JsonResponse(data))
    return JsonResponse(data)

user_ids = []
class IdUser(forms.Form):
    user_id = forms.CharField(widget=forms.HiddenInput())
    if user_id:
        print('IdUser', user_id)

class AuthorRecords(forms.ModelForm):
    author_c = forms.ModelChoiceField(queryset = Author.objects.all(), label="choose author from list", required=False, widget=forms.Select(attrs={'id':'input_text_authorrecords'}))
    class Meta:
        model = Book
        fields = ['author_c']

class ItemsSearchForm(forms.Form):
    search_field = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={ 'placeholder': 'field to enter any book params', 'autofocus': True, 'id':'input_text_search_q'})) 

class BooksAuthor(forms.Form):
    author_name_hidden = forms.CharField(widget=forms.HiddenInput(attrs={}))
    # author_name_hidden = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'author_hidden_input'}))
    # author = forms.CharField(widget=forms.HiddenInput(attrs={}))

class LibrarySearch(forms.Form):
    title_lib = forms.CharField(widget=forms.HiddenInput())
    # author_search = forms.CharField(widget=forms.HiddenInput())

class BookDownload(forms.Form):
    title_download_search = forms.CharField(widget=forms.HiddenInput(attrs={}))
    

class BookChange(forms.Form):
    user_add = forms.CharField(widget=forms.HiddenInput())

# from bootstrap4.widgets import RadioSelectButtonGroup
class BookSort(forms.Form):
    SORT = [
        ('', 'select sort option'),
        ('title', 'title: A-Z'),
        ('-title', 'title: Z-A'),
        ('surname', 'author: A-Z'),
        ('-surname', 'author: Z-A'),
        ('published', 'published: newest'),
        ('-published', 'published: oldest'),
        ('created_at', 'created: newest'),
        ('-created_at', 'created: oldest'),
    ]


    sorting = forms.ChoiceField(required=False, label='', choices=SORT, widget=forms.Select(attrs={"id":"input_choice_sorting", 'class': "bs_input_sort", "size":"11", "name":"sortlist", "form":"sortform", }))

    #sorting = forms.ChoiceField(required=True, label='', choices=SORT)

# class ChoiceField(choices: Union[_FieldChoices, Callable[[], _FieldChoices]]=..., required: bool=..., widget: Optional[Union[Widget, Type[Widget]]]=..., label: Optional[Any]=..., initial: Optional[Any]=..., help_text: str=..., error_messages: Optional[Any]=..., show_hidden_initial: bool=..., validators: Sequence[Any]=..., localize: bool=..., disabled: bool=..., label_suffix: Optional[Any]=...)
    # sorting = forms.ChoiceField(required=False, label='', choices=SORT, widget=RadioSelectButtonGroup)

class BookFormView(ModelForm):
    class Meta:
        model = Book
        fields = ['google_id', 'title', 'author', 'published', 'isbn','preview_link', 'summary', 'category', 'language', 'imageLinks', 'selfLink', ]

class UrlPathForm(forms.Form):
    url_path = forms.CharField(widget=forms.HiddenInput())

# class DateInput(DateTimeBaseInput):
#     format_key = 'DATE_INPUT_FORMATS'
#     template_name = 'django/forms/widgets/date.html'




class BookForm(ModelForm):
    # user_num_b = forms.IntegerField(disabled=True)
    class Meta:
        model = Book
        fields = ['id', 'google_id', 'title', 'author', 'category', 'summary', 'published', 'preview_link', 'language', 'imageLinks', 'selfLink', 'isbn', 'epub', 'embeddable', 'preview_link_new']
        labels = {
            'google_id': 'google identity',
            'title': 'title of book',
            'author': 'author of book', 
            'category': 'book category',
            'summary': 'book summary',
            'published': 'date published book',
            'preview_link': 'google book link',
            'language': 'book language',
            'imageLinks': 'link to book cover',
            'selfLink': 'google books apis link',
            'isbn': 'industry identity',
            'epub': 'is for free to read',
            'embeddable': 'possibility to read',
            'preview_link_new': 'new google books link',
            
        }
        widgets = {
            'google_id': forms.TextInput(attrs={'placeholder':'enter the book id in google books', 'id':'input_text_google_id'}),
            'title': forms.TextInput(attrs={'placeholder':'enter the title of the book', 'id':'input_text_book_title'}),
            'author': forms.TextInput(attrs={'placeholder':'enter book author', 'id':'input_text_book_author'}),
            'category': forms.TextInput(attrs={'placeholder':'enter the category or type of the book', 'id':'input_text_book_category'}),
            'summary': forms.Textarea(attrs={'placeholder': 'enter a description or summary of the book', 'id':'input_text_book_summary'}),
            'published': MyFlatPickrDatePubl(format='%m/%d/%Y', attrs={'id': 'input_date_publ', 'placeholder':'mm/dd/yyyy', 'autocomplete':'off', 'maxlength':10, 'size':10, 'pattern':'^(0[1-9]|1[1,2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$'}),
            # 'published': forms.NumberInput(attrs={'type': 'date', 'id':'bs_input'}),

            # 'published': forms.DateInput(attrs={'type': 'date', 'id':'bs_input'}),
            # 'published': MyFlatpickr(attrs={'class': 'form_control'}),

            # 'published': forms.NumberInput(attrs={'type': 'date', 'class':'pickr_booksmart'}),
            #'published': forms.NumberInput(attrs={'template_name':'snippets-booksmart/date_picker_published.html','type': 'date', 'id':'published'}),

            'preview_link': forms.TextInput(attrs={'placeholder':'google book link', 'id':'input_text_book_preview_link'}),
            'language': forms.TextInput(attrs={'placeholder':'enter book language', 'id':'input_text_book_language'}),
            'imageLinks': forms.TextInput(attrs={'placeholder': 'link to book cover', 'id':'input_text_book_imagelinks'}),
            'selfLink': forms.TextInput(attrs={'placeholder': 'google books apis link', 'id':'input_text_book_selflink'}),
            'isbn': forms.TextInput(attrs={'placeholder':'enter identity book ISBN', 'id':'input_text_book_isbn'}),
            'epub': forms.TextInput(attrs={'placeholder':'enter information whether the book is available for free', 'id': 'input_text_book_epub'}),
            'embeddable': forms.TextInput(attrs={'placeholder':'enter information whether the book is available for free', 'id':'input_text_book_embeddable'}),
            'preview_link_new': forms.TextInput(attrs={'placeholder':'google book new link', 'id':'input_text_book_preview_link_new'}),
            
        }
        # 'author_c': forms.Select(attrs={'id':'bs_input'}),
        # fields[0].widget.attrs.update({'class': 'text-uppercase'})
        widgets['title']=forms.TextInput(attrs={'class': 'text-uppercase', 'placeholder':'', 'id':'input_text_book_title' })

# class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
#     def label_from_instance(self, member):
#         return "%s" % member.name

# class SearchRecord(forms.Form):

# from rest_framework import filters
# # from django_filters import rest_framework as filters
# # class IsOwnerFilterBackend(filters.BaseFilterBackend):
# class IsOwnerFilter(filters.BaseFilterBackend):   
#     def filter_userset(self, request, queryset, view):
#         global user
#         user = request.user
#         # global owner_user
#         # owner_user = queryset.filter(owner=user)
#         # return owner_user
#         return user

#     # def user_querytset(self, request, queryset, view):
#     #     return Book.objects.filter(owner=request.user)
# # IsOwnerFilter.filter_userset = classmethod(IsOwnerFilter.filter_userset)
# data_IsOwnerFilter = IsOwnerFilter()
# print('data_IsOwnerFilter', data_IsOwnerFilter)


# class IsOwnerFilterBackend(filters.BaseFilterBackend):
#     """
#     Filter that only allows users to see their own objects.
#     """
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(owner=request.user)

# data_IsOwnerFilterBackend=IsOwnerFilterBackend()
# print('data_IsOwnerFilterBackend', data_IsOwnerFilterBackend.__dict__)
 




# queryset_owner = [[("", "")],]
# def queryset_books(request):
#     user = request.user
#     user_owner = [("", "")]
#     if Book.objects.filter(user_num_b=user.id).count() == 0:
#         user_owner = [("", "")]
#         queryset_owner.append(user_owner)
#         return user_owner

#     # return user.owner_set.all() #many to many
#     # else:
#         # return Book.objects.filter(user_num_b=user.id)
#     user_owner = [("", "")] + [Book.objects.filter(user_num_b=user.id).values_list('title', 'title')]
#     queryset_owner.append(user_owner)
#     return user_owner
        
#     # return user_owner

# if queryset_owner:
#     print('queryset_books[-1]', queryset_owner[-1])
#     print('queryset_books', queryset_owner)
# else:
#     print('NO queryset_books[-1]')


# user_nums = []
# def user_id(request):
#     user = request.user
#     user_num = user.id
#     user_nums.append(user_num)
#     return user_num   

# if user_nums:
#     print('user_nums:', user_nums)
# else:
#     print('NO user_nums')

# from booksmart.views import cont

# print('cont:', cont)
# cur_user = CurrentUser.objects.last()
# print('cur_user', cur_user)

class SearchRecord(forms.ModelForm):
# class SearchRecord(forms.Form):
    user_num_b = forms.BooleanField(label='Search your book', required=False, widget=forms.CheckboxInput(attrs={'id':'input_checkbox_sr_user_num_b', 'type':'checkbox','required': 'False'}))

    epub = forms.BooleanField(label='Search book to read', required=False, widget=forms.CheckboxInput(attrs={'id':'input_checkbox_sr_epub','type':'checkbox','required': 'False'}))

    title = forms.CharField(max_length=50, label='Search by book title', required=False, widget=forms.TextInput(attrs={'id':'input_text_sr_title', 'placeholder': 'field to enter part or full title of the book', 'autofocus': True}))  

    # class CharField(max_length: Optional[Any]=..., min_length: Optional[Any]=..., strip: bool=..., empty_value: Optional[str]=..., required: bool=..., widget: Optional[Union[Widget, Type[Widget]]]=..., label: Optional[Any]=..., initial: Optional[Any]=..., help_text: str=..., error_messages: Optional[Any]=..., show_hidden_initial: bool=..., validators: Sequence[Any]=...
    
    author = forms.CharField(min_length=5, max_length=50, label='Search by book author', required=False, widget=forms.TextInput(attrs={'id':'input_text_sr_author', 'placeholder': "field to enter part or full author name" , 'autofocus': True, 'pattern':'(\w.+\s).+', 'title':'must contain at least two words'})) 

    google_id = forms.CharField(
        max_length=12, label='Search by book google id', required=False, widget=forms.TextInput(attrs={'id':'input_text_sr_google_id', 'placeholder': "field to enter google books, book identity" , 'autofocus': True})) 

    Languages=(
        ('', 'select language'),
        ('en', 'English'),
        ('eo', 'Esperanto'),
        ('fr', 'French'),
        ('de', 'German'),
        ('pl', 'Polish'),
        ('pe', 'Portuguese'),
        ('ru', 'Russian'),
        ('es', 'Spanish'),
        ('uk', 'Ukrainian')
    )
    language = forms.ChoiceField(label= 'Search by language', choices=Languages, required=False, widget=forms.Select(attrs={'id':'input_select_sr_language'}))

    Order = [
        ('', 'select order'),
        ('title', 'title-ascending'),
        ('-title', 'title-descending'),
        ('surname', 'author-ascending'),
        ('-surname', 'author-descending'),
        ('published', 'published-ascending'),
        ('-published', 'published-descending'),
    ]
   
    ordering = forms.ChoiceField(label = 'sort by',  required=False, choices = Order, widget=forms.Select(attrs={'id':'input_select_sr_ordering'}))

    try:
        author_list = forms.ChoiceField(label= 'Search by author', choices=  [("", "select author")] + list(set(Book.objects.values_list('author', 'author'))), required=False, widget=forms.Select(attrs={'id':'input_select_sr_author_list'}))
    except:
        # print("booksmart forms 376 no author_list")
        author_list = forms.ChoiceField(label= 'Search by author', choices=  [("", "select author")], required=False, widget=forms.Select(attrs={'id':'input_select_sr_author_list'}))
        pass

    published__gte = forms.DateField(label='Start date publish', widget=NumberInput(attrs={'type':'date', 'id':'input_date_start', 'placeholder':'mm/dd/yyyy', 'autocomplete':'off', 'maxlength':10, 'size':10, 'pattern':'^(0[1-9]|1[1,2])\/(0[1-9]|[12][0-9]|3[01])\/d{4}$'}), required=False)

    published__lt = forms.DateField(label='End date publish', widget=NumberInput(attrs={'type':'date', 'id':'input_date_end', 'placeholder':'mm/dd/yyyy', 'autocomplete':'off', 'maxlength':10, 'size':10, 'pattern':'^(0[1-9]|1[1,2])\/(0[1-9]|[12][0-9]|3[01])\/d{4}$'}), required=False)

    # published__gte = forms.DateField(label='Start date publish', required=False,widget=MyFlatPickrDateStart(format='%m/%d/%Y', attrs={'id':'input_date_start', 'placeholder':'mm/dd/yyyy', 'autocomplete':'off', 'maxlength':10, 'size':10, 'pattern':'^(0[1-9]|1[1,2])\/(0[1-9]|[12][0-9]|3[01])\/d{4}$'}))
    # published__lt = forms.DateField(label='End date publish', required=False,widget=MyFlatPickrDateEnd(format='%m/%d/%Y', attrs={'id':'input_date_end', 'placeholder':'mm/dd/yyyy', 'autocomplete':'off', 'maxlength':10, 'size':10, 'pattern':'^(0[1-9]|1[1,2])\/(0[1-9]|[12][0-9]|3[01])\/d{4}$'})) 

    # published__gte = forms.DateField(label='Start date publish', widget=NumberInput(attrs={'type': 'date', 'id':'bs_input_sp'}), required=False)
    # published__lt = forms.DateField(label='End date publish', widget=NumberInput(attrs={'type': 'date', 'id':'bs_input_sp'}), required=False)

    # owner = forms.ChoiceField(
    #     label='Search by book owner', required=False, widget=forms.CheckboxSelectMultiple(attrs={'class': "form-control", 'autofocus': True, 'value':'get_current_user'}))  

    owner__username = forms.CharField(
        max_length=50, label='Search by book owner', required=False, widget=forms.TextInput(attrs={'placeholder': 'field to enter part or full owner username', 'autofocus': True, 'id':'input_text_sr_owner'})) 

    # class ChoiceField(choices: Union[_FieldChoices, Callable[[], _FieldChoices]]=..., required: bool=..., widget: Optional[Union[Widget, Type[Widget]]]=..., label: Optional[Any]=..., initial: Optional[Any]=..., help_text: str=..., error_messages: Optional[Any]=..., show_hidden_initial: bool=..., validators: Sequence[Any]=..., localize: bool=..., disabled: bool=..., label_suffix: Optional[Any]=...)
 
    class Meta:
        model= Book
        fields = ['user_num_b', 'epub', 'title', 'author', 'google_id', 'language', 'published__gte', 'published__lt', 'owner__username', 'author_list', 'ordering'] # , 'user_owner'
        # fields_order = ['title', 'surname']

    # author_c = forms.ChoiceField(queryset=None, label= 'Choose author', required=False, widget=forms.Select(attrs={'id':'bs_input_c'}))

    # author_c = forms.ChoiceField(label= 'Choose author', choices=author_c, required=False, widget=forms.Select(attrs={'id':'bs_input_c'}))

    # class Meta:
    #     model= Book
    #     fields = ['user_books_field', 'title', 'author', 'google_id', 'language', 'published__gte', 'published__lt', 'owner', 'author_c']
    # user = get_current_user()
    # print(user)
    # def user_records(request):

    #     context = {}
    #     user = request.user
    #     if user.is_authenticated:

    #         user_books = forms.ModelChoiceField(
    #         widget = forms.CheckboxSelectMultiple(attrs={'type': 'date', 'id':'bs_input'}),
    #         queryset = Book.objects.filter(owner_id=user.id),
    #         initial = 0
    #         )
    #         return user_books
    #     else:
    #         return None

    # user_books = user_records

class SearchRecordNew(forms.Form):
    user_num_b = forms.BooleanField(label='Search your book', required=False, widget=forms.CheckboxInput(attrs={'type':'checkbox','required': 'False', 'id':'bs_input'}))

    title = forms.CharField(
        max_length=50, label='Search by book title', required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'field to enter part or full title of the book', 'autofocus': True, 'id':'bs_input_sp'}))  

 
    author = forms.CharField(
        max_length=50, label='Search by book author', required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "field to enter part or full author name" , 'autofocus': True, 'id':'bs_input_sp'}))  
    google_id = forms.CharField(
        max_length=12, label='Search by book google id', required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "field to enter google books, book identity" , 'autofocus': True, 'id':'bs_input_sp'})) 
    Languages=(
        ('', 'select language'),
        ('en', 'English'),
        ('eo', 'Esperanto'),
        ('fr', 'French'),
        ('de', 'German'),
        ('pl', 'Polish'),
        ('pe', 'Portuguese'),
        ('ru', 'Russian'),
        ('es', 'Spanish'),
        ('uk', 'Ukrainian')
    )
    language = forms.ChoiceField(label= 'Search by language', choices=Languages, required=False, widget=forms.Select(attrs={'id':'bs_input_c'}))

    published__gte = forms.DateField(label='Start date publish', widget=NumberInput(attrs={'type': 'date', 'id':'bs_input'}), required=False)
    published__lt = forms.DateField(label='End date publish', widget=NumberInput(attrs={'type': 'date', 'id':'bs_input'}), required=False)

    owner__username = forms.CharField(
        max_length=50, label='Search by book owner', required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'field to enter part or full owner username', 'autofocus': True, 'id':'bs_input_sp'})) 

    # author_list = forms.ChoiceField(label= 'Search by author', choices=  [("", "")] + list(set(Book.objects.values_list('author', 'author'))), required=False, widget=forms.Select(attrs={'id':'bs_input_c'}))
    try:
        author_list = forms.ChoiceField(label= 'Search by author', choices=  [("", "")] + list(set(Book.objects.values_list('author', 'author'))), required=False, widget=forms.Select(attrs={'id':'bs_input_c'}))
    except:
        print("booksmart forms 376 no author_list")
        author_list = forms.ChoiceField(label= 'Search by author', choices=  [("", "")], required=False, widget=forms.Select(attrs={'id':'bs_input_c'}))
        pass

    # user_books = forms.ChoiceField(label= 'Choose from your books', choices= queryset_owner[-1], required=False, widget=forms.Select(attrs={'id':'bs_input_c'}))

    class Meta:
        model= Book
        fields = ['user_num_b', 'title', 'author', 'google_id', 'language', 'published__gte', 'published__lt', 'owner__username', 'author_list'] # , 'user_books'


# class MyFlatpickrUni(forms.DateInput):
#     template_name = "my_flatpickr_uni.html"

class AuthorForm(ModelForm):
    #id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Author
        fields = ['id', 'author_name', 'date_of_birth', 'date_of_death','author_wiki_link', 'first_name','middle_name', 'last_name', 'wiki_idx', 'author_wiki_img', ]
        # exclude = ['date_of_birth', 'date_of_death']
        labels = {
            'author_name': 'author full name',
            'date_of_birth': 'date of birth',
            'date_of_death': 'date of death',
            'author_wiki_link': 'author summary',
            'first_name': 'author first name',
            'middle_name': 'author middle_name or names',
            'last_name': 'author surname name',
          #  'date_of_birth': 'date of birth',
          #  'date_of_death': 'date of death',
            'wiki_idx': 'author wikidata identity',
            'author_wiki_img': 'author image',
        }

        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder':'enter the full name of the author of the book', 'id':'input_text_author_name', }),

            'date_of_birth': MyFlatPickrDateStart(format='%m/%d/%Y', attrs={'id': 'input_date_start', 'placeholder':'mm/dd/yyyy', 'autocomplete':'off', 'maxlength':10, 'size':10, 'pattern':'^(0[1-9]|1[1,2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$'}),
            'date_of_death': MyFlatPickrDateEnd(format='%m/%d/%Y', attrs={'id': 'input_date_end', 'placeholder':'mm/dd/yyyy', 'autocomplete':'off', 'maxlength':10, 'size':10, 'pattern':'^(0[1-9]|1[1,2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$'}), 

            'author_wiki_link': forms.Textarea(attrs={'placeholder':'enter information about the author of the book', 'id': 'input_text_author_wiki_link'}),
            'first_name': forms.TextInput(attrs={'placeholder':'enter the name of the author of the book', 'id':'input_text_author_first_name' }),
            'middle_name': forms.TextInput(attrs={'placeholder':'enter the second name or names the author', 'id':'input_text_author_middle_name' }),
            'last_name': forms.TextInput(attrs={'placeholder':'enter the surname of the author of the book', 'id':'input_text_author_last_name'}),

            # 'date_of_birth': MyFlatPickrDateBirth(format='%m/%d/%Y', attrs={'id': 'input_date_birth', }),
            # 'date_of_birth': forms.NumberInput(attrs={'type': 'date', 'id':'bs_input'}), 
            # 'date_of_death': forms.NumberInput(attrs={'type': 'date', 'id':'bs_input'}),

            #'type': 'date',
            # 'date_of_death': forms.TextInput(attrs={'id':'bs_input'}), #'type': 'date',
            # 'date_of_death': MyFlatpickrAuthorDeath(attrs={'id':'input_date_death'}),

            'wiki_idx': forms.TextInput(attrs={'placeholder':'enter wikidata author indentity', 'id':'input_text_author_wiki_idx' }),
            'author_wiki_img': forms.URLInput(attrs={'placeholder':'enter link to author image', 'id':'input_text_author_wiki_img' }),
            
            }
        
            # 
            #  'date_of_birth': forms.DateInput(
            # attrs={'placeholder': '__/__/____', 'class': 'date',}),
            # 'date_of_death': forms.DateInput(format='%m/%d/%Y'),
            # forms.DateField(widget=AdminDateWidget())
            # forms.DateField(widget = forms.SelectDateWidget)


class NewAuthorForm(ModelForm):
    #id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Author
        fields = ['id', 'author_name', 'date_of_birth', 'date_of_death','author_wiki_link', 'first_name','middle_name', 'last_name', 'wiki_idx', 'author_wiki_img', ]
        # exclude = ['date_of_birth', 'date_of_death']
        labels = {
            'author_name': 'author full name',
            'date_of_birth': 'date of birth',
            'date_of_death': 'date of death',
            'author_wiki_link': 'author summary',
            'first_name': 'author first name',
            'middle_name': 'author middle_name or names',
            'last_name': 'author surname name',
          #  'date_of_birth': 'date of birth',
          #  'date_of_death': 'date of death',
            'wiki_idx': 'author wikidata identity',
            'author_wiki_img': 'author image',
        }

        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder':'enter the full name of the author of the book', 'id':'bs_input_ab' }),

            'date_of_birth': MyFlatPickrDateStart(format='%m/%d/%Y', attrs={'id': 'input_date_start', 'placeholder':'mm/dd/yyyy', 'autocomplete':'off', 'maxlength':10, 'size':10, 'pattern':'[0-9]{2}/[0-9]{2}/[0-9]{4}'}),
            'date_of_death': MyFlatPickrDateEnd(format='%m/%d/%Y', attrs={'id': 'input_date_end', 'placeholder':'mm/dd/yyyy', 'autocomplete':'off', 'maxlength':10, 'size':10, 'pattern':'[0-9]{2}/[0-9]{2}/[0-9]{4}'}), 

            'author_wiki_link': forms.Textarea(attrs={'class': 'form_control', 'placeholder':'enter information about the author of the book', 'id':'bs_input' }),
            'first_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder':'enter the name of the author of the book', 'id':'bs_input_ab' }),
            'middle_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder':'enter the second name or names the author', 'id':'bs_input_ab' }),
            'last_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder':'enter the surname of the author of the book', 'id':'bs_input_ab' }),

            # 'date_of_birth': MyFlatPickrDateBirth(format='%m/%d/%Y', attrs={'id': 'input_date_birth', }),
            # 'date_of_birth': forms.NumberInput(attrs={'type': 'date', 'id':'bs_input'}), 
            # 'date_of_death': forms.NumberInput(attrs={'type': 'date', 'id':'bs_input'}),

            #'type': 'date',
            # 'date_of_death': forms.TextInput(attrs={'id':'bs_input'}), #'type': 'date',
            # 'date_of_death': MyFlatpickrAuthorDeath(attrs={'id':'input_date_death'}),

            'wiki_idx': forms.TextInput(attrs={'class': 'form_control', 'placeholder':'enter wikidata author indentity', 'id':'bs_input_ab' }),
            'author_wiki_img': forms.URLInput(attrs={'class': 'form_control', 'placeholder':'enter link to author image', 'id':'bs_input' }),
            
            }
        
            # 
            #  'date_of_birth': forms.DateInput(
            # attrs={'placeholder': '__/__/____', 'class': 'date',}),
            # 'date_of_death': forms.DateInput(format='%m/%d/%Y'),
            # forms.DateField(widget=AdminDateWidget())
            # forms.DateField(widget = forms.SelectDateWidget)
        
