from django import template
import re

register = template.Library()

@register.filter(name='remove_html_tags')
def remove_html_tags(raw_html):
    if raw_html:
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        clean_html = re.sub(cleanr, '', raw_html)
        return clean_html
    
    return ''

@register.filter(name='country_icon_url')
def country_icon_url(code): 
    print(code)
    if code: 
        return "https://www.countryflags.io/" + code + "/shiny/32.png"

    return "https://www.countryflags.io/gb/shiny/32.png"
