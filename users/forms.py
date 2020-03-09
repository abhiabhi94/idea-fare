from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ideas.manager import email_verification


class UserRegisterForm(UserCreationForm):
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

    def clean_username(self):
        """Return username in lower case"""
        return self.cleaned_data.get('username').lower()

    def clean_email(self):
        """
        Returns
            email address in lower case if email is unique
            error message in case it isn't.
        """
        email = self.cleaned_data.get('email').lower()
        username = self.cleaned_data.get('username').lower()
        if email_verification(email):
            return forms.ValidationError(
                f'Are you sure this is a valid email address? We suspect you made a typing error')

        elif email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(
                f'This email address is already associated with another account.')
        return email

    def clean_first_name(self):
        """Verify whether the input is a valid alphabetic"""
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError(
                f'Are you sure that is a valid name. Names can only have alphabets')
        return first_name

    def clean_last_name(self):
        """Verify whether the input is alphabetic when there's one"""
        last_name = self.cleaned_data.get('last_name')
        if last_name and not last_name.isalpha():
            raise forms.ValidationError(
                f'Are you sure that is a valid name. Names can only have alphabets')
        return last_name


class UserUpdateForm(forms.ModelForm):
    """Allows users to update their personal information"""
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        """Return username in lower case"""
        return self.cleaned_data.get('username').lower()

    def clean_email(self):
        """
        Returns
            email address in lower case if email is unique
            error message in case it isn't.
        """
        email = self.cleaned_data.get('email').lower()
        username = self.cleaned_data.get('username').lower()
        if email_verification(email):
            return forms.ValidationError(
                f'Are you sure this is a valid email address? We suspect you made a typing error')

        elif email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(
                f'This email address is already associated with another account.')
        return email

    def clean_first_name(self):
        """Verify whether the input is a valid alphabetic"""
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError(
                f'Are you sure that is a valid name. Names can only have alphabets')
        return first_name

    def clean_last_name(self):
        """Verify whether the input is alphabetic when there's one"""
        last_name = self.cleaned_data.get('last_name')
        if last_name and not last_name.isalpha():
            raise forms.ValidationError(
                f'Are you sure that is a valid name. Names can only have alphabets')
        return last_name
