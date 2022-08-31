from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.db import DatabaseError
from django.db.models.query import QuerySet
from django.forms import Form
from django.shortcuts import redirect
from django.urls import reverse

from links.models import Link
from users.models import CustomUser


def create_short_url(request: WSGIRequest, form: Form) -> redirect:
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


def link_handler(request: WSGIRequest, hash_: str) -> redirect:
	"""Checks for a link"""
	try:
		link = Link.objects.get(url_hash=hash_)
		link.redirection += 1
		link.save()
		return link.url
	except ObjectDoesNotExist:
		messages.error(request, 'Запрашиваемой короткой ссылки не найдено!')
		return reverse('home')


def get_all_user_links(request: WSGIRequest) -> QuerySet:
	"""Returns all user links"""
	return CustomUser.objects.get(pk=request.user.pk).all_links.all()
