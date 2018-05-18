# -*- coding: utf-8 -*-
from . import views
from django.conf.urls import include, url

urlpatterns = [
    url(regex=r'^$', view=views.index, name='index'),
    url(regex=r'^title/$', view=views.title, name='title'),
    url(regex=r'^div_load/$', view=views.div_load, name='div_load'),
    url(regex=r'^div_header/$', view=views.div_header, name='div_header'),
    url(regex=r'^div_leftside/$', view=views.div_leftside, name='div_leftside'),
    url(regex=r'^div_center_div_content/$', view=views.div_center_div_content, name='div_center_div_content'),
    url(regex=r'^div_center_div_footer/$', view=views.div_center_div_footer, name='div_center_div_footer'),
    #
    url(regex=r'^login/$', view=views.login, name='login'),
    url(regex=r'^login_forgot_credential_1/$', view=views.login_forgot_credential_1, name='login_forgot_credential_1'),
    url(regex=r'^login_forgot_credential_2/(?P<pk>\d+)/$', view=views.login_forgot_credential_2, name='login_forgot_credential_2'),
    url(regex=r'^login_forgot_credential_3/(?P<pk>\d+)/$', view=views.login_forgot_credential_3, name='login_forgot_credential_3'),
    url(regex=r'^login_request/$', view=views.login_request, name='login_request'),
    url(regex=r'^logout/$', view=views.logout, name='logout'),
    url(regex=r'^profile/$', view=views.profile, name='profile'),
    url(regex=r'^locale/$', view=views.locale, name='locale'),
    #
    url(r'^module/', include('src.home.module.urls', namespace='module')),
]
