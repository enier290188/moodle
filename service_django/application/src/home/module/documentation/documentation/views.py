# -*- coding: utf-8 -*-
from .... import utils as home_utils
from src.documentation import models as documentation_models
from src.security import (
    decorators as security_decorators,
    utils as security_utils,
)
from django import http


@security_decorators.required_request_is_ajax()
@security_decorators.required_security_user(security_from_module=security_utils.SECURITY_FROM_MODULE_HOME)
def index(request):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    data['HTML_DIV_CENTER_DIV_CONTENT'] = home_utils.html_template(
        request=request,
        context=dict(),
        template='home/_include_/div_center/div_content/documentation/documentation/div_content.html',
    )
    return http.JsonResponse(data)


@security_decorators.required_request_is_ajax()
@security_decorators.required_security_user(security_from_module=security_utils.SECURITY_FROM_MODULE_HOME)
def tree(request):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    instances = documentation_models.Document.objects.all().filter(is_active=True)
    data['HTML_DIV_CENTER_DIV_CONTENT_DOCUMENTATION_DOCUMENTATION_TREE'] = home_utils.html_template(
        request=request,
        context={
            'ctx_instances': instances,
        },
        template='home/_include_/div_center/div_content/documentation/documentation/_include_/tree.html',
    )
    return http.JsonResponse(data)


@security_decorators.required_request_is_ajax()
@security_decorators.required_security_user(security_from_module=security_utils.SECURITY_FROM_MODULE_HOME)
def content(request, pk):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    try:
        pk = int(pk)
    except ValueError:
        return home_utils.jsonresponse_error(request=request)
    if pk > 0:
        instance = documentation_models.Document.objects.instance___by_pk(pk=pk)
        if instance is None:
            return home_utils.jsonresponse_error(request=request)
        context = {
            'ctx_title': instance,
            'ctx_content': instance.string___content(),
        }
    else:
        instances = documentation_models.Document.objects.all().filter(is_active=True)
        if instances.count() > 0:
            instance = instances[0]
            context = {
                'ctx_title': instance,
                'ctx_content': instance.string___content(),
            }
        else:
            context = dict()
    data['HTML_DIV_CENTER_DIV_CONTENT_DOCUMENTATION_DOCUMENTATION_CONTENT'] = home_utils.html_template(
        request=request,
        context=context,
        template='home/_include_/div_center/div_content/documentation/documentation/_include_/content.html',
    )
    return http.JsonResponse(data)
