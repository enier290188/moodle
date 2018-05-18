# -*- coding: utf-8 -*-
from . import views
from django.conf.urls import url

urlpatterns = [
    url(regex=r'^$', view=views.index, name='index'),
    url(regex=r'^table_tbody_and_pagination_reload/$', view=views.table_tbody_and_pagination_reload, name='table_tbody_and_pagination_reload'),
    url(regex=r'^detail/(?P<pk>\d+)/$', view=views.detail, name='detail'),
    url(regex=r'^approve/(?P<pk>\d+)/$', view=views.approve, name='approve'),
    url(regex=r'^disapprove/(?P<pk>\d+)/$', view=views.disapprove, name='disapprove'),
]
