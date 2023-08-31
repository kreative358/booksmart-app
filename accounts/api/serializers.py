from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import Account
from booksmart.models import Book, Author
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError, APIException
from collections import OrderedDict
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
import requests
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator, BaseUniqueForValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib import messages
import sys
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth import password_validation
from accounts.api.hyperlink import AuthorHyperlink, BookHyperlink
from accounts.api.hyperlink import OwnAuthorSerializer, OwnBookSerializer
from accounts.api.hyperlink import OwnAuthorField, OwnBookField
# from rest_auth.serializers import LoginSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):

    username = serializers.CharField(
    required=False, 
    # allow_blank=True,
    style={'template':'snippets/input-username.html'},
    validators=[UniqueValidator(queryset=Account.objects.all(), message="this username already exists, this field must be unique")],
    )

    email = serializers.EmailField(
    required=False, 
    style={'template':'snippets/input-email.html'},
    validators=[UniqueValidator(queryset=Account.objects.all(), message='this email already exists, this field must be unique' ) ],
    )

    class Meta:
        model = Account
        fields = ('url', 'id', 'username', 'email', )
        # extra_kwargs = {
        #     'style':{'template':'snippets/input-custom.html', 'autofocus': True,},}
        

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    authors = OwnAuthorSerializer(many=True, read_only=True)
    books = OwnBookSerializer(many=True, read_only=True)

    # authors = OwnAuthorField(many=True)
    # books = OwnBookField(many=True)

    # authors = AuthorHyperlink(many=True, read_only=False)
    # books = BookHyperlink(many=True, read_only=False)

    # authors = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='browserapi:author-detail', read_only=True)

    # books = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='browserapi:book-detail', read_only=True)

    username = serializers.CharField(
    required=False,
    # allow_blank=True,
    style={'placeholder': 'enter new username'},
    validators=[UniqueValidator(queryset=Account.objects.all(), message="this username already exists, this field must be unique")],)

    email = serializers.EmailField(
    required=False, 
    style={'placeholder': 'enter new email', },
    validators=[UniqueValidator(queryset=Account.objects.all(), message='this email already exists, this field must be unique' ) ],)

    class Meta:
        model = Account
        fields = ('url', 'id', 'username', 'email', 'authors', 'books')

    # # OwnAuthorSerializer
    # def create(self, validated_data):
    #     authors_data = validated_data.pop('authors')
    #     books_data = validated_data.pop('books')
    #     account = Account.objects.create(**validated_data)
    #     for author_data in authors_data:
    #         Author.objects.create(account=account, **author_data)
    #     return account

    # # OwnBookSerializer
    # def create(self, validated_data):
    #     books_data = validated_data.pop('books')
    #     account = Account.objects.create(**validated_data)
    #     for book_data in books_data:
    #         Book.objects.create(account=account, **book_data)
    #     return account
        

class UserDetailSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = Account
        fields = ('pk', 'url', 'username', 'email',)


# class AccountsSerializer(serializers.HyperlinkedModelSerializer):
#     apiauthors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
#     apibooks = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
#     # apiaccounts = serializers.PrimaryKeyRelatedField(many=True, queryset=Accounts.objects.all())
#     id = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = Account
#         fields = ['url', 'id', 'username', 'email', 'accounts', 'apibooks', 'apiauthors']


# class AccountSerializer(serializers.HyperlinkedModelSerializer):
#     apiauthors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
#     apibooks = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
#     id = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = Account
#         fields = ['url', 'id', 'username', 'email']

# https://python.plainenglish.io/django-custom-user-model-and-auth-using-jwt-simple-boilerplate-6acd78bf7767
# class RegisterPostSerializer(serializers.ModelSerializer):
class RegistrationSerializerApi(serializers.ModelSerializer):

