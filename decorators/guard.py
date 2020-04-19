from django.http import Http404
from functools import wraps

def require_superuser(func):
    """Redirects non superusers to a 404 page"""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404

        return func(request, *args, **kwargs)
        # return user_passes_test(func)

    return wrapper