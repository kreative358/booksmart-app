from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import Account
from booksmart.models import Book, Author

from rest_framework.exceptions import ValidationError
from collections import OrderedDict
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
import requests
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib import messages
import sys
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth import password_validation
from accounts.api.hyperlink import AuthorHyperlink, BookHyperlink
from accounts.api.hyperlink import OwnAuthorSerializer, OwnBookSerializer
from accounts.api.hyperlink import OwnAuthorField, OwnBookField

# property errors
# def errors(self): ret = super().errors if isinstance(ret, list) and len(ret) == 1 and getattr(ret[0], 'code', None) == 'null': detail = ErrorDetail('No data provided', code='null') ret = {api_settings.NON_FIELD_ERRORS_KEY: [detail]} return ReturnDict(ret, serializer=self)
# Full name: rest_framework.serializers.Serializer.errors

# class ReCaptchaSerializer(serializers.Serializer):
#     recaptcha_token = serializers.CharField(
#         read_only=True, 
#         allow_blank=True, 
#         required=False,
#         style={'template':'snippets/input-recaptcha.html'},
#         )

class RegistrationSerializer(serializers.ModelSerializer):

    current_url = serializers.CharField(
        read_only=True, 
        allow_blank=True, 
        required=False,
        style={'template':'snippets/input-hidden.html'},
        )

    username = serializers.CharField(
        required=False, 
        max_length=14,
        style={'template':'snippets/input-username.html', 'placeholder': 'enter username'},
        validators=[UniqueValidator(queryset=Account.objects.all(), message="this username already exists, this field must be unique")],
        )

    # username = serializers.CharField(
    # required=False, 
    # validators=[UniqueValidator(queryset=Account.objects.all())],
    # error_messages ={'username': "This username already exists."},
    # )

    email = serializers.EmailField(
        required=False, 
        #allow_blank=True,
        style={'template':'snippets/input-email.html', 'placeholder': 'enter email'},
        validators=[UniqueValidator(queryset=Account.objects.all(), message='this email already exists, this field must be unique' ) ],
        # validators=[UniqueValidator(queryset=Account.objects.all())],
        # error_messages ={'email':"This email already exists."}
    )

    password = serializers.CharField(
        required=False, 
        # write_only=True,
        style={'template':'snippets/input-password.html', 'placeholder': 'enter password'},
    )

    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as exc:
            print('serializers.ValidationError(str(exc)):', serializers.ValidationError(str(exc)))
            raise serializers.ValidationError(str(exc))
        return password
    
    password2 = serializers.CharField(
        required=False, 
        min_length=8,
        write_only=True,
        style={'template':'snippets/input-password2.html', 'placeholder': 'confirm password', },
        )

    # class BooleanField(*, read_only=False, write_only=False, required=None, default=empty, initial=empty, source=None, label=None, help_text=None, style=None, error_messages=None, validators=None, allow_null=False)
    remember_me = serializers.BooleanField(
        required=False, 
        style={'template':'snippets/input-checkbox-remember.html'}
        )

    recaptcha_token = serializers.CharField(
        read_only=True, 
        allow_blank=True, 
        required=False,
        style={'template':'snippets/input-recaptcha-signin.html'},
        )

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password and repeat password": "Those two passwords don't match."})
        
        elif attrs.get('password') == attrs.get('password2'):
            print('attrs:', attrs)
            attrs.pop('password2')
            attrs.pop('remember_me')
            # attrs.pop('recaptcha')
            # password = attrs.pop('password')
            # attrs['password'] = password
            # attrs.pop('current_url')
            print('attrs1:', attrs)
            return attrs


    class Meta:
        model = Account
        fields = ['current_url', 'username', 'email', 'password', 'password2', 'remember_me', 'recaptcha_token'] # 

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    username = serializers.CharField(
    required=False, 
    # allow_blank=True,
    style={'template':'snippets/input-username.html'},
    validators=[UniqueValidator(queryset=Account.objects.all(), message="this username already exists, this field must be unique")],
    )
    
    email = serializers.EmailField(
    required=False, 
    style={'template':'snippets/input-email.html', 'input_type': 'email'},
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

    email = serializers.EmailField(
    required=False, 
    style={'input_type': 'email', 'placeholder': 'enter new email', 'autofocus': True,},
    validators=[UniqueValidator(queryset=Account.objects.all(), message='this email already exists, this field must be unique' ) ],)

    username = serializers.CharField(
    required=False, 
    max_length=14,
    # allow_blank=True,
    style={'placeholder': 'enter new username', 'autofocus': True,},
    validators=[UniqueValidator(queryset=Account.objects.all(), message="this username already exists, this field must be unique")],)

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
        fields = ('url', 'id', 'username', 'email',)


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




    

# https://www.appsloveworld.com/django/100/17/django-rest-framework-3-serializers-on-non-model-objects



class LoginSerializer(serializers.Serializer):
# class LoginSerializer(serializers.ModelSerializer):    
    current_url = serializers.CharField(
    read_only=True, 
    allow_blank=True, 
    required=False,
    style={'template':'snippets/input-hidden.html', },
    )

    username = serializers.CharField(
        # required=True, 
        required=False,
        allow_blank=True,
        min_length=3,
        # label="Username",
        style={'template':'snippets/input-username.html', 'placeholder': 'enter username'},
        )

    password = serializers.CharField( 
        # required=True, 
        required=False,
        allow_blank=True,
        min_length=8,
        style={'template': 'snippets/input-password.html', 'placeholder': 'enter password',  },
        
        # This will be used when the DRF browsable API is enabled
        # style={'input_type': 'password', 'placeholder': 'field to enter email', 'autofocus': True, 'size':'36', 'id':'bs_input'},
        # trim_whitespace=False,
        # write_only=True,
        # help_text='Minimum 8 signts include one upper letter and one number',
    )

    remember_me = serializers.BooleanField(
        required=False, 
        style={'template':'snippets/input-checkbox-remember.html'},
        )

    recaptcha_token = serializers.CharField(
        read_only=True, 
        allow_blank=True, 
        required=False,
        style={'template':'snippets/input-recaptcha-login.html'},
        )
    # type = serializers.CharField(style={'base_template': 'textarea.html', 'rows': 10})
    class Meta:
        model = Account
        fields = ['current_url', 'username', 'password', 'remember_me', 'recaptcha_token'] 
         


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        attrs.pop('remember_me')
        # attrs.pop('current_url')
        return attrs

    # class Meta:
    #     model = Account
    #     fields = ['current_url', 'username', 'password', 'remember_me']
        
    
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



class PasswordUpdateSerializer(serializers.ModelSerializer):

    current_url = serializers.CharField(
    read_only=True, 
    allow_blank=True, 
    required=False,
    style={'template':'snippets/input-hidden.html','input_type': 'url', },
    )

    oldpassword = serializers.CharField(
        required=False, 
        min_length=8,
        
        style={'template': 'snippets/input-oldpassword.html', 'input_type': 'password', 'placeholder': 'enter current password'},
       ) #'placeholder': 'enter current password'

    password1 = serializers.CharField(
        required=False, 
        # write_only=True,
        style={'template':'snippets/input-password1.html', 'placeholder': 'enter password'},
    )

    def validate_password(self, password1):
        try:
            validate_password(password1)
        except ValidationError as exc:
            print('serializers.ValidationError(str(exc)):', serializers.ValidationError(str(exc)))
            raise serializers.ValidationError(str(exc))
        return password
    
    password2 = serializers.CharField(
        required=False, 
        min_length=8,
        write_only=True,
        style={'template':'snippets/input-password2.html', 'placeholder': 'confirm password', },
        )

    # remember_me = serializers.BooleanField(
    #     required=False, 
    #     style={'autofocus': True}
    #     )

    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError({"password and repeat password": "Those two passwords don't match."})
        
        elif attrs.get('password1') == attrs.get('password2'):
            print('attrs:', attrs)
            attrs.pop('password2')
            
            return attrs


    class Meta:
        model = Account
        fields = ['current_url','oldpassword', 'password1', 'password2']


        # fields = ('old_password', 'password', 'password2')

class PasswordUpdateSerializerApi(serializers.ModelSerializer):

    # current_url = serializers.CharField(
    # read_only=True, 
    # allow_blank=True, 
    # required=False,
    # style={'template':'snippets/input-hidden.html','input_type': 'text', },
    # )

    oldpassword = serializers.CharField(
        required=False, 
        min_length=8,
        
        style={'template': 'snippets/input-oldpassword.html', 'input_type': 'password', 'placeholder': 'enter current password'},
       ) #'placeholder': 'enter current password'

    password1 = serializers.CharField(
        required=False, 
        # write_only=True,
        style={'template':'snippets/input-password1.html', 'placeholder': 'enter password'},
    )

    def validate_password(self, password1):
        try:
            validate_password(password1)
        except ValidationError as exc:
            print('serializers.ValidationError(str(exc)):', serializers.ValidationError(str(exc)))
            raise serializers.ValidationError(str(exc))
        return password
    
    password2 = serializers.CharField(
        required=False, 
        min_length=8,
        write_only=True,
        style={'template':'snippets/input-password2.html', 'placeholder': 'confirm password', },
        )

    # remember_me = serializers.BooleanField(
    #     required=False, 
    #     style={'autofocus': True}
    #     )

    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError({"password and repeat password": "Those two passwords don't match."})
        
        elif attrs.get('password1') == attrs.get('password2'):
            print('attrs:', attrs)
            attrs.pop('password2')
            
            return attrs


    class Meta:
        model = Account
        fields = ['oldpassword', 'password1', 'password2']

from django.utils.html import format_html
class AccountUpdateSerializer(serializers.ModelSerializer):
    # current_url = serializers.CharField(read_only=True, allow_blank=True, required=False)

    current_url = serializers.CharField(
    read_only=True, 
    allow_blank=True, 
    required=False,
    style={'template':'snippets/input-hidden.html', },
    )

    username = serializers.CharField(
    required=True, 
    # allow_blank=True,
    style={'template': 'snippets/input-username.html', 'placeholder': 'enter new username', },
    validators=[UniqueValidator(queryset=Account.objects.all(),  message="<br>- this username  already exists<br>- this field must be unique")],)
    
    email = serializers.EmailField(
    required=True, 
    style={'template': 'snippets/input-email.html', 'input_type': 'email', 'placeholder': 'enter new email',},
    validators=[UniqueValidator(queryset=Account.objects.all(),message='<br>- this email already exists<br>- this field must be unique' ) ],)

    class Meta:
        model = Account
        fields = ['current_url', 'username', 'email'] # 'current_url', 



    