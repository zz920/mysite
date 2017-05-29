import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def my_markdown(value):
    return mark_safe(
        markdown.markdown(
            value,
            extensions=['markdown.extensions.fenced_code',
                'markdown.extensions.codehilite'],
            safe_mode=True,
            enable_attributes=False
        )
    )


@register.filter
def plural(num, text):

    if num > 1:
        text = text + 's'
    return text.format(num)

