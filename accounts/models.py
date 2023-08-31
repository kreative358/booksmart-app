from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AnonymousUser
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# from booksmart.models import *

# from browserapi.models import ActivityLog
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django.contrib.auth.models import AnonymousUser

# def get_user(request):
#     user=request.user
#     if user.is_authenicated:
#         get_id = {}
#         print('accounts.models user.id:', user.id)
#         get_id['user_id']=user.id
#         print(" accounts.models get_id['user_id']", get_id['user_id'])
#         userid = get_id['user_id']
#         print('accounts.models userid', userid)
#         return userid
#     else:
#         print('accounts.models None')
#         return None


# get_user_id = get_user
# print('accounts.models get_user_id', get_user_id)

# class MyAccountManager(BaseUserManager):

#     def create_user(self, email, username, password=None):
#         if not username:
#             raise ValueError('Users must have a username')
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#         username=username,
#         email=self.normalize_email(email),
# 		)

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#         username=username,
#         email=self.normalize_email(email),
#         password=password,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

class MyAccountManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, ' ', **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

# class Account(AbstractBaseUser):
class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    # position = [
    #     (1, 'superuser'),
    #     (2, 'admin'),
    #     (3, 'manager'),
    #     (4, 'employee'),
    # ]

    # staff_position = models.CharField(max_length=24, choices=position, editable=False, default='employee' )
    
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)

    # owner_book = GenericRelation(Book)
    # owner_author = GenericRelation(Author)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    objects = MyAccountManager()

    class Meta:
        ordering=['id']

    def __str__(self):
        # return f"{self.username} - {self.staff_position}"
        return self.username 

    # For checking permissions. to keep it simple all admin have ALL permissons
    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    # # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    # def has_module_perms(self, app_label):
    #     return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# class OwnerRecords(models.Model):
#     owner_record = ForeignKey(
#         Account, default=None, null=True, on_delete=models.SET_NULL, related_name='owner-record')
#     owner_book = GenericRelation(Book, related_query_name='owner-book')
#     owner_author = GenericRelation(Author, related_query_name='owner-author')
#     # activity_logs = GenericRelation(ActivityLog ,content_type_field='content_type',
#     #     object_id_field='object_id', related_query_name='reader')


#     # Other fields