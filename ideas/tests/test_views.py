import feedparser
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
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
        - 2 users
            - 1 will be used to associate ideas
            - 2nd will be used for checking unauthorised access during tests
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
        cls.dummy_user = User.objects.create_user(username='tester3',
                                                  email='jach.kar.ta@gmail.com',
                                                  password='user123#'
                                                  )
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

    def test_non_anonymous_idea_create_view_url_name_for_authenticated_user(self):
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

    """
    For IdeaUpdateView, test
        - unauthenticated users are redirected to login page
        - for authenticated users
            - anonymous idea can't be updated
                - raise http error 403
            - for non-anonymous ideas
                    - permission error(http 403) is raised for non owners
                    - only original conceivers(creaters) can
                        - url is accessible by name
                        - correct template is rendered
                        - they can update their idea
    """

    def test_idea_update_view_for_unauthenticated_user(self):
        """Test unauthenticated users are redirected to login page"""
        # Non-anonymous ideas ids are indivisible by 4 and 10
        slug = Idea.objects.get(id=5).slug
        url_idea_update = reverse(
            'ideas:idea-update', kwargs={'slug': slug})
        response = self.client.get(url_idea_update)
        self.assertRedirects(
            response, expected_url=f'/login/?next=%2Fidea%2F{slug}%2Fupdate/')

    def test_anonymous_ideas_update_view_for_authenticated_user(self):
        """Test permission error for access by authenticated users for anonymous ideas"""
        # All anonymous ideas ids are divisible by 4
        idea = Idea.objects.get(id=4)
        self.client.login(username=self.dummy_user.username,
                          password='user123#')
        url_idea_update = reverse(
            'ideas:idea-update', kwargs={'slug': idea.slug})
        response = self.client.get(url_idea_update)
        self.assertEqual(response.status_code, 403)

    def test_idea_update_view_for_nonconceiver(self):
        """Test permission error is raised for non-owners(non-creator or non-conceivers)"""
        slug = Idea.objects.get(id=5).slug
        self.client.login(username=self.dummy_user.username,
                          password='user123#')
        url_idea_update = reverse(
            'ideas:idea-update', kwargs={'slug': slug})
        response = self.client.get(url_idea_update)
        self.assertEqual(response.status_code, 403)

    def test_non_anonymous_idea_update_view_url_name_for_conceiver(self):
        """Test url is accessible by name"""
        slug = Idea.objects.get(id=5).slug
        url_idea_update = reverse(
            'ideas:idea-update', kwargs={'slug': slug})
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(url_idea_update)
        self.assertEqual(response.status_code, 200)

    def test_non_anonymous_idea_update_view_template_for_conceiver(self):
        """Test correct template is used while rendering"""
        slug = Idea.objects.get(id=5).slug
        url_idea_update = reverse(
            'ideas:idea-update', kwargs={'slug': slug})
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(url_idea_update)
        self.assertTemplateUsed(response, template_name='ideas/idea_form.html')

    def test_update_non_anonymous_idea_by_conceiver(self):
        """Test conceivers can update their ideas"""
        slug = Idea.objects.get(id=5).slug
        url_idea_update = reverse(
            'ideas:idea-update', kwargs={'slug': slug})
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(url_idea_update)

        response = self.client.post(url_idea_update, data={
            'title': 'This is an updated idea',
            'concept': 'Unit testing suddenly, seems too much work',
            'user': self.user
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

    #########################################################################################
    """
    For IdeaDeleteView, test
        - unauthenticated users are redirected to login page
        - for authenticated users
            - anonymous idea can't be deleted
                - raise http error 403
            - for non-anonymous ideas
                    - permission error(http 403) is raised for non owners(creators/conceivers)
                    - only original conceivers(creaters) can
                        - url is accessible by name
                        - correct template is rendered
                        - they can delete their idea and redirected to homepage
    """

    def test_idea_delete_view_for_unauthenticated_user(self):
        """Test unauthenticated users are redirected to login page"""
        # Non-anonymous ideas ids are indivisible by 4 and 10
        slug = Idea.objects.get(id=5).slug
        url_idea_delete = reverse(
            'ideas:idea-delete', kwargs={'slug': slug})
        response = self.client.get(url_idea_delete)
        self.assertRedirects(
            response, expected_url=f'/login/?next=%2Fidea%2F{slug}%2Fdelete/')

    def test_anonymous_ideas_delete_view_for_authenticated_user(self):
        """Test permission error for access by authenticated users for anonymous ideas"""
        # All anonymous ideas ids are divisible by 4
        idea = Idea.objects.get(id=4)
        self.client.login(username=self.dummy_user.username,
                          password='user123#')
        url_idea_delete = reverse(
            'ideas:idea-delete', kwargs={'slug': idea.slug})
        response = self.client.get(url_idea_delete)
        self.assertEqual(response.status_code, 403)

    def test_idea_delete_view_for_nonconceiver(self):
        """Test permission error is raised for non-owners(non-creator or non-conceivers)"""
        slug = Idea.objects.get(id=5).slug
        self.client.login(username=self.dummy_user.username,
                          password='user123#')
        url_idea_delete = reverse(
            'ideas:idea-delete', kwargs={'slug': slug})
        response = self.client.get(url_idea_delete)
        self.assertEqual(response.status_code, 403)

    def test_non_anonymous_idea_delete_view_url_name_for_conceiver(self):
        """Test url is accessible by name"""
        slug = Idea.objects.get(id=5).slug
        url_idea_delete = reverse(
            'ideas:idea-delete', kwargs={'slug': slug})
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(url_idea_delete)
        self.assertEqual(response.status_code, 200)

    def test_non_anonymous_idea_delete_view_template_for_conceiver(self):
        """Test correct template is used while rendering"""
        slug = Idea.objects.get(id=5).slug
        url_idea_delete = reverse(
            'ideas:idea-delete', kwargs={'slug': slug})
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(url_idea_delete)
        self.assertTemplateUsed(
            response, template_name='ideas/idea_confirm_delete.html')

    def test_delete_non_anonymous_idea_by_conceiver(self):
        """Test conceivers can update their ideas"""
        slug = Idea.objects.get(id=5).slug
        url_idea_delete = reverse(
            'ideas:idea-delete', kwargs={'slug': slug})
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(url_idea_delete)

        response = self.client.post(url_idea_delete)
        self.assertRedirects(response, expected_url=reverse('ideas:home'))
        # Ensure that the resource no longer exists
        response = self.client.get(url_idea_delete)
        self.assertEqual(response.status_code, 404)

    #########################################################################################

    """
    For IdeaDetailView, test
        - correct template is used for rendering
        - for public ideas
            - url is accessible to everyone
        - private ideas 
            - url are only accessible to conceivers
            - for others throw a permission error 
    """

    def test_idea_detail_view_template(self):
        """Test correct template is used while rendering"""
        url_idea_detail = Idea.objects.get(id=5).get_absolute_url()
        response = self.client.get(url_idea_detail)
        self.assertTemplateUsed(
            response, template_name='ideas/idea_details.html')

    def test_public_idea_detail_view_url_by_name(self):
        """Test correct template is used while rendering"""
        slug = Idea.objects.get(id=5).slug
        url_idea_detail = reverse('ideas:idea-details', kwargs={'slug': slug})
        response = self.client.get(url_idea_detail)
        self.assertEqual(response.status_code, 200)

    def test_private_idea_detail_view_url_for_nonconceiver(self):
        """Test whether permission error is raised or not"""
        # idea with id 10 is private
        url_idea_detail = Idea.objects.get(id=10).get_absolute_url()
        response = self.client.get(url_idea_detail)
        self.assertTrue(response.status_code, 403)

    def test_private_idea_detail_view_url_for_conceiver(self):
        """Test whether conceivers can access their private idea"""
        # idea with id 10 is private
        url_idea_detail = Idea.objects.get(id=10).get_absolute_url()
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(url_idea_detail)
        self.assertTrue(response.status_code, 200)

    #############################################################################

    """
    For ConceiverIdeaListView, test
        - url is accessible by name
        - correct template is used for rendering
        - for anonymous ideas(username=anonymous), all such ideas are shown
        - for non-anonymous users, all of their public ideas are shown
        - for non-anonymous users, none of their private idea is shown
        - for authenticated users, their private idea is shown 
    """

    def test_conceiver_idea_list_view_url_by_name(self):
        """Test url is accessible by name"""
        url_conceiver_idea = reverse(
            'ideas:conceiver-ideas', kwargs={'username': self.user.username})
        response = self.client.get(url_conceiver_idea)
        self.assertEqual(response.status_code, 200)

    def test_conceiver_idea_list_view_url_template(self):
        """Test correct template is used for rendering"""
        url_conceiver_idea = reverse(
            'ideas:conceiver-ideas', kwargs={'username': self.user.username})
        response = self.client.get(url_conceiver_idea)
        self.assertTemplateUsed(
            response, template_name='ideas/conceiver_ideas.html')

    def test_conceiver_idea_list_view_for_anonymous_idea(self):
        """Test all anonymous ideas are shown"""
        url_conceiver_idea = reverse(
            'ideas:conceiver-ideas', kwargs={'username': AnonymousUser.username})
        response = self.client.get(url_conceiver_idea)
        # Ideas with id -> (4, 8, 12, 16, 20, 24) are anonymous
        self.assertEqual(len(response.context['ideas']), 6)

    def test_conceiver_idea_list_view_for_private_idea(self):
        """Test privates ideas are shown only to conceivers"""
        url_conceiver_idea = reverse(
            'ideas:conceiver-ideas', kwargs={'username': self.user.username})
        self.client.login(username=self.user.username, password='user123#')
        response = self.client.get(url_conceiver_idea)
        # Idea with id -> (10) is anonymous
        idea = Idea.objects.get(id=10)
        # idea is present in context
        self.assertEqual(idea in response.context['ideas'], True)
        # all private ideas are shown
        self.assertEqual(len(response.context['ideas']), 15)

    def test_conceiver_idea_list_view_for_public_idea_pagination(self):
        """Test all public ideas are shown and the view is paginated"""
        url_conceiver_idea = reverse(
            'ideas:conceiver-ideas', kwargs={'username': self.user.username})
        response = self.client.get(url_conceiver_idea)
        # There are 17 public ideas, see setUpTestData function for more information
        self.assertEqual('is_paginated' in response.context, True)
        self.assertEqual(response.context['is_paginated'], True)
        self.assertEqual(len(response.context['ideas']), 15)

    ####################################################################################

    """
    For LatestIdeaRSSFeed, test
        - url is accessible by name
        - feed is in correct format
        - feed uses the last_modified functionality(used for caching)
        - each item contains
            - title
            - description
            - author's name
            - link
    """

    def test_latest_post_rss_feed_url_by_name(self):
        """Test the url by name"""
        response = self.client.get(reverse('ideas:rss-feed'))
        self.assertEqual(response.status_code, 200)

    def test_latest_post_rss_feed_format(self):
        """Test the format of the feed"""
        url_rss_feed = reverse('ideas:rss-feed')
        response = self.client.get(url_rss_feed)
        feed = feedparser.parse(response.content)
        # 1 indicates feed is not in a correct format
        self.assertEqual(feed['bozo'], 0)

    def test_latest_post_rss_feed_last_modified(self):
        """Test the last_modified property of the feed"""
        url_rss_feed = reverse('ideas:rss-feed')
        response = self.client.get(url_rss_feed)
        last_modified = response._headers.get('last-modified', None)
        self.assertNotEqual(last_modified, None)

    def test_latest_post_rss_feed_item_number(self):
        """Test all the public ideas are present: 23(24(total) - 1(private))"""
        url_rss_feed = reverse('ideas:rss-feed')
        response = self.client.get(url_rss_feed)
        feed = feedparser.parse(response.content)
        self.assertEqual(len(feed['items']), 23)

    def test_latest_post_rss_feed_item_title(self):
        """Test each item contains title"""
        url_rss_feed = reverse('ideas:rss-feed')
        response = self.client.get(url_rss_feed)
        feed = feedparser.parse(response.content)
        title = feed['items'][0].title
        self.assertNotEqual(title, '')

    def test_latest_post_rss_feed_item_description(self):
        """Test each item contains description"""
        url_rss_feed = reverse('ideas:rss-feed')
        response = self.client.get(url_rss_feed)
        feed = feedparser.parse(response.content)
        description = feed['items'][0].description
        self.assertNotEqual(description, '')

    def test_latest_post_rss_feed_item_author_name(self):
        """Test each item contains author name"""
        url_rss_feed = reverse('ideas:rss-feed')
        response = self.client.get(url_rss_feed)
        feed = feedparser.parse(response.content)
        author = feed['items'][0].author
        self.assertNotEqual(author, '')

    def test_latest_post_rss_feed_item_link(self):
        """Test each item contains link"""
        url_rss_feed = reverse('ideas:rss-feed')
        response = self.client.get(url_rss_feed)
        feed = feedparser.parse(response.content)
        link = feed['items'][0].link
        self.assertNotEqual(link, '')
