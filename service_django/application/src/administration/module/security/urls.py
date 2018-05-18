# -*- coding: utf-8 -*-
from django.conf.urls import include, url

urlpatterns = [
    url(r'^requestedlocaluser/', include('src.administration.module.security.requestedlocaluser.urls', namespace='requestedlocaluser')),
    url(r'^localuser/', include('src.administration.module.security.localuser.urls', namespace='localuser')),
    url(r'^requestedldapuser/', include('src.administration.module.security.requestedldapuser.urls', namespace='requestedldapuser')),
    url(r'^ldapuser/', include('src.administration.module.security.ldapuser.urls', namespace='ldapuser')),
    url(r'^group/', include('src.administration.module.security.group.urls', namespace='group')),
    url(r'^permission/', include('src.administration.module.security.permission.urls', namespace='permission')),
]
