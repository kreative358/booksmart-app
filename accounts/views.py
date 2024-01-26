import os, requests, json, re
# from booksmart.models import context_bm as context_bm_rest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
# from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer, HTMLFormRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework import permissions
from accounts.serializers import RegistrationSerializer, AccountUpdateSerializer, LoginSerializer, PasswordUpdateSerializer, PasswordUpdateSerializerApi #, ReCaptchaSerializer

from rest_framework.generics import GenericAPIView, CreateAPIView
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_auth.app_settings import (
    TokenSerializer,
    )
from rest_framework.fields import Field
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from accounts.error import *
from django.contrib.auth.hashers import make_password
from accounts.forms import RechaptchaForm
from booksmart.models import url_img, url_img_author, Book, Author, BackgroundPoster, BackgroundVideo, BackgroundMusic #, context_bm_m

RECAPTCHA_SECRET_KEY = '6Le3IP4nAAAAAH5J3uPYy4BPPEsS55k0RwCaYxeY'
url_recaptcha = 'https://www.google.com/recaptcha/api/siteverify'


context_main = {}
context_bm_rest = {}
# try:
#     if Book.objects.all():
#     # if Book.objects.filter().all():
#         all_books = Book.objects.all()
#         # context_list.append(all_books)
#         num_books = Book.objects.all().count()
#         context_main['allbooks'] = all_books
#         context_main['num_books'] = num_books
#     elif not Book.objects.all():
#     # elif not Book.objects.filter().all():
#         context_main['allbooks'] = None
#         context_main['num_books'] = 0
# except Exception as err:
#     print(f"accounts views: Book.objects.all() except Exception as {err}")
#     pass

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
except Exception as err:
    print(f"accounts views: Author.objects.all(): except Exception as {err}")
    pass