#     # current_url = serializers.CharField(read_only=True, allow_blank=True, required=False)
#     current_url = serializers.HiddenField(
#     default="index"
# )

    username = serializers.CharField(
    required=False, 
  
    # validators=[UniqueValidator(queryset=Account.objects.all())],
    # error_messages ={'username': "This username already exists."},
    style={'template':'snippets/input-username.html', 'placeholder': 'enter username'},
    validators=[UniqueValidator(queryset=Account.objects.all(), message="this username already exists, this field must be unique")],
    )

    email = serializers.EmailField(
    required=False, 
    #allow_blank=True,
    # style={'input_type': 'email'},
    # validators=[UniqueValidator(queryset=Account.objects.all())],
    # error_messages ={'email':"This email already exists."}
    style={'template':'snippets/input-email.html', 'placeholder': 'enter email' },
    validators=[UniqueValidator(queryset=Account.objects.all(), message='this email already exists, this field must be unique' ) ],
    )

    password1 = serializers.CharField(
    required=False, 
    write_only=True,
    style={'template':'snippets/input-password1.html', 'placeholder': 'enter password'},
    )


    def validate_password(self, password1):
        print('password1:', password1)
        try:
            validate_password(password1)
        except ValidationError as exc:
            print('serializers.ValidationError(str(exc)):', serializers.ValidationError(str(exc)))
            raise serializers.ValidationError(str(exc))
        return password1
    
    password2 = serializers.CharField(
        required=False, 

        style={'template':'snippets/input-password2.html', 'placeholder': 'confirm password' },
        write_only=True,
        )


    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError({"password and repeat password": "those two passwords don't match."})
        
        elif attrs.get('password1') == attrs.get('password2'):
            print('attrs:', attrs)
            attrs.pop('password2')
            
            password = attrs.pop('password1')
            attrs['password'] = password
            print('attrs1:', attrs)
            return attrs

 
    class Meta:
        model = Account
        fields = ['email', 'username', 'password1', 'password2'] # 'current_url',

# serializer = RegistrationSerializerApi()   
# print("repr(serializer):", repr(serializer)) 

# https://www.appsloveworld.com/django/100/17/django-rest-framework-3-serializers-on-non-model-objects

class LoginSerializerApi_New(serializers.ModelSerializer):
    username = serializers.CharField(
        required=False, 
        style={'template':'snippets/input-username.html', 'placeholder': 'enter username'},      
                    )

    def validate_username(self, username):
        if username == "":
            # if len(username) < 4:
            raise serializers.ValidationError({'field username error': 'this field can not be empty'})
        else:
            return username


    password = serializers.CharField( 
        required=False, 
        style={'template': 'snippets/input-password.html', 'placeholder': 'enter password'},  
        # validators=[BaseUniqueForValidator()]
                    )

    def validate_password(self, password):
        if password == "":
            # if len(username) < 4:
            raise serializers.ValidationError({'field password error': 'this field can not be empty'})
        else:
            return password

    # def validate_username(self, username):
    #     if attrs.get('username') == "":
    #         raise serializers.ValidationError({'non field error': 'field username can not be empyt'})
    #     else
    #         return username
    remember_me = serializers.BooleanField(required=False, style={'autofocus': True})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                user = authenticate(request=self.context.get('request'), username=username, password=password)
                attrs['user'] = user
                attrs.pop('remember_me')
                print("attrs:", attrs)
                return attrs               
                
            except:
                raise serializers.ValidationError({'MESSAGE:', 'wrong username or password'})
        


    class Meta:
        model = Account
        fields = ['username', 'password', 'remember_me']



