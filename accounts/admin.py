from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff', )
    search_fields = ('username', 'email',)
    readonly_fields=('id', 'date_joined', 'last_login')
    fields = ('id', 'password', 'username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
# admin.site.register(Account)