try:
    if BackgroundPoster.objects.filter().last():
        poster = BackgroundPoster.objects.filter().last()
        context_main['poster_url_1'] = poster.link_poster_1
        context_main['poster_url_2'] = poster.link_poster_2
    elif not BackgroundPoster.objects.filter().last():
        context_main['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
        context_main['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
except Exception as err:
    print(f"accounts views: Author.objects.all(): except Exception as {err}")
    pass

try:
    if BackgroundVideo.objects.filter().last():   
        video = BackgroundVideo.objects.filter().last()
        context_main['video_url'] = video.link_video
        context_main['video_type'] = video.type_video
    elif not BackgroundVideo.objects.filter().last():
        context_main['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
        context_main['video_type'] = "mp4"
except Exception as err:
    print(f"accounts views: BackgroundVideo.objects.filter().last(): except Exception as {err}")
    pass

try:
    if BackgroundMusic.objects.filter().last():   
        music = BackgroundMusic.objects.filter().last()
        context_main['music_url_1'] = music.link_music_1
        context_main['music_type_1'] = music.type_music_1
        context_main['music_url_2'] = music.link_music_2
        context_main['music_type_2'] = music.type_music_2
    elif not BackgroundMusic.objects.filter().last(): 
        context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_main['music_type_1'] = "mp3"
        context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_main['music_type_2'] = "mp3"
except Exception as err:
    print(f"accounts views: BackgroundMusic.objects.filter().last(): except Exception as {err}")
    context_main['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
    context_main['music_type_1'] = "mp3"
    context_main['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
    context_main['music_type_2'] = "mp3"
    
try:
    if Book.objects.all():
        context_serializer_start = {'num_authors': context_bm_rest['num_authors'], 'poster_url_1': context_bm_rest['poster_url_1'], 'poster_url_2': context_bm_rest['poster_url_2'], 'video_url': context_bm_rest['video_url'], 'video_type': context_bm_rest['video_type'], 'music_url_1': context_bm_rest['music_url_1'], 'music_type_1': context_bm_rest['music_type_1'], 'music_url_2': context_bm_rest['music_url_2'], 'music_type_2': context_bm_rest['music_type_2']}
    else:
        print("No Books")
except Exception as err:
    print(f"accounts views Exception as {err}")    
    
# def get_user(request):
#     r_user=request.user
#     if r_user.is_authenicated:
#         get_id = {}
#         # print('accounts views user.id:', r_user.id)
#         get_id['user_id'] = r_user.id
#         # print("accounts views get_id['user_id']", get_id['user_id'])
#         userid = get_id['user_id']
#         # print('accounts views userid', userid)
#         return userid
#     else:
#         print('accounts views None')
#         return None


@api_view(['GET', ])
@permission_classes([AllowAny,])
# @authentication_classes([])
@renderer_classes([TemplateHTMLRenderer])
def index_auth(request):
    context_i_a = context_bm_rest
	# return render(request, 'must_authenticate.html', {})
    return Response(context_i_a, template_name='index_auth.html', )

context_serializer_start = {}
    

# from typing import Protocol
# from django.contrib.auth.decorators import login_required
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.core.mail import EmailMessage
# from .tokens import account_activation_token

# def activate(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()

#         messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
#         return redirect('login')
#     else:
#         messages.error(request, "Activation link is invalid!")

#     return redirect('homepage')

# def activateEmail(request, user, to_email):
#     mail_subject = "Activate your user account."
#     message = render_to_string("template_activate_account.html", {
#         'user': user.username,
#         'domain': get_current_site(request).domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#         "protocol": 'https' if request.is_secure() else 'http'
#     })
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     if email.send():
#         messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
#                 received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
#     else:
#         messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


class RegistrationViewBase(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    renderer_classes = [TemplateHTMLRenderer, HTMLFormRenderer]
    permission_classes = [AllowAny,]
    template_name="register.html"
    ser_val = {}
    style = {'template_pack': 'rest_framework/vertical/'} #
    serializer_class = RegistrationSerializer

    try:
        context_serializer = {'num_authors': context_bm_rest['num_authors'], 'poster_url_1': context_bm_rest['poster_url_1'], 'poster_url_2': context_bm_rest['poster_url_2'], 'video_url': context_bm_rest['video_url'], 'video_type': context_bm_rest['video_type'], 'music_url_1': context_bm_rest['music_url_1'], 'music_type_1': context_bm_rest['music_type_1'], 'music_url_2': context_bm_rest['music_url_2'], 'music_type_2': context_bm_rest['music_type_2']}
    except Exception as e:
        print(f"210. RegistrationViewBase Exception as {e}")        
        context_serializer = {}
        
    def get(self, request, *args, **kwargs):
        message_errors = ""
        context_serializer_get = {}
        context_serializer_get.update(context_main)
        #current_url_name = request.path
        # messages.info(request, "")
        # print("context_bm_rest = ", context_bm_rest)
        serializer = self.serializer_class()

        context_serializer_get = self.context_serializer
        context_serializer_get['serializer']= serializer 
        context_serializer_get['style'] = self.style 

        return Response(context_serializer_get, )

    def post(self, request, *args, **kwargs):
        # message_errors = ""
        message_errors = []
        recaptcha_error = []

        context_serializer_post = {}
        context_serializer_post = self.context_serializer
        context_serializer_post['style'] = self.style
        # messages.info(request, "")
        # datas = request.data.copy()
        
        serializer = self.serializer_class(data=request.data)
        # serializer = self.serializer_class(data=request.data, context={'request': request})
        # print('request data:',request.data)
        # initial_val = request.data
        # initials['current_url'] = initial_val['current_url']
        initial_val = serializer.initial_data

        username_val = initial_val['username']
        email_val = initial_val['email']
        pass1_val = initial_val['password']
        pass2_val = initial_val['password2']
        oldpass_val = 'no_oldpass'
        current_url_val = initial_val['current_url']

        # recaptcha_val = initial_val['g-recaptcha-response']
        if initial_val['g-recaptcha-response']:
            recaptcha_val = initial_val['g-recaptcha-response']
        else:
            recaptcha_val = initial_val['recaptcha_token']

        context_serializer_post['user_name'] = username_val
        context_serializer_post['e_mail'] = email_val
        context_serializer_post['pass1'] = pass1_val
        context_serializer_post['pass2'] = pass2_val
        context_serializer_post['oldpass'] = oldpass_val

        context_serializer_post['current_url'] = current_url_val
        # https://stackoverflow.com/questions/36414804/integrate-django-password-validators-with-django-rest-framework-validate-passwor
        # https://medium.com/django-rest/django-rest-framework-login-and-register-user-fd91cf6029d5
        # https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
        # https://www.django-rest-framework.org/api-guide/serializers/#accessing-the-initial-data-and-instance
        params = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_val
        }
        verify_rs = requests.get(url_recaptcha, params=params, verify=True)
        # result = json.load(response)
        result = verify_rs.json()
        print('result =', result)
        # context['mail_sender'] = "ready"
        if result['success'] == True:
        
        # if len(recaptcha_val) > 500 and len(recaptcha_token_val) > 500 and recaptcha_val == recaptcha_token_val:
            if serializer.is_valid():
                # serializer = serializer.data
                password = serializer.validated_data.get('password')
                serializer.validated_data['password'] = make_password(password)

                account = serializer.save()
                # print("serializer.data", serializer.data)
                # print('account:', account)

                if account:
                    login(request, account)
                    try:
                        token = Token.objects.get(user=account)
                    except Token.DoesNotExist:
                        token = Token.objects.create(user=account)

                    if token:
                        # print('token.key', token.key)
                        pass
                    else:
                        # print('no token')
                        pass

                    
                    # if initial_val['current_url']!= "":
                    msgs = ['INFORMATION:', 'Account created successfully']
                    
                    if context_serializer_post['current_url'] != "":
                        messages.info(request, "<br>".join(msg for msg in msgs))
                        return redirect(context_serializer_post['current_url'])

                    else:
                        messages.info(request, "<br>".join(msg for msg in msgs))
                        return redirect("index")

            else:
                # messages.info(request, "")
                errs = serializer.errors
                # message_errors = serializer_errors(errs) +  ["<p style='font-weight: bold'>You try register with:</p>", f"<p>username: {username_val},<br>email: {email_val}</p>"]
                message_errors = serializer_errors(errs) +  ["<p class='class_text_info' style='font-weight: bold; margin-bottom: -16px; color: red'>You try register with:</p>", f"<p style='margin-bottom: 0px;'>username: {username_val}</p><p>email: {email_val}</p>"]
                # print('accounts views RegistrationViewBase m_errs:', message_errors)
                # print('accounts views RegistrationViewBase s_errs:', serializer.errors)
                # print('register message_errors:', message_errors)
                # if initial_val['current_url']!= "":
                if context_serializer_post['current_url'] != "":
                    messages.info(request, ''.join(msg_error for msg_error in message_errors))
                    return redirect(context_serializer_post['current_url'])

                else:
                    context_serializer_post_else = {}
                    messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
                    # return messages_info
                    
                    context_serializer_post_else = context_serializer_post
                    context_serializer_post_else['serializer'] = self.serializer_class
                    context_serializer_post_else['errors'] = message_errors
                    
                    return Response(context_serializer_post_else , )

        elif result['success'] != True:
            if context_serializer_post['current_url'] != "":
                messages.info(request, 'reCaptcha seems to be NOT ORIGINAL')
                return redirect(context_serializer_post['current_url'])
                    
            else:
                context_serializer_post_else = {}
                recaptcha_error = ['reCaptcha seems to be NOT ORIGINAL']
                messages.info(request, recaptcha_error)

                context_serializer_post_else = context_serializer_post
                context_serializer_post_else['serializer'] = self.serializer_class
                context_serializer_post_else['errors'] = recaptcha_error
                
                return Response(context_serializer_post_else, template_name="login.html")
        
        context_serializer_Response =  {}
        # context_serializer_Response = context_serializer_post
        context_serializer_Response = self.context_serializer
        context_serializer_Response['style'] = self.style
        context_serializer_Response['serializer'] = self.serializer_class
        # context_Response_return['serializer'] = serializer

        # return Response({'serializer':serializer, 'style': self.style},)
        return Response(context_serializer_Response, )
        # return Response(None, status=status.HTTP_202_ACCEPTED)


# class LoginView(APIView):
class LoginView(GenericAPIView):
    # This view should be accessible also for unauthenticated users.
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer, HTMLFormRenderer]
    permission_classes = [AllowAny,]
    template_name = "login.html"
    style = {'template_pack': 'rest_framework/vertical/'}
    serializer_class = LoginSerializer
    context_serializer = context_serializer_start

    def get(self, request, *args, **kwargs):
        message_errors = []
        recaptcha_error = []
        context_serializer_get = {}
        context_serializer_get.update(context_main)
        #current_url_name = request.path
        # messages.info(request, "")
        # print("context_bm_rest = ", context_bm_rest)
        serializer = self.serializer_class()

        context_serializer_get = self.context_serializer
        context_serializer_get['serializer'] = serializer 
        context_serializer_get['style'] = self.style 

        return Response(context_serializer_get, )

    def post(self, request, *args, **kwargs):
        # message_errors = ""
        message_errors = []
        recaptcha_error = []
        
        context_serializer_post = {}
        context_serializer_post = self.context_serializer
        context_serializer_post['style'] = self.style
        # messages.info(request, "")
        # recaptcha_login = ""
        # print('request', request)
        # data_recaptcha = json.loads(request.body.decode("utf-8"))
        serializer = self.serializer_class(data=request.data, context={'request': request})

        initial_val = serializer.initial_data
        # print('initial_val =', initial_val)
        username_val = initial_val['username']
        pass_val = initial_val['password']
        email_val = 'no_email'
        current_url_val = initial_val['current_url']

        # recaptcha_val = initial_val['g-recaptcha-response']
        if initial_val['g-recaptcha-response']:
            recaptcha_val = initial_val['g-recaptcha-response']
        else:
            recaptcha_val = initial_val['recaptcha_token']

        # print(f'len(recaptcha_val) {len(recaptcha_val)}:', recaptcha_val[:20])
        # print(f'len(recaptcha_token_val) {len(recaptcha_token_val)}:', recaptcha_token_val[:20])
        
        context_serializer_post['user_name'] = username_val
        context_serializer_post['pass'] = pass_val
        context_serializer_post['e_mail'] = email_val
        context_serializer_post['current_url'] = current_url_val

        params = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_val
        }
        verify_rs = requests.get(url_recaptcha, params=params, verify=True)
        # result = json.load(response)
        result = verify_rs.json()
        print('result =', result)
        # context['mail_sender'] = "ready"
        if result['success'] == True:
        # recaptcha_token_val = recaptcha_val[:505]
        # if len(recaptcha_val) > 500 and len(recaptcha_token_val) > 500 and recaptcha_val == recaptcha_token_val:
                
            if serializer.is_valid():

                account = serializer.validated_data['user']

                if account:

                    login(request, account)
                    try:
                        token = Token.objects.get(user=account)
                    except Token.DoesNotExist:
                        token = Token.objects.create(user=account)

                    if token:
                        # print('token.key', token.key)
                        pass
                    else:
                        # print('no token')
                        pass

                    # if initial_val['current_url']!= "":
                    if context_serializer_post['current_url'] != "":
                        # print("login initial_val['current_url']:", initial_val['current_url'] )
                        msgs = ['INFORMATION:<br>', 'You logged in successfully']
                        messages.info(request, ''.join(msg for msg in msgs))
                        print("LoginView context_serializer_post['current_url'] =", context_serializer_post['current_url'])
                        return redirect(context_serializer_post['current_url'])
                
                    else:
                        msgs = ['MESSAGE:<br>', 'You logged in successfully']
                        messages.info(request, ''.join(msg for msg in msgs))
                        return redirect("index")

            elif result['success'] != True:
                message_errors = ['INFORMATION:<br>', 'Access denied:<br>', 'wrong username or password.<br>', f"You tried log in with:<br> username: {username_val}<br>password: {pass_val}"]
                # errs = serializer.errors
                # message_errors = serializer_errors(errs)
                if context_serializer_post['current_url'] != "":
                    messages.info(request, ''.join(msg_error for msg_error in message_errors))
                    return redirect(context_serializer_post['current_url'])
                        
                else:
                    context_serializer_post_else = {}
                    # message_errors = ['MESSAGE:<br>', 'Access denied:<br> wrong username or password']
                    messages.info(request, ''.join(msg_error for msg_error in message_errors))
                    context_serializer_post_else = context_serializer_post
                    context_serializer_post_else['serializer'] = self.serializer_class
                    context_serializer_post_else['errors'] = message_errors
                    
                    return Response(context_serializer_post_else, template_name="login.html")
            
        else:
            if context_serializer_post['current_url'] != "":
                messages.info(request, ['reCaptcha seems to be NOT ORIGINAL'])
                return redirect(context_serializer_post['current_url'])
                    
            else:
                context_serializer_post_else = {}
                messages.info(request, ['reCaptcha seems to be NOT ORIGINAL !?!', ])

                context_serializer_post_else = context_serializer_post
                context_serializer_post_else['serializer'] = self.serializer_class
                context_serializer_post_else['errors'] = ['reCaptcha seems to be<br>NOT ORIGINAL !!!',]
                
                return Response(context_serializer_post_else, template_name="login.html")

        context_serializer_Response =  {}
        # context_serializer_Response = context_serializer_post
        context_serializer_Response = self.context_serializer
        context_serializer_Response['style'] = self.style
        context_serializer_Response['serializer'] = self.serializer_class
        # context_Response_return['serializer'] = serializer
        
        return Response(context_serializer_Response,  template_name="login.html")


class AccauntUpdateView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer, HTMLFormRenderer]
    permission_classes = [IsAuthenticated,]
    template_name="account.html"
    ser_val = {}
    style = {'template_pack': 'rest_framework/vertical/'}
    serializer_class = AccountUpdateSerializer
    # style = { 'placeholder': 'field to enter email', 'autofocus': True, 'size':'36', 'id':'bs_input'}
    context_serializer = context_serializer_start

    def get(self, request, *args, **kwargs): #self, request, *args, **kwargs
    # def get(self, request, format=None):   
        # messages.info(request, "") 
        context_serializer_get = {}

        account = request.user
        username_val = account.username
        email_val = account.email

        serializer = self.serializer_class(account)

        context_serializer_get = self.context_serializer
        context_serializer_get['serializer'] = serializer 
        context_serializer_get['style'] = self.style 

        return Response(context_serializer_get,)

    def post(self, request, format=None):
        # messages.info(request, "")
        context_serializer_post = {}
        context_serializer_post = self.context_serializer
        context_serializer_post['style'] = self.style

        account = request.user
        serializer = self.serializer_class(account, data=request.data)
        # serializer = self.serializer_c;ass(account, data=request.data)
        initial_val = serializer.initial_data
        # print('initial_val =', initial_val)
        username_val = initial_val['username']
        email_val = initial_val['email']
        pass1_val = 'no_pass1'
        if initial_val['current_url']:
            current_url_val = initial_val['current_url']
            context_serializer_post['current_url'] = current_url_val
        else:
            context_serializer_post['current_url'] = ""

        context_serializer_post['user_name'] = username_val
        context_serializer_post['pass1'] = pass1_val
        context_serializer_post['e_mail'] = email_val
        

        if serializer.is_valid():
            serializer.save()
            
            if context_serializer_post['current_url'] != "":
                # print("login initial_val['current_url']:", initial_val['current_url'] )
                msgs = ['MESSAGE: <br>', 'Profile details updated success<br>', f"username: {username_val},<br>adress email: {email_val}"]
                messages.info(request, ''.join(msg for msg in msgs))
                # return redirect(f"booksmart:{initial_val['current_url']}")
                return redirect(context_serializer_post['current_url'])
            else:
                context_serializer_post_else = {}
                msgs = ['MESSAGE: <br>', 'Profile details updated success<br>', f"username: {username_val},<br>adress email: {email_val}"]
                messages.info(request, ''.join(msg for msg in msgs))

                context_serializer_post_else = context_serializer_post
                # context_serializer_post_else["serializer"] = serializer
                context_serializer_post_else["serializer"] = self.serializer_class
                context_serializer_post_else['msgs_info'] = msgs

                # return Response({'serializer':serializer, 'user_name': username_val, 'e_mail':email_val, 'pass1':pass1_val, 'msgs_info': msgs, 'style':self.style})
                return Response(context_serializer_post_else,)

        else:
            errs = serializer.errors
            message_errors = serializer_errors(errs)
            # print('register message_errors:', message_errors)

            if context_serializer_post['current_url'] != "":

                messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
                return redirect(context_serializer_post['current_url'])

            else:
                context_serializer_post_else = {}
                messages.info(request, "<br>".join(msg_error for msg_error in message_errors))


                context_serializer_post_else = self.context_serializer
                # context_serializer_post_else['serializer'] = serializer
                context_serializer_post_else['serializer'] = self.serializer_class
                context_serializer_post_else['errors'] = message_errors 

                # return Response({'serializer':serializer, 'errors': message_errors, 'user_name':username_val, 'e_mail': email_val, 'pass1':pass1_val, 'style':self.style},  template_name="account.html")
                return Response(context_serializer_post_else, template_name="account.html")

                # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #return Response(None, status=status.HTTP_202_ACCEPTED)
        context_serializer_Response =  {}
        # context_serializer_Response = context_serializer_post
        context_serializer_Response = self.context_serializer
        context_serializer_Response['style'] = self.style
        context_serializer_Response['serializer'] = self.serializer_class
        # context_Response_return['serializer'] = serializer
        return Response(context_serializer_Response,  template_name="account.html")



@api_view(["GET"])
@permission_classes([AllowAny,])
def logout_user(request):
    messages.info(request, "")
    try:
        # print("request.data:", request.data)
        # print("request.path:", request.path)
        request.user.auth_token.delete()
        logout(request)

        msgs = ['MESSAGE:<br>','Logout successfully, token deleted']
        messages.info(request, ''.join(msg for msg in msgs))

        return redirect('/')
    except:
        # print("request.path:", request.path)
        logout(request)
        msgs = ['INFORMATION:<br>','Logout successfully']
        messages.info(request, ''.join(msg for msg in msgs))
        return redirect('/')

    return Response(None, status=status.HTTP_202_ACCEPTED)

class PasswordUpdateView(APIView):
# class PasswordUpdateView(UpdateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    renderer_classes = [TemplateHTMLRenderer, HTMLFormRenderer]
    permission_classes = [IsAuthenticated,] #IsOwnerOrReadOnly 
    template_name="password-update.html"
    style = {'template_pack': 'rest_framework/vertical/'}
    serializer_class = PasswordUpdateSerializer
    context_serializer = context_serializer_start
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs): #self, request, *args, **kwargs
    # def get(self, request, format=None):   
        context_serializer_get = {}
        # messages.info(request, "") 
        # user = self.request.user  # !!!
        account = request.user
        serializer = self.serializer_class(account)
        context_serializer_get = self.context_serializer
        context_serializer_get['serializer'] = serializer 
        # serializer = self.serializer_class()
        return Response(context_serializer_get, )

    def post(self, request, format=None):
        # messages.info(request, "")
        context_serializer_post = {}
        context_serializer_post = self.context_serializer
        context_serializer_post['style'] = self.style

        account = request.user
        serializer = self.serializer_class(account, data=request.data)
        # serializer = self.serializer_c;ass(account, data=request.data)
        initial_val = serializer.initial_data
        oldpassword_val = initial_val['oldpassword']
        password1_val = initial_val['password1']
        password2_val = initial_val['password2']
        email_val = initial_val['email']
        pass_val = 'no_pass'
        if initial_val['current_url']:
            current_url_val = initial_val['current_url']
            context_serializer_post['current_url'] = current_url_val
        else:
            context_serializer_post['current_url'] = ""

        context_serializer_post['oldpassword'] = oldpassword_val
        context_serializer_post['pass1'] = password1_val
        context_serializer_post['pass2'] = password2_val
        context_serializer_post['e_mail'] = email_val
        context_serializer_post['pass'] = pass_val
        if serializer.is_valid():
            # serializer.save()
            # user = self.get_object()
            account = serializer.save()
            if not account.check_password(serializer.data.get('oldpassword')):
                # errs = serializer.errors
                # message_errors = serializer_errors(errs)
                # print('register message_errors:', message_errors)
                msgs = ['INFORMATION:<br>', 'Wrong current password.<br>', 'It is not:', oldpassword_val]
                messages.info(request, ' '.join(msg for msg in msgs))

                if context_serializer_post['current_url'] != "":
                    messages.info(request, ' '.join(msg for msg in msgs))
                    return redirect(context_serializer_post['current_url'])

                else:
                    context_serializer_post_else = {}
                    messages.info(request, ' '.join(msg for msg in msgs))

                    context_serializer_post_else = context_serializer_post
                    # context_serializer_post_else['serializer'] = serializer
                    context_serializer_post_else['serializer'] = self.serializer_class

                    return Response(context_serializer_post_else,  template_name="password-update.html")

            elif account.check_password(serializer.data.get('oldpassword')):
                # password = password1
                account.set_password(serializer.data.get('password1'))
                account.save()

                login(request, account)

                try:
                    token = Token.objects.get(user=account)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=account)

                if token:
                    # print('token.key', token.key)
                    pass
                else:
                    # print('no token')
                    pass

                msgs = ['INFORMATION: <br>', 'Password details updated success.']
                if context_serializer_post['current_url'] != "":
                    # print("pass update initial_val['current_url']:", initial_val['current_url'] )
                    messages.info(request, ''.join(msg for msg in msgs))
                    # return redirect(f"booksmart:{initial_val['current_url']}")
                    return redirect(context_serializer_post['current_url'])
                # elif initial_val['current_url'] == "":
                else:
                    context_serializer_post_else = {}

                    messages.info(request, ''.join(msg for msg in msgs))

                    context_serializer_post_else = context_serializer_post
                    context_serializer_post_else["serializer"] = serializer
                    # context_serializer_post_else['serializer'] = self.serializer_class
                    context_serializer_post_else['msgs_info'] = msgs 
                    return Response(context_serializer_post_else, )
        else:
            errs = serializer.errors
            message_errors = serializer_errors(errs)
            # print('register message_errors:', message_errors)
            
            if context_serializer_post['current_url'] != "":

                messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
                
                return redirect(context_serializer_post['current_url'])

            else:
                context_serializer_post_else = {}

                messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
                
                context_serializer_post_else = context_serializer_post
                # context_serializer_post_else['serializer'] = serializer
                context_serializer_post_else['serializer'] = self.serializr_class

                return Response(context_serializer_post_else,  template_name="password-update.html")

        context_serializer_Response =  {}
        # context_serializer_Response = context_serializer_post
        context_serializer_Response = self.context_serializer
        context_serializer_Response['style'] = self.style
        context_serializer_Response['serializer'] = self.serializer_class
        # context_Response_return['serializer'] = serializer
        return Response(context_serializer_Response, )

