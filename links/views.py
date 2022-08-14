from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import LinkForm, UserRegisterForm, UserLoginForm
from .services import create_short_url, link_handler, create_new_user, login_handler, get_user_all_links


def index(request):
	if request.method == 'POST':
		form = LinkForm(request.POST)
		if form.is_valid():
			return create_short_url(form=form, request=request)
	else:
		form = LinkForm()
	return render(request, 'micro-linker/index.html', {'form': form})


def link_redirect(request, hash_):
	return link_handler(hash_=hash_)


def user_registration(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			return create_new_user(form=form, request=request)
	else:
		form = UserRegisterForm()
	return render(request, 'micro-linker/register.html', {'form': form})


def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			return login_handler(form=form, request=request)
		else:
			messages.error(request, 'Ошибка входа!')
	else:
		form = UserLoginForm()
	return render(request, 'micro-linker/login.html', {'form': form})


def user_logout(request):
	logout(request)
	return redirect('login')


@login_required
def user_links(request):
	links = get_user_all_links(request=request)
	paginator = Paginator(links, 19)
	page_number = request.GET.get('page', 1)
	page_obj = paginator.get_page(page_number)
	return render(request, 'micro-linker/links.html', {'page_obj': page_obj})
