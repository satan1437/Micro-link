import base64
import uuid

from django.conf import settings

from links.models import Link


def generate_hash() -> str:
	"""Generates hash link"""
	new_hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:10]
	is_valid_hash = Link.objects.filter(url_hash=new_hash)
	while is_valid_hash:
		new_hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:10]
		is_valid_hash = Link.objects.filter(url_hash=new_hash)
	complete_hash = new_hash.decode('utf-8')
	return complete_hash


def create_valid_url(url_hash: str) -> str:
	"""Creates a new valid link"""
	return f'https://{settings.ALLOWED_HOSTS[0]}/{url_hash}'
