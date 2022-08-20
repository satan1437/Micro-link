from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, UserLoginForm


class UserRegistrationView(SuccessMessageMixin, CreateView):
	form_class = CustomUserCreationForm
	template_name = 'users/register.html'
	success_url = reverse_lazy('home')
	success_message = 'Вы успешно зарегистрировались!'

	def form_valid(self, form):
		form_valid = super().form_valid(form)
		login(self.request, self.object)
		return form_valid


class UserLoginView(LoginView):
	form_class = UserLoginForm
	template_name = 'users/login.html'
	redirect_authenticated_user = True
