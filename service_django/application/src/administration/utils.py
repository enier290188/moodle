# -*- coding: utf-8 -*-
from django import http
from django.contrib import messages
from django.core import paginator, urlresolvers
from django.template import loader
from django.utils.translation import ugettext_lazy as _
import copy


def html_template(request, context, template):
    return loader.render_to_string(
        template_name=template,
        context=context,
        request=request
    )


def html_template_div_modal_message(request):
    return loader.render_to_string(
        template_name='administration/_include_/div_modal/message/message.html',
        context={},
        request=request
    )


def html_template_div_modal_message_message(request):
    return loader.render_to_string(
        template_name='administration/_include_/div_modal/_include_/message/message.html',
        context={
            'ctx_messages': messages.get_messages(request=request),
        },
        request=request
    )


def html_template_div_modal(request, utils_module, utils_module_model, template_modal_path, form):
    return loader.render_to_string(
        template_name='administration/_include_/div_modal/administration/%s/%s/%s.html' % (utils_module.MODULE_PATH, utils_module_model.MODEL_PATH, template_modal_path,),
        context={
            'ctx_form': form,
        },
        request=request
    )


def html_template_div_center_div_content_table_tbody(request, utils_module, utils_module_model, page):
    return loader.render_to_string(
        template_name='administration/_include_/div_center/div_content/administration/%s/%s/_include_/tbody.html' % (utils_module.MODULE_PATH, utils_module_model.MODEL_PATH,),
        context={
            'ctx_page': page,
        },
        request=request
    )


def html_template_div_center_div_content_pagination(request, utils_module, utils_module_model, page):
    request_get___search = request.GET.get('search')
    if request_get___search is not None:
        request_get___search = ' '.join(request_get___search.split())
    else:
        request_get___search = ''
    return loader.render_to_string(
        template_name='administration/_include_/div_center/div_content/administration/_include_/pagination.html',
        context={
            'ctx_page': page,
            'ctx_url': urlresolvers.reverse('administration:module:%s:%s:table_tbody_and_pagination_reload' % (utils_module.MODULE_PATH, utils_module_model.MODEL_PATH,)),
            'ctx_search': request_get___search
        },
        request=request
    )


def jsonresponse_error(request):
    if len(messages.get_messages(request=request)) <= 0:
        messages.add_message(request, messages.ERROR, _('ADMINISTRATION_MODULE_MESSAGE ERROR.'))
    data = dict()
    data['BOOLEAN_ERROR'] = True
    data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
    return http.JsonResponse(data)


def jsonresponse_template_div_center_div_content(request, utils_module, utils_module_model):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    data['HTML_DIV_CENTER_DIV_CONTENT'] = html_template(
        request=request,
        context=dict(),
        template='administration/_include_/div_center/div_content/administration/%s/%s/div_content.html' % (utils_module.MODULE_PATH, utils_module_model.MODEL_PATH,)
    )
    return http.JsonResponse(data)


