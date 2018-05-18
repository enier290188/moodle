# -*- coding: utf-8 -*-
from django.conf.urls import include, url

urlpatterns = [
    url(r'^security/', include('src.administration.module.security.urls', namespace='security')),
    url(r'^documentation/', include('src.administration.module.documentation.urls', namespace='documentation')),
]
