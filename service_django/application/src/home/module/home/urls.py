# -*- coding: utf-8 -*-
from django.conf.urls import include, url

urlpatterns = [
    url(r'^website/', include('src.home.module.home.website.urls', namespace='website')),
]
