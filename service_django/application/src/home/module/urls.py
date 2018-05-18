# -*- coding: utf-8 -*-
from django.conf.urls import include, url

urlpatterns = [
    url(r'^home/', include('src.home.module.home.urls', namespace='home')),
    url(r'^documentation/', include('src.home.module.documentation.urls', namespace='documentation')),
]
