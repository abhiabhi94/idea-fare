"""General purpose functions that provide utility throughout the application"""
from django.apps import apps
from django.contrib.contenttypes.models import ContentType


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
    Idea = apps.get_model('ideas', 'Idea')
    return Idea.objects.filter(visibility=True).latest('date_created').date_created


def get_content_type(model_obj):
    return ContentType.objects.get_for_model(model_obj.__class__)


def get_model_object(*, app_name, model_name, model_id):
    """
    Get content object.
    Args:
        app_name (str): name of the app that contains the model.
        model_name (str): name of the model class.
        model_id (int): the id of the model object.

    Returns:
        object: model object according to the parameters passed
    """
    content_type = ContentType.objects.get(app_label=app_name, model=model_name.lower())
    model_object = content_type.get_object_for_this_type(id=model_id)

    return model_object