class PasswordUpdateViewApi(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    renderer_classes = [TemplateHTMLRenderer, HTMLFormRenderer]
    permission_classes = [IsAuthenticated,] #IsOwnerOrReadOnly 
    template_name="password-update-api.html"
    style = {'template_pack': 'rest_framework/vertical/'}
    serializer_class = PasswordUpdateSerializerApi
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    context_serializer = context_serializer_start

    def get(self, request, *args, **kwargs): #self, request, *args, **kwargs
    # def get(self, request, format=None):   
        context_serializer_get = {}
        # messages.info(request, "")
        # user = self.request.user  # !!!

        account = request.user
        serializer = self.serializer_class(account)
        # serializer = self.serializer_class()
        context_serializer_get = self.context_serializer
        context_serializer_get['style'] = self.style 
        context_serializer_get['serializer'] = serializer
        
        return Response(context_serializer_get, )

    def post(self, request, format=None):
        context_serializer_post = {}
        # messages.info(request, "")

        context_serializer_post = self.context_serializer
        context_serializer_post['style'] = self.style

        account = request.user
        serializer = self.serializer_class(account, data=request.data)
        # serializer = self.serializer_c;ass(account, data=request.data)
        initial_val = serializer.initial_data
        oldpassword_val = initial_val['oldpassword']
        password_val = initial_val['password']
        email_val = initial_val['email']
        pass1_val = 'no_pass1'
        if initial_val['current_url']:
            current_url_val = initial_val['current_url']
            context_serializer_post['current_url'] = current_url_val
        else:
            context_serializer_post['current_url'] = ""

        context_serializer_post['oldpassword'] = oldpassword_val
        context_serializer_post['password'] = password_val
        context_serializer_post['e_mail'] = email_val
        context_serializer_post['pass1'] = pass1_val

        if serializer.is_valid():
            account = serializer.save()
            # user = self.get_object()
            if not account.check_password(serializer.data.get('oldpassword')):
                context_serializer_post_if = {}
                # errs = serializer.errors
                # message_errors = serializer_errors(errs)
                # print('register message_errors:', message_errors)
                msgs = ['INFORMATION:<br>', 'Wrong old password.']
                messages.info(request, ''.join(msg for msg in msgs))
                context_serializer_post_if = context_serializer_post
                context_serializer_post_if['serializer'] = serializer

                return Response(context_serializer_post_if,  template_name="password-update.html")

            elif account.check_password(serializer.data.get('oldpassword')):
                account.save()
                context_serializer_post_elif = {}

                msgs = ['MESSAGE: <br>', 'Profile details updated success']
                messages.info(request, ''.join(msg for msg in msgs))

                context_serializer_post_elif = context_serializer_post
                context_serializer_post_elif['serializer'] = serializer 
                context_serializer_post_elif['msgs_info'] = msgs

                return Response(context_serializer_post_elif, )
        else:
            context_serializer_post_else = {}
            errs = serializer.errors
            message_errors = serializer_errors(errs)
            # print('register message_errors:', message_errors)
            messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
            context_serializer_post_else = context_serializer_post
            context_serializer_post_else['serializer'] = serializer
            context_serializer_post_else['errors'] = message_errors 

            return Response(context_serializer_post_else,  template_name="password-update-api.html")

        # return Response(None, status=status.HTTP_202_ACCEPTED)
        context_serializer_Response =  {}
        # context_serializer_Response = context_serializer_post
        context_serializer_Response = self.context_serializer
        context_serializer_Response['style'] = self.style
        context_serializer_Response['serializer'] = self.serializer_class
        # context_Response_return['serializer'] = serializer
        return Response(context_serializer_Response,  template_name="password-update-api.html")



# from accounts.models import EmailConfirmationToken
# from accounts.utils import send_confirmation_email
# from rest_framework.parsers import (
#     MultiPartParser, 
#     FormParser
#     )
# from django.urls import reverse_lazy


# class UserInformationAPIVIew(APIView):

#     permission_classes = [IsAuthenticated,]

#     def get(self, request):
#         r_user = request.user
#         email = r_user.email
#         is_email_confirmed = r_user.is_email_confirmed
#         payload = {'email': email, 'is_email_confirmed': is_email_confirmed, 'id': r_user.pk}
#         return Response(data=payload, status=200)


# class SendEmailConfirmationTokenAPIView(APIView):

#     permission_classes = [IsAuthenticated,]

#     def post(self, request, format=None):
#         r_user = request.user
#         token = EmailConfirmationToken.objects.create(user=r_user)
#         send_confirmation_email(email=r_user.email, token_id=token.pk, user_id=r_user.pk)
#         return Response(data=None, status=201)
    
# def confirm_email_view(request):
#     token_id = request.GET.get('token_id', None)
#     user_id = request.GET.get('user_id', None)
#     try:
#         token = EmailConfirmationToken.objects.get(pk=token_id)
#         user = token.user
#         user.is_email_confirmed = True
#         user.save()
#         data = {'is_email_confirmed': True}
#         return render(request, template_name='users/confirm_email_view.html', context=data)
#     except EmailConfirmationToken.DoesNotExist:
#         data = {'is_email_confirmed': False}
#         return render(request, template_name='users/confirm_email_view.html', context=data)


