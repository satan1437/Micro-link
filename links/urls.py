from django.urls import path, re_path

from .views import index, user_registration, user_login, user_logout, user_links, link_redirect

urlpatterns = [
	path('', index, name='home'),
	path('register/', user_registration, name='register'),
	path('login/', user_login, name='login'),
	path('logout/', user_logout, name='logout'),
	path('links/', user_links, name='links'),
	re_path(r'^(?P<hash_>.+)$', link_redirect),
]
