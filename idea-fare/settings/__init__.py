import os
import json
import sys

# Just a hack to find wayaround relative imports
sys.path.append('...')
from setup.setup import *  # nopep8

if prod_flag is not None:  # production
    from .prod import *
else:  # development
    from .dev import *

SECRET_KEY = secret_key

##### For MySQL use this ########################

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

##### For sqlite you use this ###############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#############################################
