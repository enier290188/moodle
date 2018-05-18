# -*- coding: utf-8 -*-
from . import utils
from src.security import (
    decorators as security_decorators,
    utils as security_utils
)
from django import http, shortcuts


def index(request):
    context = dict()
    return shortcuts.render(
        request=request,
        context=context,
        template_name='home/application.html'
    )


@security_decorators.required_request_is_ajax()
def title(request):
    data = dict()
    data['HTML_TITLE'] = utils.html_template(
        request=request,
        context=dict(),
        template='home/_include_/title/title.html'
    )
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


@security_decorators.required_request_is_ajax()
def div_load(request):
    data = dict()
    data['HTML_DIV_LOAD'] = utils.html_template(
        request=request,
        context=dict(),
        template='home/_include_/div_load/div_load.html'
    )
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


@security_decorators.required_request_is_ajax()
def div_header(request):
    data = dict()
    data['HTML_DIV_HEADER'] = utils.html_template(
        request=request,
        context=dict(),
        template='home/_include_/div_header/div_header.html'
    )
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


@security_decorators.required_request_is_ajax()
def div_leftside(request):
    data = dict()
    data['HTML_DIV_LEFTSIDE'] = utils.html_template(
        request=request,
        context=dict(),
        template='home/_include_/div_leftside/div_leftside.html'
    )
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


@security_decorators.required_request_is_ajax()
def div_center_div_content(request):
    data = dict()
    data['HTML_DIV_CENTER_DIV_CONTENT'] = utils.html_template(
        request=request,
        context=dict(),
        template='home/_include_/div_center/div_content/div_content.html'
    )
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


@security_decorators.required_request_is_ajax()
def div_center_div_footer(request):
    data = dict()
    data['HTML_DIV_CENTER_DIV_FOOTER'] = utils.html_template(
        request=request,
        context=dict(),
        template='home/_include_/div_center/div_footer/div_footer.html'
    )
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


@security_decorators.required_request_is_ajax()
def login(request):
    return security_utils.jsonresponse_login(
        request=request,
        security_from_module=security_utils.SECURITY_FROM_MODULE_HOME
    )


@security_decorators.required_request_is_ajax()
def login_forgot_credential_1(request):
    return security_utils.jsonresponse_login_forgot_credential_1(
        request=request,
        security_from_module=security_utils.SECURITY_FROM_MODULE_HOME
    )


@security_decorators.required_request_is_ajax()
def login_forgot_credential_2(request, pk):
    return security_utils.jsonresponse_login_forgot_credential_2(
        request=request,
        security_from_module=security_utils.SECURITY_FROM_MODULE_HOME,
        pk=pk
    )


@security_decorators.required_request_is_ajax()
def login_forgot_credential_3(request, pk):
    return security_utils.jsonresponse_login_forgot_credential_3(
        request=request,
        security_from_module=security_utils.SECURITY_FROM_MODULE_HOME,
        pk=pk
    )


@security_decorators.required_request_is_ajax()
def login_request(request):
    return security_utils.jsonresponse_login_request(
        request=request,
        security_from_module=security_utils.SECURITY_FROM_MODULE_HOME
    )


@security_decorators.required_request_is_ajax()
@security_decorators.required_security_user(security_from_module=security_utils.SECURITY_FROM_MODULE_HOME)
def logout(request):
    return security_utils.jsonresponse_logout(
        request=request,
        security_from_module=security_utils.SECURITY_FROM_MODULE_HOME
    )


@security_decorators.required_request_is_ajax()
@security_decorators.required_security_user(security_from_module=security_utils.SECURITY_FROM_MODULE_HOME)
def profile(request):
    return security_utils.jsonresponse_profile(
        request=request,
        security_from_module=security_utils.SECURITY_FROM_MODULE_HOME
    )


@security_decorators.required_request_is_ajax()
def locale(request):
    return security_utils.jsonresponse_locale(
        request=request,
        security_from_module=security_utils.SECURITY_FROM_MODULE_HOME
    )
