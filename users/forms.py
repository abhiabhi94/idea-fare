from django import forms
from django.contrib.auth.forms import User, UserCreationForm

from ideas.manager import email_verification
from ideas.mixins import CleanUserDetailsMixin


class UserRegisterForm(UserCreationForm, CleanUserDetailsMixin):
    """
    Register a user by extending the User model with the following information:
        First Name
        Last Name(optional)-> not all people have a last name
        Email
    """
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm, CleanUserDetailsMixin):
    """Allows users to update their personal information"""
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
