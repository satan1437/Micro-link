from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.db import DatabaseError
from django.db.models.query import QuerySet
from django.forms import Form
from django.shortcuts import redirect

from links.forms import UserRegisterForm, UserLoginForm
from links.models import Link


def create_short_url(form: Form, request: WSGIRequest) -> redirect:
	"""Записывает URL в БД и перенаправляет на домашнюю страницу"""
	try:
		form_url = form.cleaned_data.get('url')
		url = Link(url=form_url)
		url.owner = request.user
		url.save()
		messages.success(request, f'Короткая ссылка успешно создана! {url.shorted_url}')
	except DatabaseError:
		messages.error(request, f'При создании ссылки произошла ошибка!')
	finally:
		return redirect('home')


def link_handler(hash_: str) -> redirect:
	"""Проверяет наличие ссылки и перенаправляет"""
	try:
		link = Link.objects.get(url_hash=hash_)
		link.redirection += 1
		link.save()
		return redirect(link.url)
	except ObjectDoesNotExist:
		return redirect('home')


def create_new_user(form: UserRegisterForm, request: WSGIRequest) -> redirect:
	"""Создаёт нового пользователя и перенаправляет на домашнюю страницу"""
	try:
		user = form.save()
		login(request, user)
		messages.success(request, 'Вы успешно зарегистрировались!')
	except DatabaseError:
		messages.error(request, 'Ошибка регистрации!')
	finally:
		return redirect('home')


def login_handler(form: UserLoginForm, request: WSGIRequest) -> redirect:
	"""Авторизирует пользователя и перенаправляет на домашнюю страницу"""
	user = form.get_user()
	login(request, user)
	messages.success(request, 'Вы успешно вошли!')
	return redirect('home')


def get_user_all_links(request: WSGIRequest) -> QuerySet:
	"""Возвращает все ссылки пользователя"""
	return User.objects.get(username=request.user).all_links.all()
