from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (
	UserLoginView, UserRegistrationView, UserVerifyEmailView, UserProfileView, UserRestoreView,
	UserPasswordResetView
)

urlpatterns = [
	#  Core
	path('profile/', UserProfileView.as_view(), name='profile'),

	# Authentication
	path('login/', UserLoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('register/', UserRegistrationView.as_view(), name='register'),

	# Restore/Confirm
	path('restore/', UserRestoreView.as_view(), name='restore'),
	path('verify_email/<uidb64>/<token>/', UserVerifyEmailView.as_view(), name='verify_email'),
	path('reset_password/<uidb64>/<token>/', UserPasswordResetView.as_view(), name='reset_password'),
]
