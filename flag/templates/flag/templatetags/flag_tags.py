from django import template

from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.inclusion_tag("flag/flag_form.html", takes_context=True)
def render_flag_form(context, content_object, creator_field):
    """
    A template tag used for adding flag form in templates

    Usage `{render_flag_form}`
    
    Parameters
    ----------
    context : [type]
        [description]
    content_object : [type]
        [description]
    creator_field : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """
    content_type = ContentType.objects.get(
        app_label=content_object._meta.app_label,
        model=content_object._meta.module_name
    )
    request = context["request"]
    return {
        "content_type": content_type.id,
        "object_id": content_object.id,
        "creator_field": creator_field,
        "request": request,
        "user": request.user,
    }