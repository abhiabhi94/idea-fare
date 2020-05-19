from django import template
from django.contrib.contenttypes.models import ContentType

from flag.models import FlagInstance


register = template.Library()


@register.inclusion_tag("flag/flag_form.html", takes_context=True)
def render_flag_form(context, content_object, creator_field):
    """
    A template tag used for adding flag form in templates

    To render the flag form for a idea model with creator field as 'conceiver'

    Usage: `{% render_flag_form for ideas 'conceiver' %}`
    """
    content_type = ContentType.objects.get(
        app_label=content_object._meta.app_label,
        model=content_object._meta.model_name
    )
    request = context["request"]
    return {
        "content_type": content_type.id,
        "object_id": content_object.id,
        "creator_field": creator_field,
        "request": request,
        "user": request.user,
        "flag_reasons": FlagInstance.reasons
    }
