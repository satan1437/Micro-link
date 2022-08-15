import base64
import uuid

from django.conf import settings

from links.models import Link


def create_url(instance: Link) -> None:
	"""Writes hash and url to instance"""
	url_hash = generate_hash()
	shorted_url = create_short_url(url_hash)
	instance.url_hash = url_hash
	instance.shorted_url = shorted_url


def generate_hash() -> str:
	"""Generates hash link"""
	new_hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:10]
	is_valid_hash = Link.objects.filter(url_hash=new_hash)
	while is_valid_hash:
		new_hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:10]
		is_valid_hash = Link.objects.filter(url_hash=new_hash)
	complete_hash = new_hash.decode('utf-8')
	return complete_hash


def create_short_url(url_hash: str) -> str:
	"""Creates a new valid link"""
	return f'https://{settings.ALLOWED_HOSTS[0]}/{url_hash}'
