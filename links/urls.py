from django.urls import path, re_path

from .views import HomeView, UserLinksView, LinkRedirectView

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('links/', UserLinksView.as_view(), name='links'),
	re_path(r'^(?P<hash_>.+)$', LinkRedirectView.as_view()),
]
