# -*- coding: utf-8 -*-
from . import views
from django.conf.urls import url

urlpatterns = [
    url(regex=r'^$', view=views.index, name='index'),
    url(regex=r'^tree/$', view=views.tree, name='tree'),
    url(regex=r'^content/(?P<pk>\d+)/$', view=views.content, name='content'),
]
