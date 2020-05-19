"""General purpose functions that provide utility throughout the application"""
from ideas.models import Idea

def process_idea_form(request, form):
    """
    Returns
        form: obj
            The processed form
    Args
        request: WSGIRequest
            The incoming request object

        form: IdeaForm
            The form to be processed
    """
    if not (request.POST.get('anonymous', True) == 'anonymous'):  # Non-anonymous ideas
        if request.user.is_authenticated:
            # For authenticated users
            form.instance.user = request.user

    return form

def latest_entry(request):
    """
    Returns
        date: date-time
            The date time of the latest public idea posted.
    """
    return Idea.objects.filter(visibility=True).latest('date_created').date_created
