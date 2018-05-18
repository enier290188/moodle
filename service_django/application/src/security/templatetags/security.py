# -*- coding: utf-8 -*-
from src.security import models
from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags import staticfiles
from django.utils import timezone

register = template.Library()


@register.filter()
def boolean___not(boolean):
    return not boolean


@register.filter()
def string___title(request):
    return '-%s' % (settings.LDAP_SERVER_GROUPS_GROUP_CN,)


@register.filter()
def boolean___is_not_security_user_equal_none(request):
    if request.SECURITY_USER is not None:
        return True
    return False


@register.filter()
def boolean___has_permission_security_user(request, string___identifiers_to_verify):
    if boolean___is_not_security_user_equal_none(request=request):
        set_identifier___to_verify = set(' '.join(string___identifiers_to_verify.split()).split())  # delete space
        if request.SECURITY_USER.is_superuser is True or request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify=set_identifier___to_verify):
            return True
    return False


@register.filter()
def boolean___is_security_user_localuser(request):
    if boolean___is_not_security_user_equal_none(request=request):
        if isinstance(request.SECURITY_USER, models.LOCALUser):
            return True
    return False


@register.filter()
def boolean___is_security_user_ldapuser(request):
    if boolean___is_not_security_user_equal_none(request=request):
        if isinstance(request.SECURITY_USER, models.LDAPUser):
            return True
    return False


@register.filter()
def instance___security_user(request):
    return request.SECURITY_USER


@register.filter()
def string___security_user_url_current(request):
    return request.session['SECURITY_USER_URL_CURRENT']


@register.filter()
def string___security_user_avatar_url(request):
    string___avatar_url = staticfiles.static('_images_/security/avatar.png')
    if request.SECURITY_USER is not None and request.SECURITY_USER.avatar:
        string___avatar_url = request.SECURITY_USER.avatar.url
    return '%s?%s' % (string___avatar_url, timezone.datetime.now().strftime("%Y%m%d%H%M%S"))


@register.filter()
def string___security_user_by_instance_avatar_url(instance):
    string___avatar_url = staticfiles.static('_images_/security/avatar.png')
    if instance is not None and instance.avatar:
        string___avatar_url = instance.avatar.url
    return '%s?%s' % (string___avatar_url, timezone.datetime.now().strftime("%Y%m%d%H%M%S"))


@register.filter()
def boolean___show_the_administration_link(request):
    if boolean___is_not_security_user_equal_none(request=request):
        if request.SECURITY_USER.is_superuser is True:
            return True
        if request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify={'security_requestedlocaluser_list', }):
            return True
        if request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify={'security_localuser_list', }):
            return True
        if request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify={'security_requestedldapuser_list', }):
            return True
        if request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify={'security_ldapuser_list', }):
            return True
        if request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify={'security_importedldapuser_list', }):
            return True
        if request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify={'security_group_list', }):
            return True
        if request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify={'security_permission_list', }):
            return True
        if request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify={'documentation_document_list', }):
            return True
    return False
