import os

from django.contrib.auth import get_user_model
from django.test import TestCase

from ideas.models import Idea

User = get_user_model()

class TestBase(TestCase):

    def setUp(self):
        """Set the environment variable to disable RECAPTCHA"""
        os.environ['RECAPTCHA_DISABLE'] = 'True'

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize all global testing data here."""
        super().setUpClass()

        cls.valid_email_string = os.environ.get('VALID_EMAILS', None)
        if cls.valid_email_string is not None:
            cls.valid_emails = cls.valid_email_string.lower().split()

        cls.user_data = {
            'username': 'tester',
            'email': cls.valid_emails[0],
            'password':'user123#',
            'first_name':'Jach',
            'last_name':'Karta'
        }
        cls.user = User.objects.create(**cls.user_data)
        cls.ideas = 0

    def get_valid_emails():
        valid_email_string = os.environ.get('VALID_EMAILS', None)
        if valid_email_string is not None:
            return valid_email_string.lower().split()

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
