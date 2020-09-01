from unittest.mock import patch

from tests.base import TestBase
from utils import validators


class TestValidators(TestBase):
    @patch('utils.validators.is_email_valid')
    def test_email_verification_for_bogus_emails(self, mocked_attr):
        mocked_attr.return_value = False
        """Test email verification for bogus emails"""
        test_data = ['ab@ab.com']
        for data in test_data:
            self.assertEqual(False, validators.is_email_valid(data))

    @patch('utils.validators.is_email_valid')
    def test_email_verification_for_true_emails(self, mocked_attr):
        """Test email verification for true emails"""
        mocked_attr.return_value = True
        test_data = [self.get_email() for i in range(3)]
        for data in test_data:
            self.assertEqual(True, validators.is_email_valid(data))
