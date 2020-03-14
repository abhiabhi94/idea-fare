"""Reads the contents from the environment variable of the\
    virtual environment for setting up the project"""
import os
import sys


project_name = os.getenv('NAME', None)
if project_name is None:
    sys.exit('Add an environment variable NAME as the name of this project')

secret_key = os.getenv('SECRET_KEY')
if secret_key is None:
    sys.exit(
        'Add an environment variable SECRET_KEY as the secret key for this project')

email_host_user = os.getenv('EMAIL_USER', None)
email_host_pass = os.getenv('EMAIL_PASS', None)
if email_host_user is None or email_host_pass is None:
    print('You will not be able to send any emails using this project')

prod_flag = os.getenv('PROD', None)
