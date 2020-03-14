"""Reads the contents from the environment variable of the\
    virtual environment for setting up the project"""
import os


project_name = os.getenv('NAME')
secret_key = os.getenv('SECRET_KEY')
email_host_user = os.getenv('EMAIL_USER')
email_host_pass = os.getenv('EMAIL_PASS')
prod_flag = os.getenv('PROD', None)