def jsonresponse_template_div_center_div_content_table_tbody_and_pagination_reload(request, utils_module, utils_module_model):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    search = list_instance___search(request=request, utils_module=utils_module, utils_module_model=utils_module_model)
    page = instance___page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, number_page=0, search=search)
    data['HTML_DIV_CENTER_DIV_CONTENT_TABLE_TBODY'] = html_template_div_center_div_content_table_tbody(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
    data['HTML_DIV_CENTER_DIV_CONTENT_PAGINATION'] = html_template_div_center_div_content_pagination(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
    return http.JsonResponse(data)


def jsonresponse_template_div_center_div_content_table_tbody_and_pagination_tree_reload(request, utils_module, utils_module_model):
    try:
        pk = int(request.GET.get('pk'))
        int___parent = int(request.GET.get('parent'))
        int___position = int(request.GET.get('position'))
    except ValueError:
        return jsonresponse_error(request=request)
    data = dict()
    instance = utils_module_model.MODEL.objects.instance(request=request, pk=pk)
    if instance is None:
        return jsonresponse_error(request=request)
    if int___parent < 0:
        return jsonresponse_error(request=request)
    instance_parent = None
    if 0 < int___parent:  # when int___parent==0: this instance have parent==null in the data base
        instance_parent = utils_module_model.MODEL.objects.instance(request=request, pk=int___parent)
        if instance_parent is None:
            return jsonresponse_error(request=request)
    instances = utils_module_model.MODEL.objects.instances(request=request)
    if not (0 < int___position <= len(instances)):
        return jsonresponse_error(request=request)
    # get parents of instance
    list_int___parent = []
    temporal_int___parent = instance.parent
    while temporal_int___parent != 0:
        list_int___parent.append(temporal_int___parent)
        temporal_instance___parent = utils_module_model.MODEL.objects.instance(request=request, pk=temporal_int___parent)
        temporal_int___parent = temporal_instance___parent.parent
    list_int___parent.append(0)
    # count children of the instance
    int___children_amount = 0
    for temporal_instance in instances[instance.position:]:
        if temporal_instance.parent in list_int___parent:
            break
        int___children_amount += 1
    # change positions
    if instance.position < int___position:
        for temporal_instance in instances[instance.position + int___children_amount:int___position + int___children_amount]:
            temporal_instance.position -= (1 + int___children_amount)
            temporal_instance.save()
        instances[instance.position - 1].parent = int___parent
        temporal_int___position = int___position
        for temporal_instance in instances[instance.position - 1:instance.position + int___children_amount]:
            temporal_instance.position = temporal_int___position
            temporal_int___position += 1
            temporal_instance.save()
    elif int___position < instance.position:
        instances[instance.position - 1].parent = int___parent
        temporal_int___position = int___position
        for temporal_instance in instances[instance.position - 1:instance.position + int___children_amount]:
            temporal_instance.position = temporal_int___position
            temporal_int___position += 1
            temporal_instance.save()
        for temporal_instance in instances[int___position - 1:instance.position - 1]:
            temporal_instance.position += (int___children_amount + 1)
            temporal_instance.save()
    else:  # instance.position == position
        instances[instance.position - 1].parent = int___parent
        instances[instance.position - 1].save()
    # change is_active
    if 0 < int___parent:  # when int___parent==0: this instance have parent==null in the data base
        if instance_parent.is_active is False and instance.is_active is True:
            instances = utils_module_model.MODEL.objects.instances(request=request)
            for temporal_instance in instances[int___position - 1:int___position + int___children_amount]:
                temporal_instance.is_active = False
                temporal_instance.save()
            data['LOCALE_IS_ACTIVE'] = dict()
            data['LOCALE_IS_ACTIVE']['option_no'] = '%s' % (_('ADMINISTRATION_MODULE_OPTION_NO'),)
    #
    if hasattr(utils_module_model, 'void___table_tbody_and_pagination_tree_reload'):
        instance = utils_module_model.MODEL.objects.instance(request=request, pk=pk)
        utils_module_model.void___table_tbody_and_pagination_tree_reload(request=request, data=data, instance=instance)
    #
    messages.add_message(request, messages.SUCCESS, _('ADMINISTRATION_MODULE_MESSAGE %(instance)s was successfully updated.') % {'instance': instance, })
    data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


def jsonresponse_template_div_modal_create(request, utils_module, utils_module_model):
    data = dict()
    if hasattr(utils_module_model, 'boolean___initial_create'):
        boolean___request = utils_module_model.boolean___initial_create(request=request, data=data)
        if boolean___request is False:
            return jsonresponse_error(request=request)
    form = utils_module_model.FORM_CREATE(data=request.POST or None, request=request)
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form.is_valid():
            instance = form.save(commit=True)
            search = list_instance___search(request=request, utils_module=utils_module, utils_module_model=utils_module_model)
            number_page = int___number_page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, pk=instance.pk)
            page = instance___page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, number_page=number_page)
            messages.add_message(request, messages.SUCCESS, _('ADMINISTRATION_MODULE_MESSAGE %(instance)s was successfully created.') % {'instance': instance, })
            data['BOOLEAN_IS_VALID_FORM'] = True
            data['HTML_DIV_CENTER_DIV_CONTENT_TABLE_TBODY'] = html_template_div_center_div_content_table_tbody(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
            data['HTML_DIV_CENTER_DIV_CONTENT_PAGINATION'] = html_template_div_center_div_content_pagination(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
            if request.GET.get('action-create-and-update') and request.GET.get('action-create-and-update') == 'active':
                instance_current = copy.deepcopy(instance)
                form = utils_module_model.FORM_UPDATE(data=None, files=None, request=request, instance=instance, instance_current=instance_current)
                data['HTML_DIV_MODAL'] = html_template_div_modal(request=request, utils_module=utils_module, utils_module_model=utils_module_model, template_modal_path='update', form=form)
                data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
                data['BOOLEAN_ERROR'] = False
                return http.JsonResponse(data)
            else:
                form = utils_module_model.FORM_CREATE(data=None, request=request)
        else:
            if form.errors.as_data().get('__all__') is not None:
                messages.add_message(request, messages.ERROR, form.errors['__all__'][0])
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    data['HTML_DIV_MODAL'] = html_template_div_modal(request=request, utils_module=utils_module, utils_module_model=utils_module_model, template_modal_path='create', form=form)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


def jsonresponse_template_div_modal_detail(request, utils_module, utils_module_model, pk):
    data = dict()
    try:
        pk = int(pk)
    except ValueError:
        return jsonresponse_error(request=request)
    instance = utils_module_model.MODEL.objects.instance(request=request, pk=pk)
    if instance is None:
        return jsonresponse_error(request=request)
    if hasattr(utils_module_model, 'boolean___initial_detail'):
        boolean___request = utils_module_model.boolean___initial_detail(request=request, data=data)
        if boolean___request is False:
            return jsonresponse_error(request=request)
    form = utils_module_model.FORM_DETAIL(data=None, request=request, instance=instance)
    if hasattr(form, 'detail'):
        form.detail()
    data['HTML_DIV_MODAL'] = html_template_div_modal(request=request, utils_module=utils_module, utils_module_model=utils_module_model, template_modal_path='detail', form=form)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


def jsonresponse_template_div_modal_update(request, utils_module, utils_module_model, pk):
    data = dict()
    try:
        pk = int(pk)
    except ValueError:
        return jsonresponse_error(request=request)
    instance = utils_module_model.MODEL.objects.instance(request=request, pk=pk)
    if instance is None:
        return jsonresponse_error(request=request)
    if hasattr(utils_module_model, 'boolean___initial_update'):
        boolean___request = utils_module_model.boolean___initial_update(request=request, data=data)
        if boolean___request is False:
            return jsonresponse_error(request=request)
    instance_current = copy.deepcopy(instance)
    form = utils_module_model.FORM_UPDATE(data=request.POST or None, files=request.FILES or None, request=request, instance=instance, instance_current=instance_current)
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form.is_valid():
            instance = form.save(commit=True)
            search = list_instance___search(request=request, utils_module=utils_module, utils_module_model=utils_module_model)
            number_page = int___number_page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, pk=instance.pk)
            page = instance___page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, number_page=number_page)
            messages.add_message(request, messages.SUCCESS, _('ADMINISTRATION_MODULE_MESSAGE %(instance)s was successfully updated.') % {'instance': instance, })
            data['BOOLEAN_IS_VALID_FORM'] = True
            data['HTML_DIV_CENTER_DIV_CONTENT_TABLE_TBODY'] = html_template_div_center_div_content_table_tbody(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
            data['HTML_DIV_CENTER_DIV_CONTENT_PAGINATION'] = html_template_div_center_div_content_pagination(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
        else:
            if form.errors.as_data().get('__all__') is not None:
                messages.add_message(request, messages.ERROR, form.errors['__all__'][0])
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    data['HTML_DIV_MODAL'] = html_template_div_modal(request=request, utils_module=utils_module, utils_module_model=utils_module_model, template_modal_path='update', form=form)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


def jsonresponse_template_div_modal_delete(request, utils_module, utils_module_model, pk):
    data = dict()
    try:
        pk = int(pk)
    except ValueError:
        return jsonresponse_error(request=request)
    instance = utils_module_model.MODEL.objects.instance(request=request, pk=pk)
    if instance is None:
        return jsonresponse_error(request=request)
    if hasattr(utils_module_model, 'boolean___initial_delete'):
        boolean___request = utils_module_model.boolean___initial_delete(request=request, data=data)
        if boolean___request is False:
            return jsonresponse_error(request=request)
    form = utils_module_model.FORM_DELETE(data=request.POST or None, request=request, instance=instance)
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form.is_valid():
            search = list_instance___search(request=request, utils_module=utils_module, utils_module_model=utils_module_model)
            number_page = int___number_page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, pk=instance.pk)
            if hasattr(form, 'delete'):
                form.delete()
            else:
                instance.delete()
            search = list_instance___search(request=request, utils_module=utils_module, utils_module_model=utils_module_model)
            page = instance___page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, number_page=number_page)
            messages.add_message(request, messages.SUCCESS, _('ADMINISTRATION_MODULE_MESSAGE %(instance)s was successfully deleted.') % {'instance': instance, })
            data['BOOLEAN_IS_VALID_FORM'] = True
            data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request)
            data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
            data['HTML_DIV_CENTER_DIV_CONTENT_TABLE_TBODY'] = html_template_div_center_div_content_table_tbody(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
            data['HTML_DIV_CENTER_DIV_CONTENT_PAGINATION'] = html_template_div_center_div_content_pagination(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
            data['BOOLEAN_ERROR'] = False
            return http.JsonResponse(data)
        else:
            if form.errors.as_data().get('__all__') is not None:
                messages.add_message(request, messages.ERROR, form.errors['__all__'][0])
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    data['HTML_DIV_MODAL'] = html_template_div_modal(request=request, utils_module=utils_module, utils_module_model=utils_module_model, template_modal_path='delete', form=form)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


def jsonresponse_template_div_modal_approve(request, utils_module, utils_module_model, pk):
    data = dict()
    try:
        pk = int(pk)
    except ValueError:
        return jsonresponse_error(request=request)
    instance = utils_module_model.MODEL.objects.instance(request=request, pk=pk)
    if instance is None:
        return jsonresponse_error(request=request)
    if hasattr(utils_module_model, 'boolean___initial_approve'):
        boolean___request = utils_module_model.boolean___initial_approve(request=request, data=data)
        if boolean___request is False:
            return jsonresponse_error(request=request)
    form = utils_module_model.FORM_APPROVE(data=request.POST or None, request=request, instance=instance)
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form.is_valid():
            if hasattr(form, 'approve'):
                instance_mirror = form.approve()
                messages.add_message(request, messages.SUCCESS, _('ADMINISTRATION_MODULE_MESSAGE %(instance)s was successfully approved.') % {'instance': instance_mirror, })
            else:
                return jsonresponse_error(request=request)
            search = list_instance___search(request=request, utils_module=utils_module, utils_module_model=utils_module_model)
            number_page = int___number_page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, pk=instance.pk)
            if hasattr(form, 'delete'):
                form.delete()
            else:
                instance.delete()
            search = list_instance___search(request=request, utils_module=utils_module, utils_module_model=utils_module_model)
            page = instance___page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, number_page=number_page)
            data['BOOLEAN_IS_VALID_FORM'] = True
            data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request)
            data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
            data['HTML_DIV_CENTER_DIV_CONTENT_TABLE_TBODY'] = html_template_div_center_div_content_table_tbody(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
            data['HTML_DIV_CENTER_DIV_CONTENT_PAGINATION'] = html_template_div_center_div_content_pagination(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
            data['BOOLEAN_ERROR'] = False
            return http.JsonResponse(data)
        else:
            if form.errors.as_data().get('__all__') is not None:
                messages.add_message(request, messages.ERROR, form.errors['__all__'][0])
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    data['HTML_DIV_MODAL'] = html_template_div_modal(request=request, utils_module=utils_module, utils_module_model=utils_module_model, template_modal_path='approve', form=form)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


def jsonresponse_template_div_modal_disapprove(request, utils_module, utils_module_model, pk):
    data = dict()
    try:
        pk = int(pk)
    except ValueError:
        return jsonresponse_error(request=request)
    instance = utils_module_model.MODEL.objects.instance(request=request, pk=pk)
    if instance is None:
        return jsonresponse_error(request=request)
    if hasattr(utils_module_model, 'boolean___initial_disapprove'):
        boolean___request = utils_module_model.boolean___initial_disapprove(request=request, data=data)
        if boolean___request is False:
            return jsonresponse_error(request=request)
    form = utils_module_model.FORM_DISAPPROVE(data=request.POST or None, request=request, instance=instance)
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form.is_valid():
            if hasattr(form, 'disapprove'):
                form.disapprove()
                messages.add_message(request, messages.SUCCESS, _('ADMINISTRATION_MODULE_MESSAGE %(instance)s was successfully disapproved.') % {'instance': instance, })
            else:
                return jsonresponse_error(request=request)
            search = list_instance___search(request=request, utils_module=utils_module, utils_module_model=utils_module_model)
            number_page = int___number_page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, pk=instance.pk)
            if hasattr(form, 'delete'):
                form.delete()
            else:
                instance.delete()
            search = list_instance___search(request=request, utils_module=utils_module, utils_module_model=utils_module_model)
            page = instance___page(request=request, utils_module=utils_module, utils_module_model=utils_module_model, search=search, number_page=number_page)
            data['BOOLEAN_IS_VALID_FORM'] = True
            data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request)
            data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
            data['HTML_DIV_CENTER_DIV_CONTENT_TABLE_TBODY'] = html_template_div_center_div_content_table_tbody(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
            data['HTML_DIV_CENTER_DIV_CONTENT_PAGINATION'] = html_template_div_center_div_content_pagination(request=request, utils_module=utils_module, utils_module_model=utils_module_model, page=page)
            data['BOOLEAN_ERROR'] = False
            return http.JsonResponse(data)
        else:
            if form.errors.as_data().get('__all__') is not None:
                messages.add_message(request, messages.ERROR, form.errors['__all__'][0])
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    data['HTML_DIV_MODAL'] = html_template_div_modal(request=request, utils_module=utils_module, utils_module_model=utils_module_model, template_modal_path='disapprove', form=form)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request)
    data['BOOLEAN_ERROR'] = False
    return http.JsonResponse(data)


