from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from library.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required. Add a valid email adress")

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")  # ()
