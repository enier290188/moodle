# -*- coding: utf-8 -*-
from django.conf.urls import include, url

urlpatterns = [
    url(r'^documentation/', include('src.home.module.documentation.documentation.urls', namespace='documentation')),
]
