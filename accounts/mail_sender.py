from accounts.models import Account, MyAccountManager
import os, requests, json, re, datetime, requests.api
from booksmart.models import context_bm, url_img, Book, Author
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage, get_connection, send_mass_mail, EmailMultiAlternatives
from booksmart.models import context_bm, url_img, Book, Author

import smtplib
import ssl
from django.conf import settings


def mail_sender_modal(request):
    context = {}
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server
    
    # email_to = "p.uryga@gmail.com"
    pswd = "ikzliaiijzdvbqlq"
    books = Book.objects.all()
    message_content = {}
    # from_email = "booksmartapp358@gmail.com"
    message_content['from_email'] = "booksmartapp358@gmail.com"
    message_content['my_email'] = "kreative358@gmail.com"
    # simple_email_context = ssl.create_default_context()

    html_message = '<div class="mail_footer"><p style="color: darkblue; font-size: 16px; font-weight: bold; margin-bottom: 4px;">mail from TEAM</p><p style="margin-top: 0px;"><a href="https://booksmart-app-bd32a8932ff0.herokuapp.com/booksmartapp/" target="_blank" style="margin-bottom: 20px; font-size: 16px; font-weight: bold; text-decoration: underline; text-decoration-thickness: 2px;">BOOKSMARTAPP</a></p><p style="font-size: 14px; color: darkblue; margin-bottom: 0px;">If you want to contact about a serious job offer, </p><p style="font-size: 14px; color: darkblue; margin-top: 0px;">you can send me an e-mail e.g. via this box.</p></div>'

    if request.method == "POST":
        from mainsite.views import index_home
        if index_home.recaptcha_token != "":
            print("index_home.recaptcha_token =", index_home.recaptcha_token[:20])
            if request.POST.get('email-sender', False):
                message_content['email_sender'] = request.POST['email-sender']
                print("message_content['email_sender']: ",message_content['email_sender'])
            if request.POST.get('email-subject', False):
                message_content['email_subject'] = request.POST['email-subject']
                print("message_content['email_subject']: ", message_content['email_subject'])
            if request.POST.get('email-text', False): 
                message_content['email_text'] = request.POST['email-text']
                print("message_content['email_text']: ", message_content['email_text'])
                
                
                # for book in books:
                #     message_text += f'\n\r"{book.title}" - {book.author}' 
                # print("message_text:", message_text)
            # try:
            #     send_mail(
            #         subject = message_content['email_subject'],
            #         message = message_content['email_text'],
            #         from_email = message_content['from_email'],
            #         recipient_list = [message_content['my_email'], message_content['email_sender']],
            #         fail_silently=False
            #     )
            #     # print(f"Email successfully sent to - {email_to}")
            # except Exception as e:
            #     print("1. ", e)
            message_text = message_content['email_text']
            try:
                message1 = send_mail(
                    subject = message_content['email_subject'],   
                    message = f"{message_text}\nfrom: {message_content['email_sender']}",         
                    from_email = message_content['from_email'],
                    recipient_list = [message_content['my_email']],
                    fail_silently=False,      
                )

                message2 = send_mail(
                    subject = message_content['email_subject'],   
                    message = message_text,         
                    from_email = message_content['from_email'],
                    recipient_list = [message_content['email_sender']],
                    fail_silently=False,
                    html_message = f"{message_text}\n{html_message}",
                )
            except Exception as e:
                print("1. ", e)
        
        else:
            messages.info(request, "reCAPTCHA doesn't match")
            return redirect("index")
    
    # return render(request, 'mail_sender_modal.html')
    return render(request, 'mail_sender_modal.html', context)

