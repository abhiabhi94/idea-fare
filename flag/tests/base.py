import json

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, RequestFactory, TestCase

from flag.models import Flag, FlagInstance
from ideas.models import Idea

User = get_user_model()


class BaseFlagTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
                    username='test-1',
                    email='a@a.com',
                    password='1234'
        )
        self.user_2 = User.objects.create_user(
            username='test-2',
            email='b@b.com',
            password='1234'
        )
        self.client.force_login(self.user_1)
        self.ideas = 0
        self.idea_1 = self.create_idea()
        self.idea_2 = self.create_idea()
        content_type = ContentType.objects.get(model=type(self.idea_1).__name__.lower())
        self.content_object_1 = content_type.get_object_for_this_type(id=self.idea_1.id)
        self.content_object_2 = content_type.get_object_for_this_type(id=self.idea_2.id)
        self.flags = 0
        self.url = reverse('flag:flag')

    def increase_flag_count(self):
        self.flags = 1

    def create_idea(self):
        self.ideas += 1
        return Idea.objects.create(
            user=self.user_1,
            title=f'idea {self.ideas} ',
            concept=f'idea number {self.ideas} concept'
        )

    def create_flag(self, ct_object=None, creator=None):
        if not ct_object:
            ct_object = self.content_object_1
        if not creator:
            creator = self.user_1
        return Flag.objects.create(content_object=ct_object, creator=creator)

    def set_flag(self, model_obj=None, user=None, reason=None, info=None):
        if not user:
            user = self.user_1
        if not reason:
            reason = FlagInstance.reason_values[0]
        if not info:
            info = None
        if not model_obj:
            model_obj = self.idea_1
        flag_obj = Flag.objects.get_flag(model_obj)
        self.increase_flag_count()
        return FlagInstance.objects.create(
            flag=flag_obj,
            user=user,
            reason=reason,
            info=info
        )

    def request(self, method: str, path: str, data=None, *args, **kwargs):
        if not data:
            data = ''
        return self.client.generic(method, path, data=json.dumps(data), *args, **kwargs)


class BaseFlagModelTest(BaseFlagTest):
    def setUp(self):
        super().setUp()
        self.flag = self.create_flag()


class BaseFlagViewTest(BaseFlagTest):
    def setUp(self):
        super().setUp()
        self.client = Client(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.force_login(self.user_1)
        self.data = {
            'app_name': 'ideas',
            'model_name': 'idea',
            'model_id': self.idea_1.id,
            'reason': FlagInstance.reason_values[0],
            'info': ''
        }
        self.flag_instance = self.set_flag()


class BaseTemplateTagsTest(BaseFlagTest):
    class MockUser:
        """Mock unauthenticated user for template. The User instance always returns True for `is_authenticated`"""
        is_authenticated = False

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()


class BaseFlagMixinsTest(BaseFlagTest):
    def setUp(self):
        super().setUp()
        self.data = {
            'app_name': 'ideas',
            'model_name': 'idea',
            'model_id': self.idea_1.id
        }
