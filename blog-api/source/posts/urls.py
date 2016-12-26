from django.conf.urls import url


# 17/01/2015
# Método para urls no Django 1.10 (Ainda não está na documentação,
# pois essa versão ainda não foi lançada)
from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    )

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]

# urlpatterns = [
#     url(r'^create/$', "posts.views.post_create"),
#     url(r'^detail/$', "posts.views.post_detail"),
#     url(r'^list/$', "posts.views.post_list"),
#     url(r'^update/$', "posts.views.post_update"),
#     url(r'^delete/$', "posts.views.post_delete"),
# ]
#
# Aviso que o Django 1.9 emite:
#
# RemovedInDjango110Warning: Support for string view arguments
# to url() is deprecated and will be removed in Django 1.10
# (got posts.views.post_delete). Pass the callable instead.
