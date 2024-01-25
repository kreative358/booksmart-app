from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Account


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = Account
		#fields = ('username', 'email', 'password1', 'password2', )
		fields = ('username', 'email', 'password', 'password2', )

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			# raise forms.ValidationError('Username is updated succes')
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)	

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('username', 'password')

	def clean(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']
			if not authenticate(username=username, password=password):
				raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('username', 'email')

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)
	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)


class AccountDeleteForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = "__all__"

class RechaptchaForm(forms.Form):
	# recaptcha_token = forms.CharField(widget=forms.HiddenInput())
	recaptcha_token = forms.CharField(widget=forms.Textarea(attrs={'id': 'textarea_recaptcha', 'rows': 4}))

class RechaptchaMailForm(forms.Form):
	# recaptcha_token = forms.CharField(widget=forms.HiddenInput())
	recaptcha_mail_token = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'id': 'recaptcha_mail_token_id', 'style':'display: none'}))

# class CharField(max_length: Optional[Any]=..., min_length: Optional[Any]=..., strip: bool=..., empty_value: Optional[str]=..., required: bool=..., widget: Optional[Union[Widget, Type[Widget]]]=..., label: Optional[Any]=..., initial: Optional[Any]=..., help_text: str=..., error_messages: Optional[Any]=..., show_hidden_initial: bool=..., validators: Sequence[Any]=..., localize: bool=..., disabled: bool=..., label_suffix: Optional[Any]=...)



