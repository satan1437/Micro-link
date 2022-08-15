from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.db import DatabaseError
from django.db.models.query import QuerySet
from django.forms import Form
from django.shortcuts import redirect

from links.models import Link


def create_short_url(form: Form, request: WSGIRequest) -> redirect:
	"""Writes URL to database"""
	try:
		form_url = form.cleaned_data.get('url')
		url = Link(url=form_url)
		url.owner = request.user
		url.save()
		messages.success(request, f'Короткая ссылка успешно создана! {url.shorted_url}')
	except DatabaseError:
		messages.error(request, 'При создании ссылки произошла ошибка!')
	finally:
		return redirect('home')


def link_handler(hash_: str, request: WSGIRequest) -> redirect:
	"""Checks for a link"""
	link = None
	try:
		link = Link.objects.get(url_hash=hash_)
		link.redirection += 1
		link.save()
	except ObjectDoesNotExist:
		messages.error(request, 'Запрашиваемой короткой ссылки не найдено!')
	finally:
		if link:
			return redirect(link.url)
		return redirect('home')


def get_all_user_links(request: WSGIRequest) -> QuerySet:
	"""Returns all user links"""
	return User.objects.get(username=request.user).all_links.all()
