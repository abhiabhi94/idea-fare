from django.test import TestCase
from django.shortcuts import reverse


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

    def test_content_policy_page(self):
        """Test whether content policy page link is working"""
        response = self.client.get(reverse('ideas:content-policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/content_policy.html')

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


class ClassBasedViewTest(TestCase):
    """Test class based views here"""

    def setUpClass(cls):
        pass

    # def test_conceiver_name_for_anonymous_idea(self):
    #     """Test the name of the conceiver for anonymous idea"""
    #     idea = Idea.objects.get(id=1)
    #     self.assertEqual(idea.conceiver(), 'AnonymousUser')
