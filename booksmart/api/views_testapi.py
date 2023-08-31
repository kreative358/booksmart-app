from booksmart.models import Book, Author, Account
from booksmart.api.serializers import BookSerializer, AuthorSerializer
from accounts.api.serializers import AccountsSerializer, AccountSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import request

serializer_account = AccoutkSerializer(account)
serializer_account_data = serializer_account.data
print(repr(serializer))

serializer_current = AccoutskSerializer(Account.objects.all().filter(request.user))
serializer_current_data = serializer_current_data.data
user_id = serializer_current_data['id']
print('serializer_user_id:', user_id)
print(repr(serializer_account_data))


# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, renderer_classes, permission_classes
# from .serializers import RegistrationSerializer, AccountPropertiesSerializer
# from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer
# from django.db import IntegrityError 
# from django.core.exceptions import ValidationError
# # class LoginSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Account
# #         fields = ['email', 'password',]

# #         extra_kwargs = {'password': {'write_only': True}}

# #     def validate(self, data):
# #         password = data.get('password')
# #         email = data.get('email')

# #@api_view(['POST', ])
# def registration_view_api_my_1(request):

#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data)
#         form = RegistrationSerializer(request.POST)
#         context = {}
#         if serializer.is_valid():
#             account = serializer.save()
#             email = account.cleaned_data.get('email')
#             user = serializer.validated_data['account']
#             username = account.cleaned_data.get('username')
#             token = Token.objects.get(user=account).key 
            
#         else:
#             data = serializer.errors
#         print(type(data))
#         print('data: ', data)
#         return data
#         # return Response(data)
# import io
# from rest_framework.parsers import JSONParser

# # authentication_classes = [authentication.TokenAuthentication]
# @api_view(['POST', ])
# @permission_classes([])
# # @authentication_classes([])
# def registration_view(request):
#     if request.method == 'POST':
#         data = {}
#         email = request.data.get('email', '0')
#         if validate_email(email) != None:
#             data['error_message'] = 'That email is already in use.'
#             data['response'] = 'Error'
#             return Response(data)

#         username = request.data.get('username', '0')
#         if validate_username(username) != None:
#             data['error_message'] = 'That username is already in use.'
#             data['response'] = 'Error'
#             return Response(data)

#         serializer = RegistrationSerializer(data=request.data)
		
#         if serializer.is_valid():
#             account = serializer.save()
#             data['response'] = 'successfully registered new user.'
#             data['email'] = account.email
#             data['username'] = account.username
#             data['pk'] = account.pk
#             token = Token.objects.get(user=account).key
#             data['token'] = token
#         else:
#             data = serializer.errors
#         return Response(data)

# def validate_email(email):
#     account = None
#     try:
#         account = Account.objects.get(email=email)
#     except Account.DoesNotExist:
#         return None
#     if account != None:
#         return email

# def validate_username(username):
#     account = None
#     try:
#         account = Account.objects.get(username=username)
#     except Account.DoesNotExist:
#         return None
#     if account != None:
#         return username
# # response.data = {'results': response.data

# @api_view(['POST', ])
# @renderer_classes([TemplateHTMLRenderer])
# def registration_view_api_my_2(request):
#         context_r = {}
#     # json = JSONRenderer().render(serializer.data)
#         # if "registration_f" in request.POST.get:
#         serializer = RegistrationSerializer(data=request.data)
        
#         data = {}
        
#         if serializer.is_valid():
#             account = serializer.save()
#             data['response'] = 'successfully registered new user.'
#             message = data['response']
#             data['email'] = account.email
#             email = data['email']
#             data['username'] = account.username
#             username=data['username']
#             token = Token.objects.get(user=account).key
#             account.token = token
#             data['token'] = token
#             token = data['token']

#             account=authenticate(data)
#             account=authenticate(message=message, email=email, username=username, token=token)
#             login(data)
#             return redirect("/")
#         else:
#             data = data.is_valid()
#             data = serializer.errors
#             context_r['registration_form'] = data
#         data = data.is_valid()
#         context_r['registration_form'] = data
        
#         content_r = context_r['registration_form']
#         return data


# @api_view(['GET', ])
# @permission_classes((IsAuthenticated, ))
# def account_properties_view(request):

