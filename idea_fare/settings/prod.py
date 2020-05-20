from .base import *

DEBUG = False
ALLOWED_HOSTS = ['mysite.com', 'my.web.site.ip.', 'www.mysite.com', ]

# Enable only if you shift to HTTPS from HTTP
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True  # makes it difficult to hijack user sessions

# prevent the browser from identifying content types incorrectly
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True  # prevents XSS attacks
SECURE_SSL_REDIRECT = True  # Redirect connections to HTTPS

# makes it difficult for network traffic sniffers to steal CSRF token
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True  # submit your website to the browser preload list
SECURE_HSTS_SECONDS = 3600  # 1 hour. Refuses to connect over HTTP
SECURE_HSTS_INCLUDE_SUBDOMAINS = True


STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

########### Integrating sentry sdk inside django #########

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# sentry_sdk.init(
#     dsn="api-key",
#     integrations=[DjangoIntegration()],

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )

##################################################################
