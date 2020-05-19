import feedparser
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.shortcuts import reverse

from ideas.models import Idea
from ideas.tests.base import TestIdeaBase
from tests.base import TestBase


class TestAboutPage(TestBase):
    def test_about_page(self):
        """Test whether about page link is working"""
        response = self.client.get(reverse('ideas:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/about.html')

class TestContentPolicyPage(TestBase):
    def test_content_policy_page(self):
        """Test whether content policy page link is working"""
        response = self.client.get(reverse('ideas:content-policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/content_policy.html')

class TestPrivacyPolicyPage(TestBase):
    def test_privacy_policy_page(self):
        """Test whether privacy policy page link is working"""
        response = self.client.get(reverse('ideas:privacy-policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/privacy_policy.html')

class TestSubscription(TestBase):
    def get_url(self):
        return reverse('ideas:subscription')

    def request(self, method='post', is_ajax=True, *args, **kwargs):
        """
        A utility function to return perform client requests.
        Args:
            method (str, optional): The HTTP method name. Defaults to 'POST'.
            is_ajax (bool, optional): Whether AJAX request is to be performed or not. Defaults to True.

        Raises:
            ValueError: When a invalid HTTP method name is passed.

        Returns:
            `Any`: Response from the request.
        """
        request_method = getattr(self.client, method.lower(), None)
        url = self.get_url()
        if not request_method:
            raise ValueError('This is not a valid request method')
        if is_ajax:
            return request_method(url, *args, **kwargs, **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'
            })
        return request_method(url, *args, **kwargs)

    def test_subscription_with_non_ajax(self):
        """Test whether dummy emails can't be used for subscription"""
        response = self.request(is_ajax=False, data={'email': 'a@a.com'})
        self.assertEqual(response.status_code, 400)

    def test_subscription_with_get_request(self):
        """Test whether dummy emails can't be used for subscription"""
        response = self.request(method='get', data={'email': 'a@a.com'})
        self.assertEqual(response.status_code, 405)

    def test_subscription_with_dummy_email(self):
        """Test whether dummy emails can't be used for subscription"""
        response = self.request(data={'email': 'a@a.com'})
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response['status'], -1)
        self.assertEqual('not a valid' in response['msg'], True)


    def test_subscription_with_dummy_email(self):
        """Test whether dummy emails can't be used for subscription"""
        response = self.request(data={'email': 'a@a.com'})
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response['status'], -1)
        self.assertEqual('not a valid' in response['msg'], True)

    def test_subscription_with_real_email(self):
        """Test whether genuine emails can be used for subscription"""
        response = self.request(data={'email': 'jachkarta@gmail.com'})
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response['status'], 0)
        self.assertNotEqual('not' in response['msg'], True)
        self.assertEqual('success' in response['msg'], True)

    def test_subscription_integrity(self):
        """Test that 1 email can only be used to subscribe once"""
        # First subscribe with the email
        response = self.request(data={'email': 'jachkarta@gmail.com'})
        # Now test subscribing again
        response = self.request(data={'email': 'jachkarta@gmail.com'})
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response['status'], -1)
        self.assertEqual('already registered' in response['msg'], True)

class TestHomeView(TestIdeaBase):
    """
    For Home, test
        - url by location
        - url by name
        - template
        - pagination
        - all ideas have visibility as True(public)
    """
    def get_url(self):
        return reverse('ideas:home')

    def test_home_view_url_by_name(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_by_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, template_name='ideas/home.html')

    def test_home_view_pagination(self):
        response = self.client.get(self.get_url())
        self.assertEqual('is_paginated' in response.context, True)
        self.assertEqual(response.context['is_paginated'], True)
        self.assertEqual(len(response.context['ideas']), 15)

    def test_home_view_visibility_for_ideas(self):
        """Test that only public ideas are visibile"""
        response = self.client.get(self.get_url())
        [self.assertEqual(idea.visibility, True)
         for idea in response.context['ideas']]

