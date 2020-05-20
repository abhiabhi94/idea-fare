"""Reads the contents from the environment variable of the\
    virtual environment for setting up the project"""
import os
import sys

project_name = os.getenv('NAME')
if project_name is None:
    sys.exit('Add an environment variable NAME as the name of this project')

secret_key = os.getenv('SECRET_KEY')
if secret_key is None:
    sys.exit(
        'Add an environment variable SECRET_KEY as the secret key for this project')

email_host_user = os.getenv('EMAIL_USER')
email_host_pass = os.getenv('EMAIL_PASS')
if not (email_host_user) or (not email_host_pass):
    print('Warning: You will not be able to send any emails using this project')

recaptcha_private_key = os.getenv('RECAPTCHA_PRIVATE_KEY')
recaptcha_public_key = os.getenv('RECAPTCHA_PUBLIC_KEY')

prod_flag = os.getenv('PROD')
