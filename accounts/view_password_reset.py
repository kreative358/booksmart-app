from rest_framework import generics, status, viewsets, response
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from accounts.models import Account 
from accounts.serializer_password_reset import EmailSerializer, ResetPasswordSerializer
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer, HTMLFormRenderer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib import messages
from booksmart.models import Book, Author, BackgroundPoster, BackgroundVideo, BackgroundMusic, url_img, url_img_author#, context_bm_models
import datetime

def context_bm_models():    
    print("views_password_reset context_bm_models()")
    context_bm = {}
    context_list = []

    context_bm['no_date'] = datetime.date(3000, 1, 1)
    context_bm['url_img_book'] = url_img
    context_bm['url_img_author'] = url_img_author

    try:
        if Book.objects.all().count() > 0:
        # if Book.objects.filter().all():
            # all_books = Book.objects.all()
            # context_list.append(all_books)
            num_books = Book.objects.all().count()
            # context_bm['allbooks'] = all_books
            context_bm['num_books'] = num_books
        elif Book.objects.all().count() == 0:
        # elif not Book.objects.filter().all():
            # context_bm['allbooks'] = None
            context_bm['num_books'] = 0
    except Exception as err:
        print(f"booksmart models 335 no Book.objects.all(): except Exception as {err}")
        context_bm['allbooks'] = None
        context_bm['num_books'] = 0  

    try:
        if Author.objects.all().count() > 0:
        # if Author.objects.filter().all():
            # all_authors = Author.objects.all()
            # context_list.append(all_authors)
            num_authors = Author.objects.all().count()
            # context_bm['allauthors'] = all_authors
            context_bm['num_authors'] = num_authors
        elif Author.objects.all() == 0:
        #elif not Author.objects.filter().all():
            # context_bm['allauthors'] = None
            context_bm['num_authors'] = 0
    except Exception as err:
        print(f"booksmart models 351 no Author.objects.all(): Exception as {err}")
        context_bm['allauthors'] = None
        context_bm['num_authors'] = 0

    try:
        if BackgroundPoster.objects.filter().last():
            poster = BackgroundPoster.objects.filter().last()
            context_bm['poster_url_1'] = poster.link_poster_1
            context_bm['poster_url_2'] = poster.link_poster_2
        elif not BackgroundPoster.objects.filter().last():
            context_bm['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
            context_bm['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
    except Exception as err:
        print(f"booksmart models 367 no BackgroundPoster.objects.filter().last(): Exception as {err}")
        context_bm['poster_url_1'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"
        context_bm['poster_url_2'] = "https://drive.google.com/uc?export=download&id=1eFl5af7eimuPVop8W1eAUr4cCmVLn8Kt"

    try:
        if BackgroundVideo.objects.filter().last():   
            video = BackgroundVideo.objects.filter().last()
            context_bm['video_url'] = video.link_video
            context_bm['video_type'] = video.type_video
        elif not BackgroundVideo.objects.filter().last():
            context_bm['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
            context_bm['video_type'] = "mp4"
    except Exception as err:
        print(f"booksmart models no BackgroundVideo.objects.filter().last(): Exception as {err}")
        context_bm['video_url'] = "https://drive.google.com/uc?export=download&id=1iRN8nKryM2FKAltnuOq1Qk8MUM-hrq2U"
        context_bm['video_type'] = "mp4"

    try:
        if BackgroundMusic.objects.filter().last():   
            music = BackgroundMusic.objects.filter().last()
            context_bm['music_url_1'] = music.link_music_1
            context_bm['music_type_1'] = music.type_music_1
            context_bm['music_url_2'] = music.link_music_2
            context_bm['music_type_2'] = music.type_music_2
        elif not BackgroundMusic.objects.filter().last(): 
            context_bm['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
            context_bm['music_type_1'] = "mp3"
            context_bm['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
            context_bm['music_type_2'] = "mp3"
    except Exception as err:
        print(f"booksmart models 400 BackgroundMusic.objects.filter().last(): except Exception as {err}")    
        context_bm['music_url_1'] = "https://www.orangefreesounds.com/wp-content/uploads/2022/02/Relaxing-white-noise-ocean-waves.mp3"
        context_bm['music_type_1'] = "mp3"
        context_bm['music_url_2'] = "https://orangefreesounds.com/wp-content/uploads/2022/05/Piano-lullaby.mp3"
        context_bm['music_type_2'] = "mp3"
    
    context_bm_models.context_bm = context_bm
    # context_bm = context_bm_models.copy()
    return context_bm

class SerializerPasswordReset(APIView):
    """
    Request for Password Reset Link.
    """
    renderer_classes = [TemplateHTMLRenderer, HTMLFormRenderer]
    permission_classes = [AllowAny,]
    template_name="password_reset_new.html"
    style = {'template_pack': 'rest_framework/vertical/'} #
    # serializer_class = serializers.EmailSerializer
    serializer_class = EmailSerializer
    # context_serializer = context_bm_models.context_bm

    def get(self, request, *args, **kwargs):
        context_bm_models()
        context_serializer_get = context_bm_models.context_bm
        messages.info(request, "")
        serializer = self.serializer_class()
        # return Response({'serializer':serializer, 'style':self.style}, )
        # context_serializer_get = {'serializer':serializer, 'style':self.style, 'num_authors': context_bm_rest['num_authors'], 'poster_url_1': context_bm_rest['poster_url_1'], 'poster_url_2': context_bm_rest['poster_url_2'], 'video_url': context_bm_rest['video_url'], 'video_type': context_bm_rest['video_type'], 'music_url_1': context_bm_rest['music_url_1'], 'music_type_1': context_bm_rest['music_type_1'], 'music_url_2': context_bm_rest['music_url_2'], 'music_type_2': context_bm_rest['music_type_2']}
        # context_serializer_get = self.context_serializer

        return Response(context_serializer_get, )

    def post(self, request):
        """
        Create token.
        """
        initial_val = serializer.initial_data
        pass1_val = initial_val['password']
        pass2_val = initial_val['password2']
        oldpass_val = 'no_oldpass'
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = Account.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "password_reset_new",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )

            reset_link = f"localhost:8000{reset_url}"
            # reset_link = f'https://booksmart-app-bd32a8932ff0.herokuapp.com/{template_name}'
            # send the rest_link as mail to the user.

            return response.Response(
                {
                    "message": 
                    f"Your password reset link: {reset_link}"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SerializerResetPasswordAPI(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """

    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return response.Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )