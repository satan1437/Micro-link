from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, RedirectView, FormView

from links.services.link_manager import create_short_url, link_handler, get_all_user_links
from .forms import LinkForm


class HomeView(FormView):
	form_class = LinkForm
	template_name = 'micro-linker/index.html'
	success_url = '/'

	def form_valid(self, form):
		return create_short_url(self.request, form)


class LinkRedirectView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		return link_handler(self.request, kwargs['hash_'])


class UserLinksView(LoginRequiredMixin, ListView):
	login_url = '/users/login/'
	paginate_by = 19
	template_name = 'micro-linker/links.html'
	context_object_name = 'links'

	def get_queryset(self):
		return get_all_user_links(self.request)