class LoginSerializerApi(serializers.Serializer):
# class LoginSerializerApi(serializers.ModelSerializer):    
    # current_url = serializers.CharField(read_only=True, allow_blank=True, required=False)

    username = serializers.CharField(
        required=False, 

        # required=False,
        # allow_blank=True,
        # label="Username",
        style={'template':'snippets/input-username.html', 'placeholder': 'enter username',},
        )

    password = serializers.CharField(  
        required=False,
        # allow_blank=True,

        style={'template': 'snippets/input-password.html', 'placeholder': 'enter password',},
        
        # This will be used when the DRF browsable API is enabled
        # style={'input_type': 'password', 'placeholder': 'field to enter email', 'autofocus': True, 'size':'36', 'id':'bs_input'},
        # trim_whitespace=False,
        # write_only=True,
        # help_text='Minimum 8 signts include one upper letter and one number',
        
    )
    remember_me = serializers.BooleanField(
        required=False, 
        style={'autofocus': True}
        )


    # class Meta:
    #     model = Account
    #     fields = ['username', 'password', 'remember_me']  

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # try:
            #     user = authenticate(request=self.context.get('request'), username=username, password=password)
            # except APIException as exc:
            #     print('serializers.ValidationError(str(exc)):', serializers.APIException(str(exc)))
            #     raise serializers.APIException(str(exc))

            user = authenticate(request=self.context.get('request'), username=username, password=password)

            # # The authenticate call simply returns None for is_active=False
            # # users. (Assuming the default ModelBackend authentication
            # # backend.)
            # # raise ValidationError(str(e))
            # print('user', user)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                # msg = ['MESSAGE', 'Unable to log in with provided credentials.', 'wrong username or password']
                raise serializers.ValidationError(msg, code='authorization')
                # raise msg
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        attrs.pop('remember_me')
        print("attrs:", attrs)
        return attrs

    # class Meta:
    #     model = Account
    #     fields = ['username', 'password', 'remember_me'] 

    # type = serializers.CharField(style={'base_template': 'textarea.html', 'rows': 10})
    # class Meta:
    #     model = Account
    #     fields = ['username', 'password', 'remember_me']

    # def authenticate(self, **kwargs):
    #     return authenticate(self.context['request'], **kwargs)


    # def validate(self, attrs):
    #     username = attrs.get('username')
    #     password = attrs.get('password')
    #     if username and password:
    #         user = self.authenticate(username=username, password=password)
    #         print('user')
    #         if not user:
    #             msg = ['Unable to log in with provided credentials.']
    #             raise exceptions.ValidationError(msg)

    #     else:
    #         msg = ['Must include "username" and "password".']
    #         raise exceptions.ValidationError(msg)

    #     attrs['user'] = user
    #     return attrs



            # Try to authenticate the user using Django auth framework.
            # try:
        #     #     user = authenticate(request=self.context.get('request'), username=username, password=password)
        #     print(" user:", user)
        #     # except ValidationError as exc:
        #     #     print('serializers.ValidationError(str(exc)):', serializers.ValidationError(str(exc)))
        #     #     raise serializers.ValidationError(str(exc))
        #         # print('not user')
        #         # user = AnonymousUser()
        # else:
        #     # print('AnonymousUser')
        #     # user = AnonymousUser()
        #     raise serializers.ValidationError()

        # attrs['user'] = user
        # if attrs:
        #     print('attrs:', attrs)
        # else:
        #     print('no attrs')
        # return attrs
        
    
    # class Meta:
    #     model = Account
    #     fields = ['current_url', 'username', 'password', 'remember_me'] 
        # else:
        #     user = AnonymousUser()

        # attrs['user'] = user
        # if attrs:
        #     print('attrs:', attrs)
        # else:
        #     print('no attrs')
        # return attrs   

class PasswordSerializerApi(serializers.ModelSerializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(
        required=False, 
        min_length=8,
        style={'template': 'snippets/input-password.html', 'placeholder': 'field to enter old password'},
        )
    password = serializers.CharField(
    required=False, 
    style={'template': 'snippets/input-password.html', 'placeholder': 'field to enter new password' }),

    def validate_password(self, new_password):
        print('password:', new_password)
        try:
            validate_password(password)
        except ValidationError as exc:
            print('serializers.ValidationError(str(exc)):', serializers.ValidationError(str(exc)))
            raise serializers.ValidationError(str(exc))
        return password

    # password2 = serializers.CharField(
    #     required=True, 
    #     style={'input_type': 'password'},
    #     write_only=True,
    #     )

    # def validate(self, attrs):
    #     if attrs.get('password') != attrs.get('password2'):
    #         raise serializers.ValidationError("Those two passwords don't match.")
        
    #     elif attrs.get('password') == attrs.get('password2'):
    #         print('attrs:', attrs)
    #         attrs.pop('password2')
    #         print('attrs:', attrs)
    #         return attrs

    class Meta:
        model = Account
        fields = ('old_password', 'password', )
        # fields = ('old_password', 'password', 'password2')

class CurrentUserDefaultEmail:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the current user.
    """
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.username

class CurrentUserDefaultUsername:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the current user.
    """
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.email


from django.utils.html import format_html
class AccountUpdateSerializerApi(serializers.ModelSerializer):
    # current_url = serializers.CharField(read_only=True, allow_blank=True, required=False)

    username = serializers.CharField(
    required=False, 
    # allow_blank=True,
    style={'template': 'snippets/input-username.html', 'placeholder': 'enter new username',},
    validators=[UniqueValidator(queryset=Account.objects.all(),  message="<br>- this username  already exists<br>- this field must be unique")],)

    email = serializers.EmailField(
    required=False, 
    style={'template': 'snippets/input-email.html', 'placeholder': 'enter new email', },
    validators=[UniqueValidator(queryset=Account.objects.all(),message='<br>- this email already exists<br>- this field must be unique' ) ],)



    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        if email== "" and username=="":
            raise serializers.ValidationError({'MESSAGE:', 'one of these fields can not be empty'})
        else:
            return attrs


    class Meta:
        model = Account
        fields = ['username', 'email'] # 'current_url', 



    