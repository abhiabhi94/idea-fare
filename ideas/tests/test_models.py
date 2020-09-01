from tests.base import TestBase


class IdeaModelTest(TestBase):

    @classmethod
    def setUpClass(cls):
        """
        Initialise data for all tests
        - Create an anonymous idea
        - Create a user and associate them with a new idea.
        """
        super().setUpClass()
        # Create an anonymous idea
        cls.anonymous_idea = cls.create_idea(
                                            title='This is a test idea',
                                            concept='Wow this is really awesome',
                                            )
        # Create an idea with a user
        cls.non_anonymous_idea = cls.create_idea(
                                                title='This is another idea',
                                                concept='This seems fun',
                                                user=cls.user
                                                )

    def test_max_length_title(self):
        """Test max length for title of an idea is 60"""
        idea = self.non_anonymous_idea
        max_length = idea._meta.get_field('title').max_length
        self.assertEqual(max_length, 60)

    def test_max_length_concept(self):
        """Test max length for concept of an idea is 500"""
        idea = self.non_anonymous_idea
        max_length = idea._meta.get_field('concept').max_length
        self.assertEqual(max_length, 500)

    def test_max_length_slug(self):
        """Test max length for slug of an idea is 80"""
        idea = self.non_anonymous_idea
        max_length = idea._meta.get_field('slug').max_length
        self.assertEqual(max_length, 80)

    def test_username_for_anonymous_idea(self):
        """Test the username of the conceiver for anonymous idea"""
        idea = self.anonymous_idea
        self.assertEqual(idea.conceiver.username, 'anonymous')

    def test_anonymous_ideas_visibility(self):
        """Test whether anonymous ideas will always be public"""
        idea = self.anonymous_idea
        self.assertEqual(idea.visibility, True)

    def test_conceiver_name_for_anonymous_idea(self):
        """Test the name of the conceiver for anonymous idea"""
        idea = self.anonymous_idea
        self.assertEqual(str(idea.conceiver()), 'AnonymousUser')

    def test_conceiver_name_for_non_anonymous_idea(self):
        """Test the name of the conceiver for non anonymous idea"""
        idea = self.non_anonymous_idea
        self.assertEqual(idea.conceiver.get_full_name(), 'Jach Karta')

    def test_idea_object_name(self):
        """Test that the title is returned when the object is printed"""
        idea = self.non_anonymous_idea
        self.assertEqual(str(idea), idea.title)

    def test_get_absolute_url(self):
        """Test whether model returns correct url for detail view of an idea"""
        idea = self.non_anonymous_idea
        # We can't exactly test the exact url since there are random characters added to the slug
        self.assertEqual(idea.slug in idea.get_absolute_url(), True)

    def test_meta_data_for_seo(self):
        """Test meta-information about the model that will be used for SEO functionalities"""
        pass