def mail_sender_site(request):
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server
    
    # email_to = "p.uryga@gmail.com"
    pswd = "ikzliaiijzdvbqlq"
    books = Book.objects.all()
    message_content = {}
    # from_email = "booksmartapp358@gmail.com"
    message_content['from_email'] = "booksmartapp358@gmail.com"
    message_content['my_email'] = "kreative358@gmail.com"
    # simple_email_context = ssl.create_default_context()

    html_message = '<div class="mail_footer"><p style="color: darkblue; font-size: 16px; font-weight: bold; margin-bottom: 4px;">mail from TEAM</p><p style="margin-top: 0px;"><a href="https://booksmart-app-bd32a8932ff0.herokuapp.com/booksmartapp/" target="_blank" style="margin-bottom: 20px; font-size: 16px; font-weight: bold; text-decoration: underline; text-decoration-thickness: 2px;" >BOOKSMARTAPP</a></p><p style="font-size: 14px; color: darkblue; margin-bottom: 0px;">If you want to contact about a serious job offer, </p><p style="font-size: 14px; color: darkblue; margin-top: 0px;">you can send me an e-mail e.g. via this box.</p></div>'


    if request.method == "POST":
    
        if request.POST.get('email-sender', False):
            message_content['email_sender'] = request.POST['email-sender']
            print("message_content['email_sender']: ",message_content['email_sender'])
        if request.POST.get('email-subject', False):
            message_content['email_subject'] = request.POST['email-subject']
            print("message_content['email_subject']: ", message_content['email_subject'])
        if request.POST.get('email-text', False): 
            message_content['email_text'] = request.POST['email-text']
            print("message_content['email_text']: ", message_content['email_text'])

        message_text = message_content['email_text']
        try:
            message1 = send_mail(
                subject = message_content['email_subject'],   
                message = f"{message_text}\nfrom: {message_content['email_sender']}",         
                from_email = message_content['from_email'],
                recipient_list = [message_content['my_email']],
                fail_silently=False,      
            )

            message2 = send_mail(
                subject = message_content['email_subject'],   
                message = message_text,         
                from_email = message_content['from_email'],
                recipient_list = [message_content['email_sender']],
                fail_silently=False,
                html_message = f"{message_text}\n{html_message}",
            )
            # send_mass_mail((message1, message2), fail_silently=False)
            # print(f"Email successfully sent to - {email_to}")
        except Exception as e:
            print("1. ", e)


    return render(request, 'mail_sender_site.html')


# https://blog.miguelgrinberg.com/post/the-new-way-to-generate-secure-tokens-in-python
# import secrets
# secrets.token_hex()
# secrets.token_urlsafe()

# def mail_sender_form_1(request):
#     # send_mail(
#     #     "They visited our site",
#     #     "They clicked on link",
#     #     "booksmartapp358@gmail.com",
#     #     ["valow25984@chambile.com"],
#     #     fail_silently=False
#     # )
#     if request.method == "POST":
#         if request.POST.get('user-email', False):
#             email_from = settings.EMAIL_HOST_USER
#             email_to = request.POST['user-email']
#             subject = "They visited our site",
#             message_text = "User send email address: " + email_to
#             books = Book.objects.all()
#             for book in books:
#                 message_text += f'\n\r"{book.title}" - {book.author}' 
#             # print("message_text:", message_text)
#             send_mail(
#                 subject,
#                 message_text,
#                 email_from,
#                 [email_to],
#                 fail_silently=False
#             )

    #         return HttpResponse("Mail with email address was sended")
    # return render(request, 'mail_sender_1.html')

def mail_sender_form_1(request):
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server
    
    # email_to = "p.uryga@gmail.com"
    pswd = "ikzliaiijzdvbqlq"
    books = Book.objects.all()
    message_content = {}
    # from_email = "booksmartapp358@gmail.com"
    message_content['from_email'] = "booksmartapp358@gmail.com"
    message_content['my_email'] = "kreative358@gmail.com"
    # simple_email_context = ssl.create_default_context()
    if request.method == "POST":
    
        if request.POST.get('email-sender', False):
            message_content['email_sender'] = request.POST['email-sender']
            print("message_content['email_sender']: ",message_content['email_sender'])
        if request.POST.get('email-subject', False):
            message_content['email_subject'] = request.POST['email-subject']
            print("message_content['email_subject']: ", message_content['email_subject'])
        if request.POST.get('email-text', False): 
            message_content['email_text'] = request.POST['email-text']
            print("message_content['email_text']: ", message_content['email_text'])
            
            
            # for book in books:
            #     message_text += f'\n\r"{book.title}" - {book.author}' 
            # print("message_text:", message_text)
        try:
            send_mail(
                subject = message_content['email_subject'],
                message = message_content['email_text'],
                from_email = message_content['from_email'],
                recipient_list = [message_content['my_email'], message_content['email_sender']],
                fail_silently=False
            )
            # print(f"Email successfully sent to - {email_to}")
        except Exception as e:
            print("1. ", e)

    return render(request, 'mail_sender_1.html')

