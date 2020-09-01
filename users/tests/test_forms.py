from unittest.mock import patch

from tests.base import TestBase
from users.forms import UserRegisterForm


class UserRegistrationFormTest(TestBase):

    @patch('utils.validators.is_email_valid')
    def test_email_invalidates_dummy_emails(self, mocked_attr):
        """Test whether email field invalidates dummy emails and raises a validation error"""
        mocked_attr.return_value = False
        field = 'email'
        data = 'ab@ab.com'
        form = UserRegisterForm(data={field: data})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.has_error(field, code='invalid'),
            True,
            msg=f'Are you sure %{data} is a valid email address? We suspect you made a typing error')

    def test_first_name_alphabetic(self):
        """Test whether first name invalidates non alphabets and raises a validation error"""
        field = 'first_name'
        data = 'Bulb2'

        form_1 = UserRegisterForm(data={field: data})
        self.assertFalse(form_1.is_valid())
        self.assertEqual(
            form_1.has_error(field, code='invalid'),
            True,
            msg=f'Are you sure {data} is a valid name. Names can only have alphabets.')

        form_2 = UserRegisterForm(data={field: '$Bulb_'})
        self.assertFalse(form_2.is_valid())
        self.assertEqual(
            form_2.has_error(field, code='invalid'),
            True,
            msg=f'Are you sure {data} is a valid name. Names can only have alphabets.')

    def test_last_name_alphabetic(self):
        """
        Test whether last name either accepts
            - accepts blank value
            - invalidates non alphabet values
                raises a validation error if it fails
        """
        field = 'last_name'
        data = ''
        form_1 = UserRegisterForm(data={field: data})

        self.assertFalse(form_1.is_valid())

        data = 'Bulb2'
        form_2 = UserRegisterForm(data={field: data})

        self.assertFalse(form_2.is_valid())
        self.assertEqual(
            form_2.has_error(field, code='invalid'),
            True,
            f'Are you sure {data} is a valid name. Names can only have alphabets.')

        data = '$Bulb_'
        form_3 = UserRegisterForm(data={field: data})
        self.assertFalse(form_3.is_valid())
        self.assertEqual(
            form_3.has_error(field, code='invalid'),
            True,
            msg=f'Are you sure {data} is a valid name. Names can only have alphabets.')

    def test_username_anonymous_is_not_allowed(self):
        """Test whether email field invalidates dummy emails and raises a validation error"""
        field = 'username'

        form = UserRegisterForm(data={field: 'anonymous'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.has_error(field, code='invalid'), True, msg='This username is already taken')
