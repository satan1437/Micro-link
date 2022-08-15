from django.db.models.signals import pre_save
from django.dispatch import receiver

from links.models import Link
from links.services.pre_create_url import generate_hash, create_valid_url


@receiver(pre_save, sender=Link)
def create_short_url(instance: Link, **kwargs) -> None:
	if not instance.shorted_url:
		url_hash = generate_hash()
		shorted_url = create_valid_url(url_hash)
		instance.url_hash = url_hash
		instance.shorted_url = shorted_url
