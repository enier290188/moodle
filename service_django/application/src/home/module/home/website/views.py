# -*- coding: utf-8 -*-
from .... import utils as home_utils
from src.security import (
    decorators as security_decorators,
)
from django import http


@security_decorators.required_request_is_ajax()
def index(request):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    data['HTML_DIV_CENTER_DIV_CONTENT'] = home_utils.html_template(
        request=request,
        context=dict(),
        template='home/_include_/div_center/div_content/home/website/div_content.html',
    )
    return http.JsonResponse(data)
