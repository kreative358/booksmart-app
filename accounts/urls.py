from django.urls import path, include
from django.conf.urls import url
from django.conf.urls import include as urlinclude
from rest_auth.views import LogoutView

# from django.contrib.auth import views as auth_views 
from accounts.api.views import (
    RegistrationAPIView, 
    LoginAPIView,
     AccountUpdateAPIView, 
     logout_api, 
     example_apiview,
)

from accounts.views import(
    logout_user,
    index_auth,
    # CustomAuthToken,
    LoginView,
    AccauntUpdateView,
    RegistrationViewBase,
    PasswordUpdateView,
    PasswordUpdateViewApi,
    
    SendEmailConfirmationTokenAPIView, 
    UserInformationAPIVIew,
    confirm_email_view
    )

from accounts.views_forms import (
    register_view_form, ## usunąć
    account_view_form,
)

from accounts.password import (
    PasswordChangeView, 
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
)

app_name = 'accounts'

password_patterns = [
    path('password_change/', PasswordChangeView.as_view(template_name='registrations/password_change.html'), name='password_change'),

    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='registrations/password_change_done.html'), name='password_change_done'),

    path('password_reset_form/', PasswordResetView.as_view(template_name='registrations/password_reset_form.html'), name='password_reset_form'),

    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='registrations/password_reset_done.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset_reset_complete/', PasswordResetCompleteView.as_view(template_name='registrations/password_reset_complete.html'), name='password_reset_complete'),
]



# accounts_patterns = [
#     path('register_view/', RegistrationAPIView.as_view(), name='register-view'),
#     path('login_view/', LoginAPIView.as_view(), name="login-view"),
#     path('account_view/', AccountUpdateAPIView.as_view(), name="account-view"),
#     path('logout_view/', logout_api, name="logout-view"),
# ]

urlpatterns = [
    
    # path('', index_auth, name='index_auth'),
    # path('register_post/', RegisterPostView.as_view(), name='register_post'),

    # path('', include(accounts_patterns)),
    path('register_view/', RegistrationAPIView.as_view(), name='register-view'),
    path('login_view/', LoginAPIView.as_view(), name="login-view"),
    path('account_view/', AccountUpdateAPIView.as_view(), name="account-view"),
    # path('logout_view/', LogoutView.as_view(), name="logout-view"),
    path('logout_view/', logout_api, name="logout-view"),
    path('password/', include(password_patterns)),

    path('register/', RegistrationViewBase.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('account/', AccauntUpdateView.as_view(), name="account"),
    path('logout/', logout_user, name="logout"),
    path('password-update/', PasswordUpdateView.as_view(), name="password-update"),
    path('password-update-api/', PasswordUpdateViewApi.as_view(), name="password-update-api"),

    # path('register/', registration_view_base, name='register'),
    #path('login_token', ObtainAuthTokenView.as_view(), name="login"),
    #path('login', CustomAuthToken.as_view(), name="login"),

    path('register_form/', register_view_form, name="register_form"),
    
    path('account_update/', account_view_form, name="account_update"),

    path('user_info/', UserInformationAPIVIew.as_view(), name='user_information_api_view'),
    path('send-confirmation-email/', SendEmailConfirmationTokenAPIView.as_view(), name='send_email_confirmation_api_view'),
    path('confirm-email/', confirm_email_view, name='confirm_email_view'),
    # path('account_update/', UpdateProfileView.as_view(), name="account_update"),
    
    # path('password_change/', PasswordChangeView.as_view(template_name='registrations/password_change.html'), name='password_change'),

    # path('password_change_done/', PasswordChangeDoneView.as_view(template_name='registrations/password_change_done.html'), 
    # name='password_change_done'),

    # path('password_reset_form/', PasswordResetView.as_view(template_name='registrations/password_reset_form.html'), name='password_reset_form'),

    # path('password_reset_done/', PasswordResetDoneView.as_view(template_name='registrations/password_reset_done.html'),
    # name='password_reset_done'),

    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # path('reset_reset_complete/', PasswordResetCompleteView.as_view(template_name='registrations/password_reset_complete.html'),
    # name='password_reset_complete'),

    # path('api-auth/', include('rest_framework.urls')),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# 	path('properties', account_properties_view, name="properties"),
# 	path('properties/update', update_account_view, name="update"),
# 	path('login', ObtainAuthTokenView.as_view(), name="login"), # -> see accounts/api/views.py for response and url info
# 	path('register', registration_view, name="register"),
# ]