# 	try:
# 		account = request.user
# 	except Account.DoesNotExist:
# 		return Response(status=status.HTTP_404_NOT_FOUND)

# 	if request.method == 'GET':
# 		serializer = AccountPropertiesSerializer(account)
# 		return Response(serializer.data)   
        
# @api_view(['POST', ])
# @renderer_classes([StaticHTMLRenderer])
# def registration_view_api(request):
#     context = {}
#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data)
        
#         data = {}
        
#         if serializer.is_valid():
#             account = serializer.save()
#             data['response'] = 'successfully registered new user.'
#             data['email'] = account.email
#             email = data['email']
#             data['username'] = account.username
            
#             token = Token.objects.get(user=account).key
#             data['token'] = token
           
#         else:
#             data = serializer.errors

#         return Response(data)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# #@renderer_classes([TemplateHTMLRenderer])
# def register_users(request):
#     try:
#         context_r = {}
#         data = {}
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             account = serializer.save()
#             account.is_active = True
#             account.save()
#             token = Token.objects.get_or_create(user=account)[0].key
#             data["message"] = "user registered successfully"
#             data["email"] = account.email
#             data["username"] = account.username
#             data["token"] = token
            
#         else:
#             data = serializer.errors

#         context_r['register_form'] = data
#         content_r = context_r['register_form']
#         return content_r
#     except IntegrityError as e:
#         account=Account.objects.get(username='')
#         account.delete()
#         raise ValidationError({"400": f'{str(e)}'})

#     except KeyError as e:
#         print(e)
#         raise ValidationError({"400": f'Field {str(e)} missing'})


# @api_view(["POST"])
# #@renderer_classes([TemplateHTMLRenderer])
# @permission_classes([AllowAny])
# def login_user(request):
#     context_l = {}
#     data = {}
#     req_body = json.loads(request.body)
#     print(req_body)
#     #if 'login_f' in req_body:
#     email1 = req_body['email']
#     print(email1)
#     password = req_body['password']
#     try:

#         account = Account.objects.get(email=email1)
#     except BaseException as e:
#         raise ValidationError({"400": f'{str(e)}'})

#     token = Token.objects.get_or_create(user=account)[0].key
#     print(token)
#     if not check_password(password, account.password):
#         raise ValidationError({"message": "Incorrect Login credentials"})

#     if account:
#         if account.is_active:
            
#             print(request.user)
#             login(request, account)
#             data["message"] = "user logged in"
#             data["email"] = account.email
#             context_l['login_form'] = data
#             content_l = context_l['login_form']
#             #Res = {"data": data, "token": token}
#             #return Response(Res)
#             return content_l

#         else:
#             raise ValidationError({"400": f'Account not active'})

#     else:
#         raise ValidationError({"400": f'Account doesnt exist'})

# https://medium.com/geekculture/register-login-and-logout-users-in-django-rest-framework-51486390c29
# def logout_user(request):
#     user = request.user
#     #if user.is_authenticated:
#     request.user.auth_token.delete()
#     logout(request)
#     return redirect('/')
#     # return Response('User Logged out successfully')


# class AccountViewSet(viewsets.ModelViewSet):
#     """
#     A viewset that provides the standard actions
#     """
#     queryset = User.objects.all()
#     serializer_class = AccountSerializer

#     @action(detail=True, methods=['post'])
#     def set_password(self, request, pk=None):
#         user = self.get_object()
#         serializer = PasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             user.set_password(serializer.validated_data['password'])
#             user.save()
#             return Response({'status': 'password set'})
#         else:
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=False)
#     def recent_users(self, request):
#         recent_users = User.objects.all().order_by('-last_login')

#         page = self.paginate_queryset(recent_users)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(recent_users, many=True)
#         return Response(serializer.data)

# from rest_framework import generics

# class BookList(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class BookDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                       IsOwnerOrReadOnly]

# class AuthorList(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = AuthorSerializer
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                       IsOwnerOrReadOnly]


# class AccountList(generics.ListAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer


# class AccountDetail(generics.RetrieveAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer

# @api_view(['GET', 'PUT', 'DELETE'])
# def author_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         author = Author.objects.get(pk=pk)
#     except Author.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = AuthorSerializer(author)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = AuthorSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         author.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE'])
# def book_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         book = Book.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = BookSerializer(book)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = BookSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)