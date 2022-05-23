from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class UserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')


class BookForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Book
        fields = ('name', 'book_country', 'book_description', 'publishing_house', 'author_name', 'book_img')