class TestAnonymousIdeaCreateView(TestIdeaBase):
    """
    For AnonymousIdeaCreateView, test
        - url by location
        - url by name
        - correct template is used
        - idea can be created by unauthenticated users
        - idea can be created by authenticated users
    """

    def get_url(self):
        return reverse('ideas:idea-create-anonymous')

    def test_anonymous_idea_create_view_url_location(self):
        """Test url is accessible by location"""
        response = self.client.get('/idea/anonymous/new/')
        self.assertEqual(response.status_code, 200)

    def test_anonymous_idea_create_view_url_name(self):
        """Test url is accessible by name"""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_anonymous_idea_create_view_template(self):
        """Test correct template is used while rendering"""
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, template_name='ideas/idea_form.html')

    def test_create_anonymous_idea_by_unauthenticated_user(self):
        """Test unauthenticated users can create anonymous ideas"""
        self.client.logout()
        response = self.client.post(self.get_url(), data={
            'title': 'This is an anonymous idea',
            'concept': 'Unit testing seems to be fun and boring',
            'tags': 'test, unit-test'
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

    def test_create_anonymous_idea_by_authenticated_user(self):
        """Test authenticated users can create anonymous ideas"""
        response = self.client.post(self.get_url(), data={
            'title': 'This is an anonymous idea',
            'concept': 'Unit testing seems to be fun and boring',
            'tags': 'test, unit-test',
            'user': self.user
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

class TestNonAnonymousIdeaCreateView(TestIdeaBase):
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
    def get_url(self):
        """A utility function that returns URL for this view"""
        return reverse('ideas:idea-create-non-anonymous')

    def test_non_anonymous_idea_create_view_for_unauthenticated_user(self):
        """Test unauthenticated users are redirected to login page"""
        self.client.logout()
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, expected_url='/login/?next=%2Fidea%2Fnew%2F')

    def test_non_anonymous_idea_create_view_url_location_for_unauthenticated_user(self):
        """Test url is accessible by location"""
        response = self.client.get('/idea/new/')
        self.assertEqual(response.status_code, 200)

    def test_non_anonymous_idea_create_view_url_name_for_authenticated_user(self):
        """Test url is accessible by name"""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_non_anonymous_idea_create_view_template_for_authenticated_user(self):
        """Test correct template is used while rendering"""
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, template_name='ideas/idea_form.html')

    def test_create_non_anonymous_public_idea_by_authenticated_user(self):
        """Test authenticated users can create public ideas"""
        response = self.client.post(self.get_url(), data={
            'title': 'This is an anonymous public idea',
            'concept': 'Unit testing seems to be fun and boring',
            'tags': 'test, unit-test',
            'user': self.user
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

    def test_create_non_anonymous_private_idea_by_authenticated_user(self):
        """Test authenticated users can create private ideas"""
        response = self.client.post(self.get_url(), data={
            'title': 'This is an non-anonymous private idea',
            'concept': 'Unit testing seems to be fun and boring',
            'tags': 'test, unit-test',
            'user': self.user,
            'visibility': False
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

    #########################################################################################

class TestIdeaUpdateView(TestIdeaBase):
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
    def get_slug(self):
        # slug of a non-anonymous Idea
        return Idea.objects.get(id=5).slug

    def get_url(self, slug=None):
        if not slug:
            slug = self.get_slug()
        return reverse('ideas:idea-update', kwargs={'slug': slug})


    def test_idea_update_view_for_unauthenticated_user(self):
        """Test unauthenticated users are redirected to login page"""
        self.client.logout()
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, expected_url=f'/login/?next=%2Fidea%2F{self.get_slug()}%2Fupdate/')

    def test_anonymous_ideas_update_view_for_authenticated_user(self):
        """Test permission error for access by authenticated users for anonymous ideas"""
        # All anonymous ideas ids are divisible by 4
        slug = Idea.objects.get(id=4).slug
        response = self.client.get(self.get_url(slug=slug))
        self.assertEqual(response.status_code, 403)

    def test_idea_update_view_for_nonconceiver(self):
        """Test permission error is raised for non-owners(non-creator or non-conceivers)"""
        self.client.force_login(self.dummy_user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 403)

    def test_non_anonymous_idea_update_view_url_name_for_conceiver(self):
        """Test url is accessible by name"""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_non_anonymous_idea_update_view_template_for_conceiver(self):
        """Test correct template is used while rendering"""
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(response, template_name='ideas/idea_form.html')

    def test_update_non_anonymous_idea_by_conceiver(self):
        """Test conceivers can update their ideas"""
        response = self.client.post(self.get_url(), data={
            'title': 'This is an updated idea',
            'concept': 'Unit testing suddenly, seems too much work',
            'tags': 'update-test, unit-test',
            'user': self.user
        })
        # Can't use assertRedirect since we are not sure about the redirected url
        self.assertEqual(response.status_code, 302)

class TestIdeaDeleteView(TestIdeaBase):
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
    def get_slug(self):
        # Non-anonymous ideas ids are indivisible by 4 and 10
        return Idea.objects.get(id=5).slug

    def get_url(self, slug=None):
        if not slug:
            slug = self.get_slug()
        return reverse('ideas:idea-delete', kwargs={'slug': slug})

    def test_idea_delete_view_for_unauthenticated_user(self):
        """Test unauthenticated users are redirected to login page"""
        self.client.logout()
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, expected_url=f'/login/?next=%2Fidea%2F{self.get_slug()}%2Fdelete/')

    def test_anonymous_ideas_delete_view_for_authenticated_user(self):
        """Test permission error for access by authenticated users for anonymous ideas"""
        # All anonymous ideas ids are divisible by 4
        slug = Idea.objects.get(id=4).slug
        response = self.client.get(self.get_url(slug))
        self.assertEqual(response.status_code, 403)

    def test_idea_delete_view_for_nonconceiver(self):
        """Test permission error is raised for non-owners(non-creator or non-conceivers)"""
        self.client.force_login(self.dummy_user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 403)

    def test_non_anonymous_idea_delete_view_url_name_for_conceiver(self):
        """Test url is accessible by name"""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_non_anonymous_idea_delete_view_template_for_conceiver(self):
        """Test correct template is used while rendering"""
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(
            response, template_name='ideas/idea_confirm_delete.html')

    def test_delete_non_anonymous_idea_by_conceiver(self):
        """Test conceivers can update their ideas"""
        url = self.get_url()
        response = self.client.post(self.get_url())
        self.assertRedirects(response, expected_url=reverse('ideas:home'))
        # Ensure that the resource no longer exists
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class TestIdeaDetailView(TestIdeaBase):
    """
    For IdeaDetailView, test
        - correct template is used for rendering
        - for public ideas
            - url is accessible to everyone
        - private ideas
            - url are only accessible to conceivers
            - for others throw a permission error
    """
    def get_slug(self):
        # Non-anonymous ideas ids are indivisible by 4 and 10
        return Idea.objects.get(id=5).slug

    def get_url(self, slug=None):
        if not slug:
            slug = self.get_slug()
        return reverse('ideas:idea-details', kwargs={'slug': slug})

    def test_idea_detail_view_template(self):
        """Test correct template is used while rendering"""
        url_idea_detail = Idea.objects.get(id=5).get_absolute_url()
        response = self.client.get(url_idea_detail)
        self.assertTemplateUsed(
            response, template_name='ideas/idea_details.html')

    def test_public_idea_detail_view_url_by_name(self):
        """Test correct template is used while rendering"""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_private_idea_detail_view_url_for_nonconceiver(self):
        """Test whether permission error is raised or not"""
        # idea with id 10 is private
        self.client.logout()
        slug = Idea.objects.get(id=10).slug
        response = self.client.get(self.get_url(slug))
        self.assertTrue(response.status_code, 403)

    def test_private_idea_detail_view_url_for_conceiver(self):
        """Test whether conceivers can access their private idea"""
        # idea with id 10 is private
        slug = Idea.objects.get(id=10).slug
        response = self.client.get(self.get_url(slug))
        self.assertTrue(response.status_code, 200)

class TestConceiverIdeaListView(TestIdeaBase):
    """
    For ConceiverIdeaListView, test
        - url is accessible by name
        - correct template is used for rendering
        - for anonymous ideas(username=anonymous), all such ideas are shown
        - for non-anonymous users, all of their public ideas are shown
        - for non-anonymous users, none of their private idea is shown
        - for authenticated users, their private idea is shown
    """
    def get_url(self, username=None):
        if not username:
            username = self.user_data['username']
        return reverse('ideas:conceiver-ideas', kwargs={'username': username})

    def test_conceiver_idea_list_view_url_by_name(self):
        """Test url is accessible by name"""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_conceiver_idea_list_view_url_template(self):
        """Test correct template is used for rendering"""
        response = self.client.get(self.get_url())
        self.assertTemplateUsed(
            response, template_name='ideas/conceiver_ideas.html')

    def test_conceiver_idea_list_view_for_anonymous_idea(self):
        """Test all anonymous ideas are shown"""
        response = self.client.get(self.get_url(username=AnonymousUser.username))
        # Ideas with id -> (4, 8, 12, 16, 20, 24) are anonymous
        self.assertEqual(len(response.context['ideas']), 6)

    def test_conceiver_idea_list_view_for_private_idea(self):
        """Test privates ideas are shown only to conceivers"""
        response = self.client.get(self.get_url())
        # Idea with id -> (10) is anonymous
        idea = Idea.objects.get(id=10)
        # idea is present in context
        self.assertEqual(idea in response.context['ideas'], True)
        # all private ideas are shown
        self.assertEqual(len(response.context['ideas']), 15)

    def test_conceiver_idea_list_view_for_public_idea_pagination(self):
        """Test all public ideas are shown and the view is paginated"""
        response = self.client.get(self.get_url())
        # There are 17 public ideas, see setUpTestData function for more information
        self.assertEqual('is_paginated' in response.context, True)
        self.assertEqual(response.context['is_paginated'], True)
        self.assertEqual(len(response.context['ideas']), 15)

class TestLatestIdeaRSSFeed(TestIdeaBase):
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
    def get_url(self):
        return reverse('ideas:rss-feed')

    def test_latest_post_rss_feed_url_by_name(self):
        """Test the url by name"""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_latest_post_rss_feed_format(self):
        """Test the format of the feed"""
        response = self.client.get(self.get_url())
        feed = feedparser.parse(response.content)
        # 1 indicates feed is not in a correct format
        self.assertEqual(feed['bozo'], 0)

    def test_latest_post_rss_feed_last_modified(self):
        """Test the last_modified property of the feed"""
        response = self.client.get(self.get_url())
        last_modified = response._headers.get('last-modified', None)
        self.assertNotEqual(last_modified, None)

    def test_latest_post_rss_feed_item_number(self):
        """Test all the public ideas are present: 23(24(total) - 1(private))"""
        response = self.client.get(self.get_url())
        feed = feedparser.parse(response.content)
        self.assertEqual(len(feed['items']), 23)

    def test_latest_post_rss_feed_item_title(self):
        """Test each item contains title"""
        response = self.client.get(self.get_url())
        feed = feedparser.parse(response.content)
        title = feed['items'][0].title
        self.assertNotEqual(title, '')

    def test_latest_post_rss_feed_item_description(self):
        """Test each item contains description"""
        response = self.client.get(self.get_url())
        feed = feedparser.parse(response.content)
        description = feed['items'][0].description
        self.assertNotEqual(description, '')

    def test_latest_post_rss_feed_item_author_name(self):
        """Test each item contains author name"""
        response = self.client.get(self.get_url())
        feed = feedparser.parse(response.content)
        author = feed['items'][0].author
        self.assertNotEqual(author, '')

    def test_latest_post_rss_feed_item_link(self):
        """Test each item contains link"""
        response = self.client.get(self.get_url())
        feed = feedparser.parse(response.content)
        link = feed['items'][0].link
        self.assertNotEqual(link, '')
