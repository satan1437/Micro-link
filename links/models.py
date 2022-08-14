import base64
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Link(models.Model):
	"""Сокращение ссылки"""
	url = models.URLField('Оригинальный URL')
	url_hash = models.CharField('Хэш', max_length=10, unique=True, db_index=True, editable=False)
	shorted_url = models.URLField('Сокращённый URL', blank=True, null=True)
	redirection = models.IntegerField('Переходов', default=0)
	date = models.DateTimeField('Дата создания', auto_now_add=True)
	owner = models.ForeignKey(
		to=User, on_delete=models.CASCADE, verbose_name='Создатель ссылки',
		related_name='all_links')

	def save(self, *args, **kwargs):
		if not self.url_hash:
			self.url_hash = self.generate_hash()
			self.shorted_url = self.create_short_url()
		super(Link, self).save(*args, **kwargs)

	@staticmethod
	def generate_hash():
		"""Генерирует хэш для ссылки"""
		new_hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:10]
		is_valid_hash = Link.objects.filter(url_hash=new_hash)
		while is_valid_hash:
			new_hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:10]
			is_valid_hash = Link.objects.filter(url_hash=new_hash)
		complete_hash = new_hash.decode('utf-8')
		return complete_hash

	def create_short_url(self):
		"""Создаёт валидную сокращённую ссылку"""
		return 'https://' + settings.ALLOWED_HOSTS[0] + '/' + self.url_hash

	def __str__(self):
		return f'ID {self.id} | Пользователь: {self.owner}'

	class Meta:
		verbose_name = 'Ссылку'
		verbose_name_plural = 'Ссылки'
		ordering = ['-date']
		db_table = 'link'
