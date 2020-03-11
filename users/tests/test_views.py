from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.models import User
from users.forms import UserRegisterForm


class UserDetailsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Initialise the form data"""
        # create a user for testing purpose
        form = UserRegisterForm(data={
            'username': 'Tester',
            'first_name': 'Jach',
            'email': 'Jachkarta@gmail.com',
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
        email = 'jachkarta@gmail.com'
        username = 'tester'

        user = User.objects.get(email=email)
        self.assertEqual(user.username, username)

    def test_email_case_insensitive(self):
        """Test whether email field is case insensitive"""
        email = 'jachkarta@gmail.com'
        username = 'tester'

        user = User.objects.get(username=username)
        self.assertEqual(user.email, email)

    def test_email_integrity(self):
        """Test invalidation for use of 1 email by more than 1 accounts,\
            raising of appropriate validation error"""
        email = 'jachkarta@gmail.com'

        form = UserRegisterForm(data={'email': email, 'username': 'test'})
        # Test invalidation of form
        self.assertFalse(form.is_valid())
        # Test if validation error is raised
        self.assertEqual(form.has_error('email', code='invalid'), True)

    def test_redirect_on_successful_registration(self):
        """Test redirect to home page on successful registration"""
        data = {
            'username': 'tester1',
            'first_name': 'Jach',
            'email': 'jachkarta+test@gmail.com',
            'password1': 'user123#',
            'password2': 'user123#',
        }
        response = self.client.post(reverse('register'), data=data)
        self.assertRedirects(response, expected_url=reverse('ideas:home'))

    def test_redirect_authenticated_user_on_register(self):
        """Test whether a logged in user is redirected to home when trying to access register link"""
        login = self.client.login(username='tester', password='user123#')
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, expected_url=reverse('ideas:home'))

    def test_redirect_unauthenticated_user_on_profile(self):
        """Test whether a logged in user is redirected to home when trying to access register link"""
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, expected_url='/login/?next=/profile/')

    def test_profile_updation(self):
        """
        Test whether
            - profile urls loads successfully
            - correct template is used for rendering
            - data is updated successfully on post request
        """
        data = {
            'username': 'tester2',
            'first_name': 'Jachi',
            'last_name': 'karta',
            'email': 'jachkarta+test1@gmail.com',
            'password1': 'user1234#',
            'password2': 'user1234#',
        }
        url_profile = reverse('profile')
        login = self.client.login(username='tester', password='user123#')
        # Test GET request
        profile_get = self.client.get(url_profile)
        self.assertEqual(profile_get.status_code, 200)
        self.assertTemplateUsed(
            profile_get, template_name='users/profile.html')

        # Test POST request
        profile_post = self.client.post(url_profile, data=data)
        # Test HTTP response
        self.assertEqual(profile_post.status_code, 302)

        user = get_object_or_404(User, username=data['username'])

        # Test profile values
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.check_password(data['password1']), True)
