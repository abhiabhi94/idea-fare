from tests.base import TestBase
from utils.validators import email_verification


class TestValidators(TestBase):

    def test_email_verification_for_bogus_emails(self):
        """Test email verification for bogus emails"""
        test_data = ['ab@ab.com']
        for data in test_data:
            self.assertEqual(False, email_verification(data))

    def test_email_verification_for_true_emails(self):
        """Test email verification for true emails"""
        test_data = self.valid_emails
        for data in test_data:
            self.assertEqual(True, email_verification(data))
