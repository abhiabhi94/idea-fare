from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter(name='cool_num', is_safe=False)
def cool_num(val, precision=2):
    """
    Convert numbers to a cool format e.g: 1K, 123.4K, 111.42M.
    Returns:
        str
            e.g: 1K, 123.4K, 111.42M

    Params:
        val: int
            The value of view
        precision: int
            The precision demanded
    """

    try:
        int_val = int(val)
    except ValueError:
        raise template.TemplateSyntaxError(
            _(f'Value must be an integer. {val} is not an integer'))
    if int_val < 1000:
        return str(int_val)
    elif int_val < 1_000_000:
        return f'{ int_val/1000.0:.{precision}f}'.rstrip('0').rstrip('.') + 'K'
    else:
        return f'{int_val/1_000_000.0:.{precision}f}'.rstrip('0').rstrip('.') + 'M'