def list_instance___search(request, utils_module, utils_module_model):
    instances = utils_module_model.MODEL.objects.instances(request=request)
    search = instances
    request_get___search = request.GET.get('search')
    if request_get___search is not None:
        list_string___search = request_get___search.split()
        if list_string___search:
            search = list()
            for instance in instances:
                boolean___add_instance = False
                for string___search in list_string___search:
                    temporal_string___search = string___search.lower()
                    temporal_string___instance = instance.__str__().lower()
                    if temporal_string___instance.find(temporal_string___search) >= 0 or temporal_string___search.find(temporal_string___instance) >= 0:
                        boolean___add_instance = True
                        break
                if boolean___add_instance is False and hasattr(instance, 'identifier'):
                    for string___search in list_string___search:
                        temporal_string___search = string___search.lower()
                        temporal_string___instance_identifier = instance.identifier.lower()
                        if temporal_string___instance_identifier.find(temporal_string___search) >= 0 or temporal_string___search.find(temporal_string___instance_identifier) >= 0:
                            boolean___add_instance = True
                            break
                if boolean___add_instance is False and hasattr(instance, 'email'):
                    for string___search in list_string___search:
                        temporal_string___search = string___search.lower()
                        temporal_string___instance_email = instance.email.lower()
                        if temporal_string___instance_email.find(temporal_string___search) >= 0 or temporal_string___search.find(temporal_string___instance_email) >= 0:
                            boolean___add_instance = True
                            break
                # Este codigo debe estar al final de todas las condiciones
                if hasattr(instance, 'is_active'):
                    list_string___is_active = [_('ADMINISTRATION_MODULE_OPTION_YES').lower(), _('ADMINISTRATION_MODULE_OPTION_NO').lower()]
                    if instance.is_active:
                        string___is_active = list_string___is_active[0]
                    else:
                        string___is_active = list_string___is_active[1]
                    if list_string___search[-1].lower() in list_string___is_active:
                        if boolean___add_instance is True and list_string___search[-1].lower() == string___is_active:
                            boolean___add_instance = True
                        else:
                            if boolean___add_instance is True:
                                boolean___add_instance = False
                            else:
                                if len(list_string___search) == 1 and list_string___search[-1].lower() == string___is_active:
                                    boolean___add_instance = True
                                else:
                                    boolean___add_instance = False
                if boolean___add_instance is True:
                    search.append(instance)
    return search


def int___number_page(request, utils_module, utils_module_model, search, pk):
    int___position = 0
    for instance___search in search:
        int___position += 1
        if instance___search.pk == pk:
            break
    if int___position <= utils_module_model.INSTANCES_AMOUNT_PER_PAGE:
        number_page = 1
    else:
        number_page = int___position // utils_module_model.INSTANCES_AMOUNT_PER_PAGE
        int___rest = int___position % utils_module_model.INSTANCES_AMOUNT_PER_PAGE
        if int___rest > 0:
            number_page += 1
    return number_page


def instance___page(request, utils_module, utils_module_model, search, number_page):
    instance___paginator = paginator.Paginator(object_list=search, per_page=utils_module_model.INSTANCES_AMOUNT_PER_PAGE)
    try:
        if number_page == 0:
            request_get___page = request.GET.get('page')
            page = instance___paginator.page(number=request_get___page)
        else:
            page = instance___paginator.page(number=number_page)
    except paginator.PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = instance___paginator.page(number=1)
    except paginator.EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = instance___paginator.page(number=instance___paginator.num_pages)
    return page
