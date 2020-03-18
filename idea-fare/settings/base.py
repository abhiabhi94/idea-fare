import os
import json
import sys

# Just a hack to find wayaround relative imports
sys.path.append('...')
from setup.setup import project_name  # nopep8

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
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
    'django_comments_xtd',
    'django_comments',
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

### Used by Django-Meta app for rendering meta tags ###
META_SITE_DOMAIN = ''
META_SITE_PROTOCOL = 'http'
##########################################

# Add '+contact' to email...for e.g source@example.com -> source+contact@example.com
CONTACT_EMAIL = os.environ.get('EMAIL_USER').replace('@', '+contact@')

#####################   django-comments-xtd ###########################
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order')
COMMENTS_XTD_FORM_CLASS = 'ideas.forms.CommentForm'
COMMENTS_XTD_MAX_THREAD_LEVEL = 20
COMMENTS_XTD_CONFIRM_EMAIL = True
#  To help obfuscating comments before they are sent for confirmation.
COMMENTS_XTD_SALT = (b"Timendi causa est nescire. "
                     b"Aequam memento rebus in arduis servare mentem.")

COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'ideas.idea': {
        'allow_flagging': True,
        'allow_feedback': True,
        'show_feedback': True,
    }
}

# Source mail address used for notifications.
COMMENTS_XTD_FROM_EMAIL = os.environ.get('EMAIL_USER')
# Contact mail address to show in messages.
COMMENTS_XTD_CONTACT_EMAIL = CONTACT_EMAIL
##########################################################################
