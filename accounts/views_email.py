from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from accounts.tokens import account_activation_token

def activateAccount(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print('uid:', uid)
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        print('user:', user)

        # messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        email_msessage_success = messages.success(request, "Thank you for your email confirmation. Now you can login your account.")

        return email_msessage_success
        # return redirect('login')
    else:
        
        email_msessage_error = messages.error(request, "Activation link is invalid!")
        return email_msessage_error
    # return redirect('homepage')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print('activateEmail:', message)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        activate_email_message_send = messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
        return activate_email_message_send
    else:
        activate_email_message_send_not = messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
        return activate_email_message_send_not