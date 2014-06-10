from django.forms import ModelForm
from projects.models import UserProfile
from django.contrib.auth.models import User

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['gender', 'birthdate']

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name']