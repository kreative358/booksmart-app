from django.contrib import admin
from booksmart.models import Book, Author, BackgroundPoster, BackgroundVideo #, BackgroundMusic #, Language #, BookInstance
try:
    from booksmart.models import BackgroundMusic
except:
    pass
from accounts.models import Account, MyAccountManager

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    readonly_fields = ['id']
    list_display = ['id', 'author_name', 'last_name',
                    'first_name', 'date_of_birth', 'date_of_death', 'wiki_idx', 'owner']
    fields = ['author_name', 'wiki_idx','first_name', 'last_name', ('date_of_birth', 'date_of_death'), 'author_wiki_link_d', 'author_wiki_link', 'author_wiki_img', 'owner', 'user_num_a']
    search_fields = ['author_name', 'last_name'] 
    list_display_links = ['author_name', ]

# admin.site.register(Author, AuthorAdmin)
    
class BookAdmin(admin.ModelAdmin):
    """Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of book instances in book view (inlines)
    """
    readonly_fields = ['id']
    fields = ['google_id', 'title', 'author', 'surname', 'author_c', 'published', 'category', 'summary', 'isbn', 'owner', 'user_num_b', 'url_pdf', 'url_pdf_search', "pdf_search_filename", "url_libgen"]
    list_display = ('id','title', 'author', 'surname', 'category', 'epub', 'google_id', 'owner', 'author_c',) # ('EPUB', 'embeddable'),'author_c__author_name, 
    list_per_page = 10
    search_fields = ['google_id', 'title', 'author', 'published', 'category', 'summary', 'isbn', 'created_at']
    # list_filter = ['author_c.author_name']
    # autocomplete_fields = ('author_c__author_name',)

    list_display_links = ('id', 'title')

admin.site.register(Book, BookAdmin)

# admin.site.register(Book)

admin.site.register(BackgroundPoster)
admin.site.register(BackgroundVideo)

if BackgroundMusic:
    admin.site.register(BackgroundMusic)
elif not BackgroundMusic:
    pass