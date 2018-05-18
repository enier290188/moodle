# -*- coding: utf-8 -*-
from .... import utils as administration_utils
from .. import utils as administration_module_utils
from . import utils as administration_module_model_utils
from src.security import (
    decorators as security_decorators,
    utils as security_utils
)


@security_decorators.required_request_is_ajax()
def index(request):
    return administration_utils.jsonresponse_template_div_center_div_content(
        request=request,
        utils_module=administration_module_utils,
        utils_module_model=administration_module_model_utils
    )


@security_decorators.required_request_is_ajax()
@security_decorators.required_security_user_has_permission(
    security_from_module=security_utils.SECURITY_FROM_MODULE_ADMINISTRATION,
    set_identifier___to_verify={'security_permission_list', }
)
def table_tbody_and_pagination_reload(request):
    return administration_utils.jsonresponse_template_div_center_div_content_table_tbody_and_pagination_reload(
        request=request,
        utils_module=administration_module_utils,
        utils_module_model=administration_module_model_utils
    )


@security_decorators.required_request_is_ajax()
@security_decorators.required_security_user_has_permission(
    security_from_module=security_utils.SECURITY_FROM_MODULE_ADMINISTRATION,
    set_identifier___to_verify={'security_permission_list', 'security_permission_detail', }
)
def detail(request, pk):
    return administration_utils.jsonresponse_template_div_modal_detail(
        request=request,
        utils_module=administration_module_utils,
        utils_module_model=administration_module_model_utils,
        pk=pk
    )


@security_decorators.required_request_is_ajax()
@security_decorators.required_security_user_has_permission(
    security_from_module=security_utils.SECURITY_FROM_MODULE_ADMINISTRATION,
    set_identifier___to_verify={'security_permission_list', 'security_permission_update', }
)
def update(request, pk):
    return administration_utils.jsonresponse_template_div_modal_update(
        request=request,
        utils_module=administration_module_utils,
        utils_module_model=administration_module_model_utils,
        pk=pk
    )
