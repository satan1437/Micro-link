from django.contrib import admin

from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
	list_display = ('owner', 'url', 'shorted_url', 'redirection', 'date')
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
	readonly_fields = ('owner', 'redirection', 'shorted_url', 'date')
