# -*- coding: utf-8 -*-
from django import http
from django.contrib import messages
from django.template import loader
from django.utils.translation import ugettext_lazy as _


def html_template(request, context, template):
    return loader.render_to_string(
        template_name=template,
        context=context,
        request=request
    )


def html_template_div_modal_message(request):
    return loader.render_to_string(
        template_name='home/_include_/div_modal/message/message.html',
        context={},
        request=request
    )


def html_template_div_modal_message_message(request):
    return loader.render_to_string(
        template_name='home/_include_/div_modal/_include_/message/message.html',
        context={
            'ctx_messages': messages.get_messages(request=request),
        },
        request=request
    )


def jsonresponse_error(request):
    if len(messages.get_messages(request=request)) <= 0:
        messages.add_message(request, messages.ERROR, _('HOME_MODULE_MESSAGE ERROR.'))
    data = dict()
    data['BOOLEAN_ERROR'] = True
    data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
    return http.JsonResponse(data)
