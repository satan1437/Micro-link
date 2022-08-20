from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):

	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError("The given email must be set")
		email = self.normalize_email(email)

		user = self.model(email=email, **extra_fields)
		user.password = make_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)

		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")
		return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
	username = models.CharField('Никнейм', max_length=256, blank=True, null=True)
	email = models.EmailField('Email', unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = CustomUserManager()

	def __str__(self):
		return f'{self.pk} | {self.email}'

	class Meta:
		verbose_name = 'Пользователя'
		verbose_name_plural = 'Пользователи'
		db_table = 'users'
		ordering = ['-date_joined']
