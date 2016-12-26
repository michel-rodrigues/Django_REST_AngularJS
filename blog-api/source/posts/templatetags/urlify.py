from urllib.parse import quote
from django import template

register = template.Library()

# 'quote' converte string em 'url-encoded text', um formato
# que pode ser enviado pela internet
# Ver post_detail.html, link do twitter


# O decorador possibilita usar a função como um filtro
# dentro de um template
@register.filter
def urlify(value):
    return quote(value)
