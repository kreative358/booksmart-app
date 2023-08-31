import os, requests, json, re
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.models import User
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
from accounts.api.serializers import RegistrationSerializerApi, AccountUpdateSerializerApi, LoginSerializerApi, PasswordSerializerApi, AccountSerializer, UserDetailSerializer, UserSerializer

from rest_framework import routers, serializers, viewsets
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
from accounts.models import Account

from rest_framework.decorators import action
from booksmart.models import Author, Book
from booksmart.api.permissions import IsOwnerOrReadOnly
from accounts.api.hyperlink import PlainTextRenderer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # authentication_classes = [TokenAutentication, SessionAuthentication, BasicAuthentication]
    # permission_classes = (IsSuperuserOrIsSelf,)
    permission_classes = permission_classes = [IsOwnerOrReadOnly,]  #(permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly)


class RegistrationAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    
    renderer_classes = [TemplateHTMLRenderer, HTMLFormRenderer]
    permission_classes = [AllowAny,]
    template_name="register_view.html"
    ser_val = {}
    style = {'template_pack': 'rest_framework/vertical/'}
    serializer_class = RegistrationSerializerApi

    def get(self, request, *args, **kwargs):
    
        serializer = self.serializer_class()
        return Response({'serializer':serializer, 'style':self.style}, )
    def post(self, request, *args, **kwargs):
        # datas = request.data.copy()
        
        print('request data:',request.data)
        serializer = self.serializer_class(data=request.data)
        # initial_val = request.data
        initial_val = serializer.initial_data
        username_val = initial_val['username']
        email_val = initial_val['email']
        pass1_val = initial_val['password1']
        pass2_val = initial_val['password2']
        pass_val = 'no_pass'
        
        print('registration initial_val accounts/api', initial_val)
        # https://stackoverflow.com/questions/36414804/integrate-django-password-validators-with-django-rest-framework-validate-passwor
        # https://medium.com/django-rest/django-rest-framework-login-and-register-user-fd91cf6029d5
        # https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
        # https://www.django-rest-framework.org/api-guide/serializers/#accessing-the-initial-data-and-instance
        if serializer.is_valid():
            account = serializer.save()
            print('account:', account)

            if account:
                login(request, account)
                try:
                    token = Token.objects.get(user=account)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=account)

                if token:
                    print('token.key', token.key)
                else:
                    print('no token')
                
                # if request.path == "/booksmartapp/accounts-app/account-urls/register_view/":
                #     messages.info(request, 'Account created successfully')
                #     return redirect("index")
                # elif reqest.path == "api/browserapi/register_view/":
                #     messages.info(request, 'Account created successfully')
                #     return redirect("index")
                msgs = ['INFORMATION:', 'Account created successfully']
                
                messages.info(request, "<br>".join(msg for msg in msgs))
              
                return redirect("index")
                # return Response({'serializer':serializer, 'msgs_info': msgs, 'style': self.style, 'username':username_val, 'email': email_val, 'password1':pass1_val, 'password2':pass2_val,'password':pass_val},  template_name="index.html")

        else:
            errs = serializer.errors
            message_errors = serializer_errors(errs)

            # print('register message_errors:', message_errors)
            # if request.path == "/booksmartapp/accounts-app/account-urls/register_view/":
            #     messages.info(request, "<br>".join(msg_error for msg_error in message_errors))

                # return Response({'serializer':serializer, 'style':self.style,  'message_errors':  message_errors}, status=status.HTTP_202_ACCEPTED, template_name="register_view.html")
            # messages_info =  message_errors
            messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
            # return messages_info
            return Response({'serializer':serializer, 'errors': message_errors, 'style': self.style, 'username':username_val, 'email': email_val, 'password1':pass1_val, 'password2':pass2_val,'password':pass_val},  template_name="register_view.html")


        return Response({'serializer':serializer, 'style': self.style},  template_name="register_view.html") # v
        # return Response(None, status=status.HTTP_202_ACCEPTED) # response.status_code
        # return Response(None, status=response.status_code)


