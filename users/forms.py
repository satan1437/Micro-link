from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, \
	SetPasswordForm

from .models import CustomUser
from .services import get_reset_password_email_body


class CustomUserCreationAdminForm(UserCreationForm):
	class Meta:
		model = CustomUser
		fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ('email',)


class CustomUserCreationForm(UserCreationForm):
	email = forms.CharField(
		label='',
		widget=forms.TextInput(attrs={
			'class': 'form-control',
			'autocomplete': 'off',
			'placeholder': 'Email',
		}))
	password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
		'class': 'form-control',
		'placeholder': 'Пароль',
	}))
	password2 = forms.CharField(
		label='',
		help_text='Ваш пароль должен содержать как минимум 8 символов.',
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': 'Повтор пароля',
		}))

	class Meta:
		model = CustomUser
		fields = ['email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Email',
	}))
	password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
		'class': 'form-control',
		'placeholder': 'Пароль',
	}))


class UserPasswordChangeForm(PasswordChangeForm):
	old_password = forms.CharField(
		label='',
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': 'Старый пароль',
		}))
	new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
		'class': 'form-control',
		'placeholder': 'Пароль',
	}))
	new_password2 = forms.CharField(
		label='',
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': 'Повтор пароля',
		}))


class CustomPasswordResetForm(forms.Form):
	email = forms.EmailField(
		max_length=254,
		widget=forms.EmailInput(attrs={
			'class': 'form-control',
			'placeholder': 'Email',
		}))

	def save(self, *args, **kwargs):
		email = self.cleaned_data["email"]
		get_reset_password_email_body(email)


class CustomSetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
	)
	new_password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
	)
