from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ideas.models import Idea


class FunctionBasedViewTest(TestCase):
    """
    Test function based view here.

    Things to test
        - response code
        - template used
        - any other functionality in use
    """

    def test_about_page(self):
        """Test whether about page link is working"""
        response = self.client.get(reverse('ideas:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/about.html')

    #####################################################

    def test_content_policy_page(self):
        """Test whether content policy page link is working"""
        response = self.client.get(reverse('ideas:content-policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/content_policy.html')

    #########################################################

    def test_privacy_policy_page(self):
        """Test whether privacy policy page link is working"""
        response = self.client.get(reverse('ideas:privacy-policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/privacy_policy.html')

    # 3

    def test_subscription_with_dummy_email(self):
        """Test whether dummy emails can't be used for subscription"""
        response = self.client.post(
            reverse('ideas:subscription'),
            data={'email': 'a@a.com'},
            **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            },
        )
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response['status'], -1)
        self.assertEqual('not a valid' in response['msg'], True)

    def test_subscription_with_real_email(self):
        """Test whether genuine emails can be used for subscription"""
        response = self.client.post(
            reverse('ideas:subscription'),
            data={'email': 'jachkarta@gmail.com'},
            **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            },
        )
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response['status'], 0)
        self.assertNotEqual('not' in response['msg'], True)
        self.assertEqual('success' in response['msg'], True)

    def test_subscription_integrity(self):
        """Test that 1 email can only be used to subscribe once"""
        # First subscribe with the email
        self.test_subscription_with_real_email()
        # Now test subscribing again
        response = self.client.post(
            reverse('ideas:subscription'),
            data={'email': 'jachkarta@gmail.com'},
            **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            },
        )
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response['status'], -1)
        self.assertEqual('already registered' in response['msg'], True)

    ######################################################################


