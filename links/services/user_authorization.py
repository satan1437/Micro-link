from django.contrib import messages
from django.contrib.auth import login
from django.core.handlers.wsgi import WSGIRequest
from django.db import DatabaseError
from django.shortcuts import redirect

from links.forms import UserRegisterForm, UserLoginForm


def create_new_user(form: UserRegisterForm, request: WSGIRequest) -> redirect:
	"""Creates a new user and authorizes"""
	try:
		user = form.save()
		login(request, user)
		messages.success(request, 'Вы успешно зарегистрировались!')
	except DatabaseError:
		messages.error(request, 'Ошибка регистрации!')
	finally:
		return redirect('home')


def login_handler(form: UserLoginForm, request: WSGIRequest) -> redirect:
	"""Authorizes user"""
	user = form.get_user()
	login(request, user)
	messages.success(request, 'Вы успешно вошли!')
	return redirect('home')
