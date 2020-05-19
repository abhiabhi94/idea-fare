from django.test import TestCase
from django.contrib.auth import get_user_model

from ideas.models import Idea

User = get_user_model()

class TestBase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize all global testing data here."""
        super().setUpClass()
        cls.user_data = {
            'username': 'tester',
            'email':'jach.karta@gmail.com',
            'password':'user123#',
            'first_name':'Jach',
            'last_name':'Karta'
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
        self.client.force_login(self.user)




