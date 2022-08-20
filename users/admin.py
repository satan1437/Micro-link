from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.forms import CustomUserChangeForm, CustomUserCreationAdminForm
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationAdminForm
	form = CustomUserChangeForm
	model = CustomUser

	list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
	fieldsets = (
		(None, {"fields": ("email", "password")}),
		(_("Personal info"), {"fields": ("first_name", "last_name")}),
		(
			_("Permissions"),
			{
				"fields": (
					"is_active",
					"is_staff",
					"is_superuser",
					"groups",
					"user_permissions",
				),
			},
		),
		(_("Important dates"), {"fields": ("last_login", "date_joined")}),
	)
	add_fieldsets = (
		(
			None,
			{
				"classes": ("wide",),
				"fields": ("username", "password1", "password2"),
			},
		),
	)
