from django.contrib import admin

from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
	list_display = ('owner', 'short_origin_url', 'shorted_url', 'redirection', 'date')
	list_filter = ('date',)
	search_fields = ('owner__username', 'url', 'date')
	search_help_text = 'Поиск осуществляется по Никнейму, URL и Дате.'
	fieldsets = (
		(
			'Информация',
			{
				'fields': ('owner', 'redirection', 'date')
			}
		),
		('URL', {
			'fields': ('url', 'shorted_url')
		})
	)
	readonly_fields = ('redirection', 'shorted_url', 'date')

	@admin.display(description='url')
	def short_origin_url(self, obj):
		if len(obj.url) >= 50:
			return f'{obj.url[:50]}...'
		return obj.url
