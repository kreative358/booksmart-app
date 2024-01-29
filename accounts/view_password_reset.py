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
from booksmart.models import context_bm_models
from django.contrib import messages

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