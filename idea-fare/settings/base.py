import os
import json
import sys

# Just a hack to find wayaround relative imports
sys.path.append('...')
from setup.setup import project_name, email_host_user, email_host_pass   # nopep8

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    # This is to override the jquery.init.js script provided by the admin, 
    # which sets up jQuery with noConflict, making jQuery available in django.jQuery only and not $.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    ##############################
    'meta',
    'crispy_forms',
    'fluent_comments',
    'django_comments',
    'threadedcomments',
    'taggit',
    'snowpenguin.django.recaptcha3',
    ################################
    'users',
    'ideas',
    'subscribers',
    ################################
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{}.urls'.format(project_name)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{}.wsgi.application'.format(project_name)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = 'ideas:home'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# for using the sites framework
SITE_ID = 1

############## Used by Django-Meta app for rendering meta tags #############
META_SITE_DOMAIN = ''
META_SITE_PROTOCOL = 'http'
################################################################

# set up variables to be used for sending emails
if email_host_user is not None:
    EMAIL_HOST_USER = email_host_user
    EMAIL_HOST_PASSWORD = email_host_pass

##########################################################################

############# django_fluent_comments######################################
COMMENTS_APP = 'fluent_comments'
FLUENT_COMMENTS_FORM_CLASS = 'ideas.forms.CommentForm'
FLUENT_COMMENTS_EXCLUDE_FIELDS = ('url', 'title')

###############################################################################

################ Django-taggit############################
TAGGIT_CASE_INSENSITIVE = True

##############################################################################

################ Django-recaptcha3############################
RECAPTCHA_PRIVATE_KEY = '6LcYvOMUAAAAALY7HbPDdAUguUmtIbunESCd8RsS'
RECAPTCHA_PUBLIC_KEY = '6LcYvOMUAAAAAPY-6-3kAELFXZ-ZA6jLH9XAW6St'
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.5

##############################################################################
