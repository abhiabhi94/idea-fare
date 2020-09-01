"""General purpose useful validators"""
from validate_email import validate_email


def is_email_valid(email):
    """
    Verify whether an email is legit or not.
    `This feature works only when the Internet connection is alive`.

    Args
        email: str
            The email to be verified

    Returns
        bool
    """
    result = validate_email(email_address=email, check_regex=True, check_mx=True)
    if result is (None or True):
        return True
    return False