class ClassBasedViewTest(TestCase):
    """
    Test class based views here

        - Try to write all tests for a class in one function\
            this works as functional testing as opposed to unit testing\
                This is done because when tests are scattered,it is\
                    tough to tell whether all tests have been\
                        written or not

        - For each class, test
            - url works as on desired location
            - url works by name
            - correct template is used
            - pagination if required
            - any other functionality as required
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create
        - 1 user
        - 24 ideas to test pagination\
            ( text inside brackets indicate pattern used for generating id)
            - 6 anonymous ideas (x % 4 == 0)
            - 18 non-anonymous ideas
                - 1 private idea (x % 4 != 0 and x % 10 == 0)
                - 17 public ideas (x%4 != 0 and x%10 != 0)
        """
        # Create 20 ideas to test pagination
        num_ideas = 25
        cls.user = User.objects.create_user(username='tester2',
                                            email='jachkarta+tester@gmail.com',
                                            password='user123#')
        for idea_id in range(1, num_ideas):
            if idea_id % 4 == 0:
                Idea.objects.create(
                    title=f'Anonymous Idea: idea number {idea_id}',
                    concept=f'The concept of the idea {idea_id}',
                )
            else:
                Idea.objects.create(
                    title=f'Non-anonymous Idea: idea number {idea_id}',
                    concept=f'The concept of the idea{idea_id}',
                    user=cls.user,
                    visibility=False if idea_id % 10 == 0 else True
                )

    """
    For Home, test
        - url by location
        - url by name
        - template
        - pagination
        - all ideas have visibility as True(public)
    """

    def test_home_view_url_by_name(self):
        response = self.client.get(reverse('ideas:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_by_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse('ideas:home'))
        self.assertTemplateUsed(response, template_name='ideas/home.html')

    def test_home_view_pagination(self):
        response = self.client.get(reverse('ideas:home'))
        self.assertEqual('is_paginated' in response.context, True)
        self.assertEqual(response.context['is_paginated'], True)
        self.assertEqual(len(response.context['ideas']), 15)

    def test_home_view_visibility_for_ideas(self):
        """Test that only public ideas are visibile"""
        response = self.client.get(reverse('ideas:home'))
        [self.assertEqual(idea.visibility, True)
         for idea in response.context['ideas']]

    #########################################################################

    """
    For AnonymousIdeaCreateView, test
        - url by location
        - url by name
        - correct template is used
        - idea can be created by unauthenticated users
        - idea can be created by authenticated users
    """

    def test_anonymous_idea_create_view_url_location(self):
        """Test url is accessible by location"""
        response = self.client.get('/idea/anonymous/new/')
        self.assertEqual(response.status_code, 200)

    def test_anonymous_idea_create_view_url_name(self):
        """Test url is accessible by name"""
        response = self.client.get(reverse('ideas:idea-create-anonymous'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_idea_create_view_template(self):
        """Test correct template is used while rendering"""
        response = self.client.get(reverse('ideas:idea-create-anonymous'))
        self.assertTemplateUsed(response, template_name='ideas/idea_form.html')

    def test_create_anonymous_idea_by_unauthenticated_user(self):
        """Test unauthenticated users can create anonymous ideas"""
        url_idea_create = reverse('ideas:idea-create-anonymous')
        response = self.client.get(url_idea_create)
        response = self.client.post(url_idea_create, data={
            'title': 'This is an anonymous idea',
            'concept': 'Unit testing seems to be fun and boring'
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

    def test_create_anonymous_idea_by_authenticated_user(self):
        """Test authenticated users can create anonymous ideas"""
        url_idea_create = reverse('ideas:idea-create-anonymous')
        response = self.client.get(url_idea_create)
        self.client.login(username=self.user.username, password='user123#')

        response = self.client.post(url_idea_create, data={
            'title': 'This is an anonymous idea',
            'concept': 'Unit testing seems to be fun and boring',
            'user': self.user
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

    ################################################################################

    """
    For NonAnonymousIdeaCreateView, test
        - unauthenticated users are redirected to login page
        - for authenticated users,
            - url is accessible by location
            - url is accessible by name
            - correct template is rendered
            - they can create
                - public idea
                - private idea
    """

    def test_non_anonymous_idea_create_view_for_unauthenticated_user(self):
        """Test unauthenticated users are redirected to login page"""
        url_idea_create = reverse('ideas:idea-create-non-anonymous')
        response = self.client.get(url_idea_create)
        self.assertRedirects(
            response, expected_url='/login/?next=%2Fidea%2Fnew%2F')

    def test_non_anonymous_idea_create_view_url_location_for_unauthenticated_user(self):
        """Test url is accessible by location"""
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get('/idea/new/')
        self.assertEqual(response.status_code, 200)

    def test_non_anonymous_idea_create_view_url_name_for_unauthenticated_user(self):
        """Test url is accessible by name"""
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(reverse('ideas:idea-create-non-anonymous'))
        self.assertEqual(response.status_code, 200)

    def test_non_anonymous_idea_create_view_template_for_authenticated_user(self):
        """Test correct template is used while rendering"""
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(reverse('ideas:idea-create-non-anonymous'))
        self.assertTemplateUsed(response, template_name='ideas/idea_form.html')

    def test_create_non_anonymous_public_idea_by_authenticated_user(self):
        """Test authenticated users can create public ideas"""
        url_idea_create = reverse('ideas:idea-create-non-anonymous')
        response = self.client.get(url_idea_create)
        self.client.login(username=self.user.username, password='user123#')

        response = self.client.post(url_idea_create, data={
            'title': 'This is an anonymous public idea',
            'concept': 'Unit testing seems to be fun and boring',
            'user': self.user
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

    def test_create_non_anonymous_private_idea_by_authenticated_user(self):
        """Test authenticated users can create private ideas"""
        url_idea_create = reverse('ideas:idea-create-non-anonymous')
        response = self.client.get(url_idea_create)
        self.client.login(username=self.user.username, password='user123#')

        response = self.client.post(url_idea_create, data={
            'title': 'This is an non-anonymous private idea',
            'concept': 'Unit testing seems to be fun and boring',
            'user': self.user,
            'visibility': False
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

    #########################################################################################