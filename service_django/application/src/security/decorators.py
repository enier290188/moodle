# -*- coding: utf-8 -*-
from . import ldap, models, utils
from django import http, shortcuts
from django.contrib import messages
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _


def jsonresponse_not_permission(request, security_from_module):
    if request.is_ajax():
        data = dict()
        data['BOOLEAN_ERROR'] = True
        messages.add_message(request, messages.ERROR, _('SECURITY_MESSAGE Action not performed, you do not have permission.'))
        data['HTML_DIV_MODAL'] = utils.html_template_div_modal_message(request=request, security_from_module=security_from_module)
        data['HTML_DIV_MODAL_MESSAGE'] = utils.html_template_div_modal_message_message(request=request, security_from_module=security_from_module)
        data['HTML_DIV_MODAL_MODAL'] = utils.html_template_div_modal_modal_message(request=request, security_from_module=security_from_module)
        data['HTML_DIV_MODAL_MODAL_MESSAGE'] = utils.html_template_div_modal_modal_message_message(request=request, security_from_module=security_from_module)
        data['BOOLEAN_WITHOUT_PERMISSION'] = True
        data['URL_REDIRECT'] = urlresolvers.reverse(utils.SECURITY_USER_URL_REVERSE)
        return http.JsonResponse(data)
    else:
        return shortcuts.redirect(urlresolvers.reverse(utils.SECURITY_USER_URL_REVERSE))


def required_request_is_ajax(function=None):
    def _decorator(view_func):
        def _view(request, *args, **kwargs):
            if request.is_ajax():
                return view_func(request, *args, **kwargs)
            return shortcuts.redirect(urlresolvers.reverse(utils.SECURITY_USER_URL_REVERSE))

        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def required_security_user(function=None, security_from_module=''):
    def _decorator(view_func):
        def _view(request, *args, **kwargs):
            if request.SECURITY_USER is not None:
                return view_func(request, *args, **kwargs)
            return jsonresponse_not_permission(request=request, security_from_module=security_from_module)

        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def required_security_user_has_permission(function=None, security_from_module='', set_identifier___to_verify=set()):
    def _decorator(view_func):
        @required_security_user(security_from_module=security_from_module)
        def _view(request, *args, **kwargs):
            if request.SECURITY_USER.is_superuser is True or request.SECURITY_USER.boolean___has_permission(set_identifier___to_verify=set_identifier___to_verify):
                return view_func(request, *args, **kwargs)
            return jsonresponse_not_permission(request=request, security_from_module=security_from_module)

        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def required_security_user_is_localuser(function=None, security_from_module=''):
    def _decorator(view_func):
        @required_security_user()
        def _view(request, *args, **kwargs):
            if isinstance(request.SECURITY_USER, models.LOCALUser):
                return view_func(request, *args, **kwargs)
            return jsonresponse_not_permission(request=request, security_from_module=security_from_module)

        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def required_security_user_is_ldapuser(function=None, security_from_module=''):
    def _decorator(view_func):
        @required_security_user()
        def _view(request, *args, **kwargs):
            if isinstance(request.SECURITY_USER, models.LDAPUser):
                return view_func(request, *args, **kwargs)
            return jsonresponse_not_permission(request=request, security_from_module=security_from_module)

        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def required_ldap_connection(function=None, security_from_module=''):
    def _decorator(view_func):
        def _view(request, *args, **kwargs):
            boolean___is_there_connection = False
            connection = ldap.connection___ldap()
            try:
                # start the connection
                if connection.bind():
                    boolean___is_there_connection = True
            except (Exception,):
                pass
            finally:
                # close the connection
                connection.unbind()
            if boolean___is_there_connection is False:
                data = dict()
                data['BOOLEAN_ERROR'] = True
                messages.add_message(request, messages.ERROR, _('SECURITY_MESSAGE Action not performed, connection to the LDAP could not be established.'))
                data['HTML_DIV_MODAL'] = utils.html_template_div_modal_message(request=request, security_from_module=security_from_module)
                data['HTML_DIV_MODAL_MESSAGE'] = utils.html_template_div_modal_message_message(request=request, security_from_module=security_from_module)
                return http.JsonResponse(data)
            else:
                return view_func(request, *args, **kwargs)

        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)
