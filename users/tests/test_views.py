import os

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import mail
from django.shortcuts import get_object_or_404, reverse

from tests.base import TestBase
from users.forms import UserRegisterForm


class TestUserRegistration(TestBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = 'tester_1'
        self.valid_email_string = os.environ.get('VALID_EMAILS', None)
        if self.valid_email_string is not None:
            self.valid_emails = self.valid_email_string.lower().split()
        self.first_name = 'Jach'
        self.last_name = 'Karta'
        self.password = 'user123#'

    @classmethod
    def setUpTestData(cls):
        """Initialise the form data"""
        super().setUpTestData()
        # create a user for testing purpose
        form = UserRegisterForm(data={
            'username': 'Tester_1',
            'first_name': 'Jach',
            'email': cls.valid_emails[2],
            'password1': 'user123#',
            'password2': 'user123#',
        })
        form.save()

    def test_correct_template_used_for_register(self):
        """
        Test if correct template is used for the register url
        """
        # Testing register
        register = self.client.get(reverse('register'))
        # Test HTTP response
        self.assertEqual(register.status_code, 200)
        self.assertTemplateUsed(
            register, template_name='users/register.html')

    def test_username_case_insensitive(self):
        """Test whether username field is case insensitive"""
        email = self.email
        username = self.username

        user = User.objects.get(email=email)
        self.assertEqual(user.username, username.lower())

    def test_email_case_insensitive(self):
        """Test whether email field is case insensitive"""
        email = self.email
        username = self.username

        user = User.objects.get(username=username)
        self.assertEqual(user.email, email.lower())

    def test_email_integrity(self):
        """Test invalidation for use of 1 email by more than 1 accounts,\
            raising of appropriate validation error"""
        email = self.email

        form = UserRegisterForm(data={'email': email, 'username': 'test'})
        # Test invalidation of form
        self.assertFalse(form.is_valid())
        # Test if validation error is raised
        self.assertEqual(form.has_error('email', code='invalid'), True)

    def test_redirect_on_successful_registration(self):
        """Test redirect to home page on successful registration"""
        data = {
            'username': 'tester_11',
            'first_name': 'Jach',
            'email': self.valid_emails[1],
            'password1': 'user123#',
            'password2': 'user123#',
        }
        response = self.client.post(reverse('register'), data=data)
        self.assertRedirects(response, expected_url=reverse('ideas:home'))

    def test_redirect_authenticated_user_on_register(self):
        """Test whether a logged in user is redirected to home when trying to access register link"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, expected_url=reverse('ideas:home'))

class TestProfileView(TestBase):
    def get_url(self):
        return reverse('profile')

    def test_redirect_unauthenticated_user_on_profile(self):
        """Test whether a logged in user is redirected to home when trying to access register link"""
        response = self.client.get(self.get_url())
        self.assertRedirects(response, expected_url='/login/?next=/profile/')

    def test_profile_updation(self):
        """
        Test whether
            - profile urls loads successfully
            - correct template is used for rendering
            - data is updated successfully on post request
        """
        new_data = {
            'username': 'tester2',
            'first_name': 'Jachi',
            'last_name': 'karta',
            'email': self.valid_emails[0],
        }
        self.client.force_login(self.user)
        url_profile = self.get_url()
        # Test GET request
        profile_get = self.client.get(url_profile)
        self.assertEqual(profile_get.status_code, 200)
        self.assertTemplateUsed(
            profile_get, template_name='users/profile.html')

        # Test POST request
        profile_post = self.client.post(url_profile, data=new_data)
        # Test HTTP response
        self.assertEqual(profile_post.status_code, 200)

        user = get_object_or_404(User, username=new_data['username'])

        # Test profile values
        self.assertEqual(user.username, new_data['username'])
        self.assertEqual(user.first_name, new_data['first_name'])
        self.assertEqual(user.last_name, new_data['last_name'])
        self.assertEqual(user.email, new_data['email'])

class TestPasswordChangeView(TestBase):
    def get_url(self):
        return reverse('password-change')

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)

    def test_password_change_for_unauthenticated_users(self):
        """Test whether users can change their password and are logged back in"""
        self.client.logout()
        new_pass = 'NewUser123#'
        data = {
            'old_password': self.user_data['password'],
            'new_password1': new_pass,
            'new_password2': new_pass
        }
        url = self.get_url()
        response = self.client.post(url, data=data)
        self.assertRedirects(response, expected_url=f'{reverse("login")}?next={url}')

    def test_password_change_for_authenticated_users(self):
        """Test whether users can change their password and are logged back in"""
        new_pass = 'NewUser123#'
        data = {
            'old_password': self.user_data['password'],
            'new_password1': new_pass,
            'new_password2': new_pass
        }
        response = self.client.post(self.get_url(), data=data)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_procedure(self):
        """
        Test whether
            - password-reset link is accessible
            - form can be posted successfully from this link
            - an email is send to their with the site name in subject
            - the link to reset password form is working
        """
        url_password_reset = reverse('password_reset')
        site_name = Site.objects.get(id=1).name
        new_pass = 'Newpass123#'

        # test GET response from password-reset
        response = self.client.get(url_password_reset)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset.html')

        # test POST response from password-reset
        response = self.client.post(
            url_password_reset, data={'email': self.user_data['email']})
        self.assertRedirects(
            response, expected_url=reverse('password_reset_done'))

        # Checks related to email
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         f'Password reset on {site_name}')

        # get the userid and token from the resposne
        uid = response.context[0]['uid']
        token = response.context[0]['token']
        url_password_reset_confirm = reverse('password_reset_confirm', kwargs={
            'token': token,
            'uidb64': uid
        })
        response = self.client.get(url_password_reset_confirm)
        # No reverse exists for this url
        url_password_reset_confirm_set = f'/password-reset-confirm/{uid}/set-password/'
        self.assertRedirects(
            response, expected_url=url_password_reset_confirm_set)

        # Now post to the same url with the new password
        response = self.client.post(
            url_password_reset_confirm, data={
                'new_password1': new_pass,
                'new_password1': new_pass
            })
        self.assertRedirects(
            response, expected_url=url_password_reset_confirm_set)
