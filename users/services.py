from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import CustomUser
from .tasks import send_mail


def create_verify_context(user: User) -> dict:
	"""Returns the personal UID and Token"""
	context = {
		'domain': settings.ALLOWED_HOSTS[-1],  # :(
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': default_token_generator.make_token(user),
	}
	return context


def get_verify_email_body(user: User) -> send_mail:
	"""Sends a confirmation letter"""
	context = create_verify_context(user)
	title = 'Micro-link - Подтверждение почты'
	message = render_to_string('users/email/verify_email.html', context=context)
	send_mail.delay(title, message, user.email)


def get_reset_password_email_body(email: str) -> send_mail:
	"""Sends an email to change the password"""
	try:
		user = CustomUser.objects.get(email=email)
	except ObjectDoesNotExist:
		return
	context = create_verify_context(user)
	title = 'Micro-link - Сброс пароля'
	message = render_to_string('users/email/reset_password.html', context=context)
	send_mail.delay(title, message, email)


def verify_user_token(uidb64: str, token: str) -> bool:
	"""Activates the user account"""
	user = _get_user(uidb64)
	check_token = default_token_generator.check_token(user, token)
	if user is not None and check_token:
		user.is_verified = True
		user.save()
		return True
	return False


def _get_user(uidb64: str) -> CustomUser | None:
	"""Finds a user by token"""
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = CustomUser.objects.get(pk=uid)
	except (
			TypeError,
			ValueError,
			OverflowError,
			CustomUser.DoesNotExist,
			ValidationError,
	):
		user = None
	return user
