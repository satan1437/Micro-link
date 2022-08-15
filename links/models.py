from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class Link(models.Model):
	"""Short link"""
	url = models.URLField('Оригинальный URL')
	url_hash = models.CharField('Хэш', max_length=10, unique=True, db_index=True)
	shorted_url = models.URLField('Сокращённый URL', blank=True, null=True)
	redirection = models.IntegerField('Переходов', default=0)
	date = models.DateTimeField('Дата создания', auto_now_add=True)
	owner = models.ForeignKey(
		to=get_user_model(), on_delete=models.CASCADE, verbose_name='Создатель ссылки',
		related_name='all_links')

	def __str__(self):
		return f'ID {self.id} | Пользователь: {self.owner}'

	class Meta:
		verbose_name = 'Ссылку'
		verbose_name_plural = 'Ссылки'
		ordering = ['-date']
		db_table = 'link'
