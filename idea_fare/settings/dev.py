import sys
import urllib.request
from subprocess import getoutput
from urllib.error import URLError

from .base import * # noqa

global ALLOWED_HOSTS
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# For Debug Toolbar ##########
INSTALLED_APPS += ['debug_toolbar']     # noqa: F405
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']   # noqa: F405
INTERNAL_IPS = ALLOWED_HOSTS
##################################


def add_ip_to_host(port=8000):
    """
    Adds local IPv4 and public IP addresses to ALLOWED_HOST

    Returns
        None

    Args:
        port:int
        port which will handle the request
    """

    IP_PRIVATE = getoutput('hostname -I').strip().split()
    try:
        IP_PUBLIC = urllib.request.urlopen(
            'https://ident.me').read().decode('utf8')
        ALLOWED_HOSTS.append(IP_PUBLIC)

    except URLError:
        print('Not connected to internet, the developement server will not be accessible from outside')

    finally:
        ALLOWED_HOSTS.extend(IP_PRIVATE)
        print('You may connect at any of the following:')
        [print(f'http://{i}:{port}') for i in ALLOWED_HOSTS]
        # Just add a blank file after the allowed addresses
        print()


try:
    host = sys.argv[2]
    if '0.0.0.0' in host:
        add_ip_to_host(port=host.split(':')[-1])
except IndexError:
    pass


DEBUG = True
