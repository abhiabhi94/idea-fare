from flag.templatetags.flag_tags import get_app_name, get_model_name, has_flagged, render_flag_form
from flag.tests.base import BaseTemplateTagsTest, FlagInstance


class TestFlagTemplateTest(BaseTemplateTagsTest):
    def test_get_model_name(self):
        self.assertEqual(get_model_name(self.idea_1), 'Idea')

    def test_get_app_name(self):
        self.assertEqual(get_app_name(self.idea_1), 'ideas')

    def test_has_flagged_for_unauthenticated_user(self):
        user = self.MockUser()
        self.assertEqual(has_flagged(user, self.idea_1), False)

    def test_has_flagged_for_authenticated_user(self):
        user = self.user_2
        idea = self.idea_1
        self.assertEqual(has_flagged(user, idea), False)
        # flag the object
        self.set_flag(idea, user)
        self.assertEqual(has_flagged(user, idea), True)

    def test_render_flag_form(self):
        idea = self.idea_1
        user = self.user_2
        data = render_flag_form(idea, user)

        self.assertEqual(data['app_name'], idea._meta.app_label)
        self.assertEqual(data['model_name'], type(idea).__name__)
        self.assertEqual(data['model_id'], idea.id)
        self.assertEqual(data['flag_reasons'], FlagInstance.reasons)
        self.assertEqual(data['has_flagged'], False)

        # flag the object
        self.set_flag(idea, user)
        data = render_flag_form(idea, user)

        self.assertEqual(data['app_name'], idea._meta.app_label)
        self.assertEqual(data['model_name'], type(idea).__name__)
        self.assertEqual(data['model_id'], idea.id)
        self.assertEqual(data['flag_reasons'], FlagInstance.reasons)
        self.assertEqual(data['has_flagged'], True)
