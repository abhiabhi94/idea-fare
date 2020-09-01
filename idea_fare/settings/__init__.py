# flake8: noqa
import os
import sys

from config.config import *

# Just a hack to find wayaround relative imports
sys.path.append('...')

if prod_flag is not None:  # production
    from .prod import *
else:  # development
    from .dev import *

SECRET_KEY = secret_key

# For MySQL use this ########################

# DB_CONFIG_FILE = '/etc/db.cnf'
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': DB_CONFIG_FILE,
#         },
#     }
# }

########################################################

# For sqlite, use this ###############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#############################################
