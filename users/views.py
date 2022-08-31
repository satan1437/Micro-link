from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import (
	CustomUserCreationForm, UserLoginForm, UserPasswordChangeForm, CustomPasswordResetForm,
	CustomSetPasswordForm
)
from .models import CustomUser
from .services import verify_user_token, get_verify_email_body


class UserProfileView(SuccessMessageMixin, PasswordChangeView):
	"""User Profile"""
	form_class = UserPasswordChangeForm
	template_name = 'users/profile.html'
	success_url = reverse_lazy('home')
	success_message = 'Пароль успешно изменен!'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['user'] = get_object_or_404(CustomUser, pk=self.request.user.pk)
		context['all_redirects'] = CustomUser.objects.get(pk=1).all_links.aggregate(Sum('redirection'))
		context['all_links'] = CustomUser.objects.get(pk=1).all_links.count()
		return context


class UserRegistrationView(SuccessMessageMixin, CreateView):
	"""Registration page"""
	form_class = CustomUserCreationForm
	template_name = 'users/registration.html'
	success_url = reverse_lazy('home')
	success_message = 'Вы успешно зарегистрировались!'

	def form_valid(self, form):
		form_valid = super().form_valid(form)
		login(self.request, self.object)
		get_verify_email_body(self.request.user)
		return form_valid


class UserVerifyEmailView(View):
	"""Email verification system"""

	def get(self, request, uidb64, token):
		if verify_user_token(uidb64, token):
			messages.success(self.request, f'Ваш Email успешно подтверждён!')
		else:
			messages.error(self.request, f'Ваша ссылка подтверждения недействительна!')
		return redirect('home')


class UserLoginView(LoginView):
	"""Authentication page"""
	form_class = UserLoginForm
	template_name = 'users/login.html'
	redirect_authenticated_user = True


class UserRestoreView(SuccessMessageMixin, PasswordResetView):
	"""Password reset page"""
	form_class = CustomPasswordResetForm
	template_name = 'users/restore.html'
	email_template_name = 'users/email/reset_password.html'
	success_url = reverse_lazy('home')
	success_message = 'Письмо с ссылкой для изменения пароля успешно отправлено!'


class UserPasswordResetView(SuccessMessageMixin, PasswordResetConfirmView):
	"""Page for entering a new password"""
	form_class = CustomSetPasswordForm
	template_name = 'users/reset_password.html'
	success_url = reverse_lazy('login')
	success_message = 'Пароль успешно изменён!'
