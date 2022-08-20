from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import CustomUser


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
			'placeholder': 'Повтор пароля'
		}))

	class Meta:
		model = CustomUser
		fields = ('email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Email',
	}))
	password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
		'class': 'form-control',
		'placeholder': 'Пароль',
	}))
