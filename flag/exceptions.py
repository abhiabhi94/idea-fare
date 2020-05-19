"""Application wide exceptions"""

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


## Most of this code is copied from django-contrib-comments
class FlagBadRequest(HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.

    The Response are translated.
    """

    def __init__(self, why):
        super().__init__()
        if settings.DEBUG:
            self.content = render_to_string("flag/400-debug.html", {"why": _(why)})
