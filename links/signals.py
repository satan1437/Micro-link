from django.db.models.signals import pre_save
from django.dispatch import receiver

from links.models import Link
from links.services.pre_create_url import create_url


@receiver(pre_save, sender=Link)
def create_short_url(instance: Link, **kwargs) -> None:
	if not instance.shorted_url:
		create_url(instance)