# class LoginView(APIView):
class LoginAPIView(GenericAPIView):
    # This view should be accessible also for unauthenticated users.
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer, HTMLFormRenderer, PlainTextRenderer]
    permission_classes = (permissions.AllowAny,)
    template_name="login_view.html"
    style = {'template_pack': 'rest_framework/vertical/'}
    serializer_class = LoginSerializerApi

    def get(self, request, *args, **kwargs):
        
        serializer = self.serializer_class()
        return Response({'serializer':serializer, 'style': self.style},)
    

    def post(self, request, *args, **kwargs):
        # try:
        print('request data', request.data)
        # serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer = self.serializer_class(data=request.data)
        initial_val = serializer.initial_data
        # initial_val = initial_values.data


        # except Exception as e:
        #     print(f'exception: {e}')

        # if initial_val['username'] and initial_val['password']:
        username_val = initial_val['username']
        pass_val = initial_val['password']
        email_val = 'no_email'
        print("login initial_val['current_url']:", initial_val )
        if serializer.is_valid():
            # user = serializer.save(commit=False)
            #try:
            user = serializer.validated_data['user']
            # user = authenticate(username=username_val, password=password_val)
            # serializer.is_valid()
            if user:
                login(request, user)

                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)

                if token:
                    print('token.key', token.key)
                else:
                    print('no token')

                msgs = ['INFORMATION: <br>', 'You logged in successfully']
                # messages.info(request, "<br>".join(msg for msg in msgs))
                messages.info(request, ''.join(msg for msg in msgs))

                return redirect("index")
                # return Response({'serializer':serializer, 'msgs_info': msgs, 'style': self.style, 'username':username_val, 'email': email_val, 'password':pass_val}, template_name="/" )

            else:
                pass
                # errs = serializer.errors
                # message_errors = serializer_errors(errs)  
                # # print('1 serializer.errors -', serializer.errors)              
                # # ser_values = {}
                # # print('elif not user:')
                # # request.user = AnonymousUser()
                # # # serializer = self.serializer_class()
                # # msg_exc = 'Access denied: wrong username or password - elif.'
                # # print(">>> elif <<<")
                # # messages.info(request, msg_exc)
                # # return redirect("/booksmartapp/accounts-app/login_view.html")
                # # return redirect("login_view.html")
                # # errs = serializer.errors
                # # message_errors = serializer_errors(errs)
                # # # messages_info =  message_errors
                # # messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
                # # return messages_info
                # # msgs = ['INFORMATION<br>', 'Access denied:<br>', '- wrong username or password']
                # # messages.info(request, "".join(msg for msg in msgs))
                # print('1 message_errors', message_errors)
                # messages.info(request, "<br>".join(msg_error for msg_error in message_errors))               

                # return Response({'serializer':serializer, 'style': self.style, 'errors': message_errors, 'username':username_val, 'password':pass_val, 'email': email_val},  template_name="login_view.html")
                    
                 
            # except:
            #     if initial_val['username'] != '' and initial_val['password'] != '':
            #         msg_exc = ['Access denied: wrong username or password.',]
            #         username = initial_val['username']
            #         password = initial_val['password']
            #     elif initial_val['username'] != '' and  initial_val['password'] == '':
            #         msg_exc = ['Both "username" and "password" are required.', 'You forgot about password',]
            #         username = initial_val['username']
            #         password = " "
            #     elif initial_val['username'] == '' and initial_val['password'] != '':
            #         msg_exc = ['Both "username" and "password" are required.', 'You forgot about password',]
            #         username = " "
            #         password = initial_val['password']
            #     elif initial_val['username'] == '' and initial_val['password'] == '':
            #         msg_exc = ['Both "username" and "password" are required.', 'You forgot about username and password',]
            #         username = " "
            #         password = " "
            #     else:
            #         msg_exc = '<br>'
                    

            #     msg = 'Access denied: wrong username or password - except.'
            #     print(">>> except <<<")
            #     messages.info(request, msg)
            #     # messages.info(request, "<br>".join(msg_exc))
            #     # return redirect("/booksmartapp/accounts-app/login_view.html")
            #     return redirect("login-view")
            
        else:
            errs = serializer.errors
            message_errors = serializer_errors(errs)
            # print('2 serializer.errors:', serializer.errors)
            print('2 message_errors:', message_errors)
            # ser_values = {}
            # print('elif not user:')
            # request.user = AnonymousUser()
            # serializer = self.serializer_class()


            message_code = ['code error: authorization']
            # msgs = ['INFORMATION:<br>','Access denied:<br>', '- both username and password are essenital']
            # msgs = ['MESSAGE:<br>', 'Access denied:<br> both username and password are essenital']
            # print(">>> else <<<")
            # messages.info(request, ''.join(msg for msg in msgs))
            messages_errors = message_errors + message_code
            messages.info(request, "<br>".join(msg_error for msg_error in messages_errors))
            return Response({'serializer':serializer, 'errors': messages_errors, 'style': self.style,'username':username_val, 'password':pass_val, 'email': email_val},  template_name="login_view.html")

        return Response({'serializer':serializer, 'style': self.style},  template_name="login_view.html")


class AccountUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    
    renderer_classes = [TemplateHTMLRenderer, HTMLFormRenderer]
    permission_classes = [IsOwnerOrReadOnly,] 
    template_name="account_view.html"
    ser_val = {}
    style = {'template_pack': 'rest_framework/vertical/'}
    serializer_class = AccountUpdateSerializerApi
    # style = { 'placeholder': 'field to enter email', 'autofocus': True, 'size':'36', 'id':'bs_input'}
    def get(self, request, *args, **kwargs): #self, request, *args, **kwargs
    # def get(self, request, format=None):    
        account = request.user
        serializer = self.serializer_class(account)
        return Response({'serializer':serializer, "user_username":account.username, 'user_email':account.email, 'style':self.style })
        # return Response({'serializer':serializer, 'style': self.style})
    
    def post(self, request, format=None):
        account = request.user
        serializer = self.serializer_class(account, data=request.data)
        # serializer = self.serializer_c;ass(account, data=request.data)
        initial_val = serializer.initial_data
        username_val = initial_val['username']
        email_val = initial_val['email']
        pass1_val = 'no_pass1'
        if serializer.is_valid():
            serializer.save()
            
            # if initial_val['current_url']!= "":
            #     print("login initial_val['current_url']:", initial_val['current_url'] )
            #     messages.info(request,'Profile details updated.')
            #     return redirect(f"booksmart:{initial_val['current_url']}")
            # else:
            msgs = ['INFORMATION:<br>', 'Profile details updated.']
            messages.info(request, ''.join(msg for msg in msgs))
            return redirect("index")
            # return Response({'serializer':serializer, 'msgs_info': msgs, 'username':username_val, 'email': email_val, 'password1':pass1_val, 'style':self.style})
        else:
            errs = serializer.errors
            
            message_errors = serializer_errors(errs)
            print('update message_errors:', message_errors)
            
            # new_errors = {}
            # new_errs = []
            # for field_name, field_error in errs.items():
            #     new_errors[field_name] = field_error[0]
            #     err = f"Field: {field_name}, error: {field_error[0]}"
            #     new_errs.append(err)

            # if initial_val['current_url']!= "":
            #     #print("login initial_val['current_url']:", initial_val['current_url'] )
            #     messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
            #     return redirect(f"booksmart:{initial_val['current_url']}")

            #else:
            messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
            return Response({'serializer':serializer, 'errors': message_errors, 'style':self.style, 'username':username_val, 'email': email_val, 'password1':pass1_val},  template_name="account_view.html")
                    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(None, status=status.HTTP_202_ACCEPTED)
        return Response({'serializer':serializer, 'style': self.style},)

# class PasswordUpdateAPIView(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    
#     renderer_classes = [TemplateHTMLRenderer, HTMLFormRenderer]
#     permission_classes = [IsOwnerOrReadOnly,] 
#     template_name="account_view.html"
#     ser_val = {}
#     style = {'template_pack': 'rest_framework/vertical/'}
#     serializer_class = PasswordUpdateSerializerApi

#     def get(self, request, *args, **kwargs):  
#         account = request.user
#         serializer = self.serializer_class(account)
#         return Response({'serializer':serializer, "user_username":account.username, 'user_email':account.email, 'style':self.style })
    
#     def post(self, request, format=None):
#         account = request.user
#         serializer = self.serializer_class(account, data=request.data)
#         initial_val = serializer.initial_data
#         username_val = initial_val['username']
#         email_val = initial_val['email']
#         pass1_val = 'no_pass1'
#         if serializer.is_valid():
#             serializer.save()
#             msgs = ['INFORMATION:<br>', 'Profile details updated.']
#             messages.info(request, ''.join(msg for msg in msgs))
#             return redirect("index")

#         else:
#             errs = serializer.errors
            
#             message_errors = serializer_errors(errs)
#             print('update message_errors:', message_errors)

#             messages.info(request, "<br>".join(msg_error for msg_error in message_errors))
#             return Response({'serializer':serializer, 'errors': message_errors, 'style':self.style, 'username':username_val, 'email': email_val, 'password1':pass1_val},  template_name="account_view.html")

#         return Response({'serializer':serializer, 'style': self.style},)

@api_view(["GET"])
@permission_classes([AllowAny,])
def logout_api(request):

    try:
        print("request.data:", request.data)
        request.user.auth_token.delete()
        logout(request)
        msgs = ['MESSAGE<br>','Logout successfully, token deleted']
        messages.info(request, ''.join(msg for msg in msgs))

        return redirect('/')
    except:
        logout(request)
        msgs = ['MESSAGE<br>','Logout successfully']
        messages.info(request, ''.join(msg for msg in msgs))
        return redirect('/')

    return Response(None, status=status.HTTP_202_ACCEPTED)

from accounts.api.serializers import UserSerializer
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = Account.objects.all().order_by('-date_joined')
    # serializer_class = AccountDetailsSerializer
    # permission_classes = [permissions.IsAdminUser]
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    @action(detail=True, methods=['POST', 'GET'], serializer_class=PasswordSerializerApi)
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializerApi(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class UserDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsOwnerOrReadOnly,] 
    queryset = Account.objects.all()
    serializer_class = UserDetailSerializer
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Account.objects.filter(id=user.id)

    @action(detail=True, methods=['POST', 'GET'], serializer_class=PasswordSerializerApi)
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializerApi(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

def example_apiview(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)





# https://www.guguweb.com/2022/01/23/django-rest-framework-authentication-the-easy-way/
# class CustomAuthToken(ObtainAuthToken):
#     template_name = "login.html"
#     authentication_classes = []
#     permission_classes = []
#     renderer_classes = [TemplateHTMLRenderer]
#     style = {'template_pack': 'rest_framework/vertical/'}
#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class()
#         serializer.is_valid()
#         return Response({'serializer': serializer})
#     def post(self, request, *args, **kwargs):
#         account = request.user
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
        
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         login(request, account)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         }, status=status.HTTP_202_ACCEPTED)
