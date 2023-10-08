from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from accounts.models import Account


class EmailSerializer(serializers.Serializer):
    """
    Reset Password Email Request Serializer.
    """

    email = serializers.EmailField(
        required=False, 
        #allow_blank=True,
        style={'template':'snippets/input-email.html', 'placeholder': 'enter email'},
        validators=[UniqueValidator(queryset=Account.objects.all(), message='this email already exists, this field must be unique' ) ],
        # validators=[UniqueValidator(queryset=Account.objects.all())],
        # error_messages ={'email':"This email already exists."}
    )

    class Meta:
        model = Account
        fields = ['email']



class ResetPasswordSerializer(serializers.Serializer):
# class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    Reset Password Serializer.
    """

    password = serializers.CharField(
        required=False, 
        # write_only=True,
        style={'template':'snippets/input-password.html', 'placeholder': 'enter password'},
    )

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")
        try:
            if token is None or encoded_pk is None:
                raise serializers.ValidationError("Missing data.")

            pk = urlsafe_base64_decode(encoded_pk).decode()
            user = User.objects.get(pk=pk)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("The reset token is invalid")

            user.set_password(password)
            user.save()
            return data    
        except ValidationError as exc:
            print('serializers.ValidationError(str(exc)):', serializers.ValidationError(str(exc)))
            raise serializers.ValidationError(str(exc))

    class Meta:
        # model = Account
        fields = ['password']
        # fields = ['password', 'password2']

    # def validate(self, data):
    #     """
    #     Verify token and encoded_pk and then set new password.
    #     """
    #     password = data.get("password")
    #     token = self.context.get("kwargs").get("token")
    #     encoded_pk = self.context.get("kwargs").get("encoded_pk")

    #     if token is None or encoded_pk is None:
    #         raise serializers.ValidationError("Missing data.")

    #     pk = urlsafe_base64_decode(encoded_pk).decode()
    #     user = User.objects.get(pk=pk)
    #     if not PasswordResetTokenGenerator().check_token(user, token):
    #         raise serializers.ValidationError("The reset token is invalid")

    #     user.set_password(password)
    #     user.save()
    #     return data