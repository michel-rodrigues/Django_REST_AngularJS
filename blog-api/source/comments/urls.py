from django.conf.urls import url

from .views import (
    comments_thread,
    comment_delete,
    )

urlpatterns = [
    url(r'^(?P<id>\d+)/$', comments_thread, name='thread'),
    url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]

