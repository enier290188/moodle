# -*- coding: utf-8 -*-
from django.conf.urls import include, url

urlpatterns = [
    url(r'^document/', include('src.administration.module.documentation.document.urls', namespace='document')),
]