def mail_sender_form_2(request):
    # smtp_port = 587                 # Standard secure SMTP port
    # smtp_server = "smtp.gmail.com"  # Google SMTP Server
    # from_email = "booksmartapp358@gmail.com"
    # # email_to = "p.uryga@gmail.com"
    # pswd = "ikzliaiijzdvbqlq"
    books = Book.objects.all()
    subject = "2. Message"
    from_email = "booksmartapp358@gmail.com"
    bcc = ["booksmartapp358@gmail.com"]
    reply_to = ["booksmartapp358@gmail.com"]
    # simple_email_context = ssl.create_default_context()
    if request.method == "POST":
        if request.POST.get('user-email', False):
            # email_from = "booksmartapp358@gmail.com"
            to = request.POST['user-email']

            body = f"User send email address: {to}"
            books = Book.objects.all()
            # for book in books:
            #     message_text += f'\n\r"{book.title}" - {book.author}' 
            # print("message_text:", message_text)
            
            try:
                print(f"2. Sending email to - {to}")
            # finally:
            #     TIE_server.quit()
                
                
                email = EmailMessage(
                    subject,
                    body,
                    from_email,
                    [to],
                    bcc,
                    reply_to
                    )
                email.send()
            except Exception as e:
                print("2. ", e)   

            return HttpResponse("Mail with email address was sended")
    return render(request, 'mail_sender_2.html')

def mail_sender_form_3(request):
    
    books = Book.objects.all()
    subject = "3. Message"
    from_email = "booksmartapp358@gmail.com"
    bcc = ["booksmartapp358@gmail.com"]
    reply_to = ["booksmartapp358@gmail.com"]
    if request.method == "POST":
        if request.POST.get('user-email', False):
            # email_from = "booksmartapp358@gmail.com"
            to = request.POST['user-email']
            body = f"User send email address: {to}"
            try:
                print(f"3. Sending email to - {to}")
                email_1 = EmailMessage(
                    subject,
                    body,
                    from_email,
                    [to],
                    bcc,
                    reply_to,
                    )
                email_2 = EmailMessage(
                    subject,
                    body,
                    from_email,
                    [to],
                    bcc,
                    reply_to,
                    )

                with get_connection() as connection:
                    connection.send_messages([email_1, email_2])
            except Exception as e:
                print("3. ", e)   

            return HttpResponse("Mail with email address was sended")
    return render(request, 'mail_sender_3.html')

# def sendmail(from_addr: str, to_addrs: Union[str, Sequence[str]], msg: Union[bytes, str], mail_options: Sequence[str]=..., rcpt_options: List[str]=...) -> _SendErrs
# This command performs an entire mail transaction.

# The arguments are:
#     - from_addr    : The address sending this mail.
#     - to_addrs     : A list of addresses to send this mail to.  A bare
#                      string will be treated as a list with 1 address.
#     - msg          : The message to send.
#     - mail_options : List of ESMTP options (such as 8bitmime) for the
#                      mail command.
#     - rcpt_options : List of ESMTP options (such as DSN commands) for
#                      all the rcpt commands.

# msg may be a string containing characters in the ASCII range, or a byte
# string.  A string is encoded to bytes using the ascii codec, and lone
# \r and \n characters are converted to \r\n characters.

# If there has been no previous EHLO or HELO command this session, this
# method tries ESMTP EHLO first.  If the server does ESMTP, message size
# and each of the specified options will be passed to it.  If EHLO
# fails, HELO will be tried and ESMTP options suppressed.

# This method will return normally if the mail is accepted for at least
# one recipient.  It returns a dictionary, with one entry for each
# recipient that was refused.  Each entry contains a tuple of the SMTP
# error code and the accompanying error message sent by the server.

# This method may raise the following exceptions:

#  SMTPHeloError          The server didn't reply properly to
#                         the helo greeting.
#  SMTPRecipientsRefused  The server rejected ALL recipients
#                         (no mail was sent).
#  SMTPSenderRefused      The server didn't accept the from_addr.
#  SMTPDataError          The server replied with an unexpected
#                         error code (other than a refusal of
#                         a recipient).
#  SMTPNotSupportedError  The mail_options parameter includes 'SMTPUTF8'
#                         but the SMTPUTF8 extension is not supported by
#                         the server.

# Note: the connection will be open even after an exception is raised.

# Example:

#  >>> import smtplib
#  >>> s=smtplib.SMTP("localhost")
#  >>> tolist=["one@one.org","two@two.org","three@three.org","four@four.org"]
#  >>> msg = '''\
#  ... From: Me@my.org
#  ... Subject: testin'...
#  ...
#  ... This is a test '''
#  >>> s.sendmail("me@my.org",tolist,msg)
#  { "three@three.org" : ( 550 ,"User unknown" ) }
#  >>> s.quit()

# In the above example, the message was accepted for delivery to three
# of the four addresses, and one was rejected, with the error code
# 550.  If all addresses are accepted, then the method will return an
# empty dictionary.
# Full name: smtplib.SMTP.sendmail

# ★ API Usage Examples for: smtplib.SMTP.sendmail()

#  See Real World Examples From GitHub

# Thoughts? 😀 Take a Survey!

