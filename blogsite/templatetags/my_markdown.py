import os
import markdown
import geoip2.database

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()
BLOG_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BLOG_BASE_DIR, "../static/")


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


@register.filter
def ipfilter(user_ip):
    img_html = "/static/flag/{}.svg"

    CITY_DB = os.path.join(STATIC_ROOT, "ip_db", "GeoLite2-City.mmdb")
    reader = geoip2.database.Reader(CITY_DB)
    try:
        response = reader.city(user_ip)

        user_country = response.country.iso_code.lower()
        user_city = response.city.name
        if user_city is None: user_city = "Unknown City"
    except:
        user_country = "Unknown"
        user_city = "Unknown City"

    return [{"country" : img_html.format(user_country), "city" : user_city}]

