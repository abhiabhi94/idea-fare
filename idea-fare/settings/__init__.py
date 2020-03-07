import os
import json
import sys

# Just a hack to find wayaround relative imports
sys.path.append('...')
from setup.setup import CONFIG_FILE  # nopep8

try:
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
        config['PROD']

    from .prod import *


except KeyError:
    from .dev import *

SECRET_KEY = config['SECRET_KEY']

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
