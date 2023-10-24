"""booksmartapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf.urls import include as urlinclude
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from rest_framework.authtoken import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from mainsite.views import (
    index_home,
    # error_pages,
    index_home_not,
    ajax_info_1
    )
from accounts.password import (
    PasswordChangeView as PasswordChangeViewForm, 
    PasswordChangeDoneView as PasswordChangeDoneViewForm,
    PasswordResetView as PasswordResetViewForm,
    PasswordResetConfirmView as PasswordResetConfirmViewForm,
    PasswordResetCompleteView as PasswordResetCompleteViewForm,
    PasswordResetDoneView as PasswordResetDoneViewForm,
    )

from rest_auth.registration.views import RegisterView, VerifyEmailView
# from rest_auth.views import (
#     LoginView, LogoutView, UserDetailsView, PasswordChangeView,
#     PasswordResetView, PasswordResetConfirmView
# )
from django.views.generic import TemplateView
from django.views.generic import TemplateView as templat_view
from browserapi.restauth import ( 
    RegisterView, VerifyEmailView,
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView,
)

# from django_currentuser.middleware import (
#     get_user,
#     )

# if get_user:
#     print('bookmain urls get_current_user', get_user)
#     print('bookmain urls  get_current_user()', get_user)
# else:
#     pass

rest_auth_urls = [
    # URLs that do not require a session or valid token
    url(r'^password/reset/$', PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^password/change/$', PasswordChangeView.as_view()),
] 
rest_auth_registration = [
    url(r'^$', RegisterView.as_view(), name='rest_register'),
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),

    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # django-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
]

# from accounts.api.views import AccountViewSet, UserDetailViewSet, UserViewSet
# from booksmart.api.views import BookViewSet, AuthorViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'books', BookViewSet, 'book')
# router.register(r'authors', AuthorViewSet, 'author')
# router.register(r'accounts', AccountViewSet, 'account')
# router.register(r'users', UserDetailViewSet,'user')
# router.register(r'user', UserViewSet, 'user-account')

# api_patterns = [
#     path('accounts-api/', include('accounts.api.urls', )),
#     path('booksmart-api/', include('booksmart.api.urls', )),
#     ]

accounts_patterns = []

booksmart_patterns = [
    path('accounts-app/', include('accounts.urls', )),
    path('booksmart-app/', include('booksmart.urls',)),
    path('booksearch-app/', include('booksearch.urls',)),   
]

browserapi_patterns = [
    path('', include('browserapi.urls'))
] # , namespace='myapi'

registration_patterns = [
    path('password_change/', PasswordChangeViewForm.as_view(template_name='registrations/password_change.html'), name='password_change_view'),

    path('password_change_done/', PasswordChangeDoneViewForm.as_view(template_name='registrations/password_change_done.html'), name='password_change_done'),

    path('password_reset_form/', PasswordResetViewForm.as_view(
        template_name='registrations/password_reset_form.html'), name='password_reset'),
    # , from_email="booksmart358@gmail.com"
    
    path('password_reset_done/', PasswordResetDoneViewForm.as_view(template_name='registrations/password_reset_done.html'),
        name='password_reset_done'),

    # path('password_reset_confirmation/<uidb64>/<token>/', PasswordResetConfirmViewForm.as_view(), name='password_reset_confirm'),
    path('password_reset_confirmation/<str:uidb64>/<str:token>/', PasswordResetConfirmViewForm.as_view(), name='password_reset_confirm'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmViewForm.as_view(), name='password_reset_confirm'),

    # path('password_reset/', PasswordResetViewForm.as_view(), name='password_reset'),

    path('password_reset_complete/', PasswordResetCompleteViewForm.as_view(template_name='registrations/password_reset_complete.html'), name='password_reset_complete'),
]

# registration_patterns = [
#     path('password_change/', auth_views.PasswordChangeViewForm.as_view(template_name='registrations/password_change.html'), name='password_change_view'),

#     path('password_change_done/', auth_views.PasswordChangeDoneViewForm.as_view(template_name='registrations/password_change_done.html'), name='password_change_done'),

#     path('password_reset_form/', auth_views.PasswordResetViewForm.as_view(template_name='registrations/password_reset_form.html'), name='password_reset'),

#     path('password_reset_form/', auth_views.PasswordResetViewForm.as_view(template_name='registrations/password_reset_form.html'), name='password_reset'),

#     path('password_reset_done/', auth_views.PasswordResetDoneViewForm.as_view(template_name='registrations/password_reset_done.html'),
#         name='password_reset_done'),

#     # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmViewForm.as_view(), name='password_reset_confirm'),

#     path('password_reset/', auth_views.PasswordResetViewForm.as_view(), name='password_reset'),

#     path('password_reset_complete/', auth_views.PasswordResetCompleteViewForm.as_view(template_name='registrations/password_reset_complete.html'), name='password_reset_complete'),
# ]

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
API_TITLE = 'Pastebin API'
API_DESCRIPTION = 'A Web API for creating and viewing code.'
schema_view = get_schema_view(title=API_TITLE)

# app_name = 'records'

urlpatterns = [
#path('background_film', templat_view, name='background'),
path('admin/', admin.site.urls),
# path('api/', include(browserapi_patterns, namespace='myapi'),),
path('api/', include(browserapi_patterns),),
# path('booksmartapi/', include(router.urls)),
# include((pattern_list, app_namespace), namespace=None)

path('booksmartapp/', index_home, name="index"),

# path('booksmartapp-n/', index_home_not, name="index_not"),
# path('booksmartapp/ajax_info_1/', ajax_info_1, name="ajax_info_1"),
path('booksmartapp/booksmart-app/', index_home, name="index-booksmart"),
path('booksmartapp/booksearch-app/', index_home, name="index-booksearch"),
path('booksmartapp/accounts-app/', index_home, name="index-accounts"),
path('', RedirectView.as_view(url='booksmartapp/')),
path('booksmartapp/', include(booksmart_patterns)),
path('registrations/', include(registration_patterns)),

path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # namespace='rest_framework'
path('rest-auth/', include('rest_auth.urls')),
path('rest-auth/registration/', include('rest_auth.registration.urls'), ),

# path('rest-auth/', include(rest_auth)),
# path('rest-auth/registration/', include(rest_auth_registration)),

path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

path('schema/', schema_view),
path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),

]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
# url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()

from mainsite import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

handler404 = 'mainsite.views.custom_page_not_found_view'
handler500 = 'mainsite.views.custom_error_view'
handler403 = 'mainsite.views.custom_permission_denied_view'
handler400 = 'mainsite.views.custom_bad_request_view'

