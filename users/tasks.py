from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail as send

from config.celery import app


@app.task
def send_mail(
		subject: str,
		body: str,
		recipient_list: str | list,
		from_email: str = settings.EMAIL_HOST_USER) -> dict:
	try:
		send(subject, body, from_email, [recipient_list])
	except SMTPException as ex:
		subject = subject.encode('utf-8')
		return {'Exeption': ex, subject: recipient_list}
	return {subject: recipient_list}
