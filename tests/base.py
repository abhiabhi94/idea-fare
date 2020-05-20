import os
import random
from string import ascii_lowercase
import sys

from django.contrib.auth import get_user_model
from django.test import TestCase

from ideas.models import Idea

User = get_user_model()

class TestBase(TestCase):

    def get_unique_email(self):
        """
        Get a valid email

        Args:
            unique (bool, optional): If a unique email is required. Defaults to False.

        Returns:
            str
        """
        email = self.get_email()
        email_username, domain = email.split('@')
        # this will only work for Gmail, not tested for other domains
        letters = ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(5))
        return f'{email_username}+{random_string}@{domain}'

    def setUp(self):
        """Set the environment variable to disable RECAPTCHA"""
        os.environ['RECAPTCHA_DISABLE'] = 'True'

    @staticmethod
    def get_email():
        """
        Get email set as an environment variable

        Returns:
            str
        """
        variable = 'VALID_EMAIL'
        email = os.getenv(variable)
        if not email:
            sys.exit(f'Please set an environment variable {variable} as a valid email. It will be used for testing.')
        return email.strip().lower()

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize all global testing data here."""
        super().setUpClass()
        cls.email = cls.get_email()
        cls.user_data = {
            'username': 'tester',
            'email': cls.email,
            'password': 'user123#',
            'first_name': 'Jach',
            'last_name': 'Karta'
        }
        cls.user = User.objects.create(**cls.user_data)
        cls.ideas = 0

    @classmethod
    def create_user(cls, *args, **kwargs) -> User:
        return User.objects.create(*args, **kwargs)

    @classmethod
    def create_idea(cls, title:str, concept:str, user: User = None, *args, **kwargs) -> Idea:
        cls.ideas += 1
        return Idea.objects.create(
            title=title,
            concept=concept,
            user=user,
            *args, **kwargs
        )


class TestBaseView(TestBase):
    def setUp(self) -> None:
        """Log in the user"""
        super().setUp()
        self.client.force_login(self.user)
