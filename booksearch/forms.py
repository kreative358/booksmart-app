from django import forms
from django.forms import ModelForm, Form
from booksmart.models import Book, Author
from django.forms.widgets import NumberInput

class MySelectWidgetNew(forms.Select):
    template_name = "my_select_widget_new.html"

class DateForm(forms.Form):
    date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'id': 'datetimepicker1',
        })
    )

class GBAuthor(forms.Form):
    author = forms.CharField(widget=forms.HiddenInput())
    language = forms.CharField(widget=forms.HiddenInput())


class BookSearch(forms.Form):

    search_params = [
        ('intitle', 'title'),
        ('inauthor', 'author'),
        ('q', 'query'),
        ('download', 'download'),
        ('filter', 'filter'),
        ('langRestrict', 'language'),
        ('maxResults', 'maxResults'),
        ('orderBy', 'order'),
        ('startIndex', 'startIndex'),
        ('inpublisher', 'publisher'),
        ('volumeId', 'volumeId'),
        ('bl_volumeId', 'bl_volumeId'),  
    ]

    intitle = forms.CharField(required=False,
        max_length=50, label='Search by book title', widget=forms.TextInput(attrs={'id':'input_text_bs_intitle', 'placeholder': 'field to enter full title of the book', 'data-title-tooltip': 'can also try searching by adding "" e.g. "Ulisses"'})) #'autofocus': True, 'required': False

    inauthor = forms.CharField(required=False,
        max_length=50, label='Search by book author', widget=forms.TextInput(attrs={'id':'input_text_bs_inauthor', 'placeholder': 'field to enter full name of the author',  'pattern':'^(\w.+\s).+|(["\'])(\w.+\s).+(["\'])$', 'data-title-tooltip': 'must contain at least two words'}))
        # 'title':'must contain at least two words\nIf it is full name please add "" e.g. "Mark Twain"'

    search_query = forms.CharField(required=False,
        max_length=50, label='Search by any parameters', widget=forms.TextInput(attrs={'id':'input_text_bs_search_query', 'placeholder': 'field to enter e.g. part author name or title', 'pattern':'[A-Za-z0-9._-]', 'data-title-tooltip':'for better results you can try add "" for query e.g. "book example" \nand to search for all entries that contain the exact phrase \n e.g. "Elizabeth Bennet" and the word "Darcy" \nbut do not contain the word "Austen", \nuse :"Elizabeth+Bennet"+Darcy-Austen'})) #, 'autofocus': True
    
    volumeId = forms.CharField(required=False,
        max_length=12, label='Search by googlebooks id', widget=forms.TextInput(attrs={'id':'input_text_bs_volumeId','placeholder': 'field to enter googlebooks id of the book', 'autofocus': True, 'pattern':'^[A-Za-z0-9._-]{12}$ ', 'data-title-tooltip':'must contain 12 characters'}))  

    search_maxResults = forms.IntegerField(required=False, min_value=1, max_value=40, label='Choose a number of results', widget=forms.NumberInput(attrs={'id': 'input_integer_bs_search_maxResults', 'data-title-tooltip': 'the maximum number of results for one search is 40'}))

    Download = [
        ('', 'select epub'),
        ('epub', 'epub'),
        ]
    download = forms.ChoiceField(required=False,
        label= 'Search by epub', choices=Download, widget=forms.Select(attrs={'id':'input_select_bs_download', 'size':'1'}))
    # , 'data-title-tooltip': 'use to try find books, usually a reading version'

    # download =  forms.ChoiceField(label= 'Search by epub, (help to find full text book)',  choices=Download, required=False, widget=MySelectWidgetNew(attrs={'id':'input_select_bs_download', 'size':1}))
  
    # download.widget.attrs.update(choices=[
    #     ('', ''),
    #     ('epub', 'epub'),]
    # )
 
    Filter = [
        ('', 'select parameters'),
        ('partial', 'partial'),
        ('full', 'full'),
        ('free-ebooks', 'free-ebooks'),
        ('paid-ebooks', 'paid-ebooks'),
        ('ebooks', 'ebooks')
    ]

    search_filter = forms.ChoiceField(required=False,
        label= 'Search by filter', choices=Filter, widget=forms.Select(attrs={'id':'input_select_bs_search_filter', 'size':1}))
    # , 'data-title-tooltip': 'use to try find books with specific parameters'

    # search_filter = forms.ChoiceField(label= 'Search by filter, (specific parameters)', required=False, choices=Filter, widget=MySelectWidgetNew(attrs={'id':'input_select_bs_search_filter', 'size':1}))
    
    Languages = [
        ('', 'select language'),
        ('en', 'English'),
        ('eo', 'Esperanto'),
        ('fr', 'French'),
        ('de', 'German'),
        ('pl', 'Polish'),
        ('pe', 'Portuguese'),
        ('es', 'Spanish'),
        ('uk', 'Ukrainian'),
    ]
    langRestrict = forms.ChoiceField(required=False,
        label= 'Search by language', choices=Languages, widget=forms.Select(attrs={'id':'input_select_bs_langRestrict', 'size':1}))

    # , 'data-title-tooltip': 'use to try find books in specific language'
    # langRestrict = forms.ChoiceField(label= 'Search by language',  required=False, choices=Languages, widget=MySelectWidgetNew(attrs={'id':'input_select_bs_langRestrict', 'size':1}))

    OrderBy = [
        ('', 'select order'),
        ('newest', 'newest'),
        ('relevance', 'relevance'),
        ]
    orderBy = forms.ChoiceField(required=False,
        label = 'Search by order', choices=OrderBy, widget=forms.Select(attrs={'id':'input_select_bs_orderBy', 'size':1}))

    # , 'data-title-tooltip': 'use to display books in a specific order' 

    # orderBy = forms.ChoiceField(label = 'Search by order',  required=False, choices= OrderBy, widget=MySelectWidgetNew(attrs={'id':'input_select_bs_orderBy', 'size':1}))

    search_startIndex = forms.IntegerField(required=False,
        label='Choose a start index search', min_value=0, widget=forms.NumberInput(attrs={'id':'input_integer_bs_search_startIndex', 'data-title-tooltip': 'use to try find books from sprcific index'}))

    search_inpublisher = forms.CharField(required=False,
        max_length=50, label='Search by book publishers', widget=forms.TextInput(attrs={'id':'input_text_bs_search_inpublisher', 'placeholder': "field to enter name of the book's publisher", 'data-title-tooltip': 'use to try find books from sprcificpublisher'}))  # , 'autofocus': True
    
    bl_volumeId = forms.CharField(required=False,
        label='Paste the link of the book', min_length=12, widget=forms.TextInput(attrs={'id':'bs_input_text_bl_volumeId', 'placeholder': "field to enter link to the book from google books", 'pattern':'^http:\/\/?\/.*id=([A-Za-z0-9._-]{12}).*|.*\/([A-Za-z0-9._-]{12})\/.*|.*\?id=([A-Za-z0-9._-]{12}\&).*$', 'data-title-tooltip': 'use to try find books using the link containing google books id'}))  #'autofocus': True,
        # ^http:\/\/?\/.*id=([A-Za-z0-9._-]{12}).*|.*\/([A-Za-z0-9._-]{12})\/.*|.*\/([A-Za-z0-9._-]{12})?.*$
        # ^http:\/\/?\/.*id=([A-Za-z0-9._-]{12})\/.*|.*id=([A-Za-z0-9._-]{,12})+?[&].*|.*\/([A-Za-z0-9._-]{12})\/.*|.*\/([A-Za-z0-9._-]{12})?.*

        # ^http:\/\/?\/.*id=([A-Za-z0-9._-]{12}).*|.*\/([A-Za-z0-9._-]{12})\/.*|.*\?id=([A-Za-z0-9._-]{12}\&).*$