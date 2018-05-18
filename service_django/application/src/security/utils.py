# -*- coding: utf-8 -*-
from . import forms, ldap, models, tasks
from django import http
from django.conf import settings
from django.contrib import messages
from django.core import urlresolvers
from django.template import loader
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
import copy

# Security from module
SECURITY_FROM_MODULE_HOME = 'home'
SECURITY_FROM_MODULE_ADMINISTRATION = 'administration'
# Sessions SECURITY_USER_MODEL
SECURITY_USER_MODEL_LOCALUSER = 'localuser'
SECURITY_USER_MODEL_LOCALUSER_TEXT = 'LOCAL'
SECURITY_USER_MODEL_LDAPUSER = 'ldapuser'
SECURITY_USER_MODEL_LDAPUSER_TEXT = 'LDAP'
# It is the URL where the user should go, either because of an error or when sawing his session.
SECURITY_USER_URL_REVERSE = 'index'


def html_template(request, context, template):
    return loader.render_to_string(
        template_name=template,
        context=context,
        request=request
    )


def html_template_div_modal_message(request, security_from_module):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/message/message.html' % (security_from_module,),
        context={},
        request=request
    )


def html_template_div_modal_message_message(request, security_from_module):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/_include_/message/message.html' % (security_from_module,),
        context={
            'ctx_messages': messages.get_messages(request=request),
        },
        request=request
    )


def html_template_div_modal_modal_message(request, security_from_module):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/message/message.html' % (security_from_module,),
        context={},
        request=request
    )


def html_template_div_modal_modal_message_message(request, security_from_module):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/_include_/message/message.html' % (security_from_module,),
        context={
            'ctx_messages': messages.get_messages(request=request),
        },
        request=request
    )


def html_template_div_modal_login(request, security_from_module, tab_localuserlogin, tab_ldapuserlogin, form_localuserlogin, form_ldapuserlogin):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/security/login.html' % (security_from_module,),
        context={
            'ctx_tab_localuserlogin': tab_localuserlogin,
            'ctx_tab_ldapuserlogin': tab_ldapuserlogin,
            'ctx_form_localuserlogin': form_localuserlogin,
            'ctx_form_ldapuserlogin': form_ldapuserlogin,
        },
        request=request
    )


def html_template_div_modal_modal_login_forgot_credential_1(request, security_from_module, tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential, form):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/security/login_forgot_credential_1.html' % (security_from_module,),
        context={
            'ctx_tab_localuserlogin_forgot_credential': tab_localuserlogin_forgot_credential,
            'ctx_tab_ldapuserlogin_forgot_credential': tab_ldapuserlogin_forgot_credential,
            'ctx_form': form,
        },
        request=request
    )


def html_template_div_modal_modal_login_forgot_credential_2(request, security_from_module, tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential, form):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/security/login_forgot_credential_2.html' % (security_from_module,),
        context={
            'ctx_tab_localuserlogin_forgot_credential': tab_localuserlogin_forgot_credential,
            'ctx_tab_ldapuserlogin_forgot_credential': tab_ldapuserlogin_forgot_credential,
            'ctx_form': form,
        },
        request=request
    )


def html_template_div_modal_modal_login_forgot_credential_3(request, security_from_module, tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential, form):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/security/login_forgot_credential_3.html' % (security_from_module,),
        context={
            'ctx_tab_localuserlogin_forgot_credential': tab_localuserlogin_forgot_credential,
            'ctx_tab_ldapuserlogin_forgot_credential': tab_ldapuserlogin_forgot_credential,
            'ctx_form': form,
        },
        request=request
    )


def html_template_div_modal_modal_login_request(request, security_from_module, tab_localuserlogin_request, tab_ldapuserlogin_request, form):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/security/login_request.html' % (security_from_module,),
        context={
            'ctx_tab_localuserlogin_request': tab_localuserlogin_request,
            'ctx_tab_ldapuserlogin_request': tab_ldapuserlogin_request,
            'ctx_form': form,
        },
        request=request
    )


def html_template_div_modal_logout(request, security_from_module):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/security/logout.html' % (security_from_module,),
        context={
        },
        request=request
    )


def html_template_div_modal_profile(request, security_from_module, form):
    return loader.render_to_string(
        template_name='%s/_include_/div_modal/security/profile.html' % (security_from_module,),
        context={
            'ctx_form': form,
        },
        request=request
    )


def jsonresponse_error(request, security_from_module):
    if len(messages.get_messages(request=request)) <= 0:
        messages.add_message(request, messages.ERROR, _('SECURITY_MESSAGE ERROR.'))
    data = dict()
    data['BOOLEAN_ERROR'] = True
    data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request, security_from_module=security_from_module)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request, security_from_module=security_from_module)
    data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_message(request=request, security_from_module=security_from_module)
    data['HTML_DIV_MODAL_MODAL_MESSAGE'] = html_template_div_modal_modal_message_message(request=request, security_from_module=security_from_module)
    return http.JsonResponse(data)


def jsonresponse_login(request, security_from_module):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    if (not hasattr(request, 'SECURITY_USER')) or (request.SECURITY_USER is not None):
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    if request.GET.get('tab_localuserlogin'):
        tab_localuserlogin = True
        tab_ldapuserlogin = False
    elif request.GET.get('tab_ldapuserlogin'):
        tab_localuserlogin = False
        tab_ldapuserlogin = True
    else:
        # default
        tab_localuserlogin = False
        tab_ldapuserlogin = True
    # 0: initial
    # 1: login is ok
    # 2: login is not ok
    # 3: login is ok, but user.is_active=False
    data['INT_IS_VALID_FORM'] = 0
    instance = None
    form_localuserlogin = forms.LOCALUserLogin(data=None, request=request)
    form_ldapuserlogin = forms.LDAPUserLogin(data=None, request=request)
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if tab_localuserlogin is True:
            form_localuserlogin = forms.LOCALUserLogin(data=request.POST or None, request=request)
            form = form_localuserlogin
        elif tab_ldapuserlogin is True:
            form_ldapuserlogin = forms.LDAPUserLogin(data=request.POST or None, request=request)
            form = form_ldapuserlogin
        else:
            return jsonresponse_error(request=request, security_from_module=security_from_module)
        if form.is_valid():
            if tab_localuserlogin is True:
                identifier = form.cleaned_data.get('local_identifier')
                password = form.cleaned_data.get('local_password')
                model = models.LOCALUser
                security_user_model = SECURITY_USER_MODEL_LOCALUSER
                instance = model.objects.instance___by_identifier(identifier=identifier)
            elif tab_ldapuserlogin is True:
                identifier = form.cleaned_data.get('ldap_identifier')
                password = form.cleaned_data.get('ldap_password')
                model = models.LDAPUser
                security_user_model = SECURITY_USER_MODEL_LDAPUSER
                instance = model.objects.instance___by_identifier(identifier=identifier)
            else:
                return jsonresponse_error(request=request, security_from_module=security_from_module)
            if instance is not None and instance.boolean___verify_password(password=password):
                if instance.is_active or instance.is_superuser:
                    request.session['SECURITY_USER_MODEL'] = security_user_model
                    request.session['SECURITY_USER_PK'] = instance.pk
                    request.SECURITY_USER = instance
                    boolean___error = True
                    for language in settings.LANGUAGES:
                        if instance.locale != '' and instance.locale in language[0]:
                            translation.activate(instance.locale)
                            request.session[translation.LANGUAGE_SESSION_KEY] = instance.locale
                            boolean___error = False
                            break
                    if boolean___error is True:
                        instance.locale = request.LANGUAGE_CODE
                        instance.save()
                    data['INT_IS_VALID_FORM'] = 1
                else:
                    data['INT_IS_VALID_FORM'] = 3
            else:
                data['INT_IS_VALID_FORM'] = 2
        else:
            data['INT_IS_VALID_FORM'] = 2
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    #
    if data['BOOLEAN_IS_METHOD_POST']:
        if data['INT_IS_VALID_FORM'] == 1:
            messages.add_message(request, messages.SUCCESS, _('SECURITY_LOGIN_MESSAGE Welcome %(instance)s.') % {'instance': instance, })
            data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request, security_from_module=security_from_module)
            data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request, security_from_module=security_from_module)
            return http.JsonResponse(data)
        if data['INT_IS_VALID_FORM'] == 2:
            messages.add_message(request, messages.ERROR, _('SECURITY_LOGIN_MESSAGE The identifier and password are incorrect.'))
        elif data['INT_IS_VALID_FORM'] == 3:
            messages.add_message(request, messages.WARNING, _('SECURITY_LOGIN_MESSAGE The identifier and password are correct, but this user is not active.'))
        data['HTML_DIV_MODAL'] = html_template_div_modal_login(request=request, security_from_module=security_from_module, tab_localuserlogin=tab_localuserlogin, tab_ldapuserlogin=tab_ldapuserlogin, form_localuserlogin=form_localuserlogin, form_ldapuserlogin=form_ldapuserlogin)
        data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request, security_from_module=security_from_module)
    else:
        data['HTML_DIV_MODAL'] = html_template_div_modal_login(request=request, security_from_module=security_from_module, tab_localuserlogin=tab_localuserlogin, tab_ldapuserlogin=tab_ldapuserlogin, form_localuserlogin=form_localuserlogin, form_ldapuserlogin=form_ldapuserlogin)
    return http.JsonResponse(data)


def jsonresponse_login_forgot_credential_1(request, security_from_module):
    tasks.task___security_login_forgot_credential_delete_instances()
    data = dict()
    data['BOOLEAN_ERROR'] = False
    if (not hasattr(request, 'SECURITY_USER')) or (request.SECURITY_USER is not None):
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    if request.GET.get('tab_localuserlogin_forgot_credential'):
        tab_localuserlogin_forgot_credential = True
        tab_ldapuserlogin_forgot_credential = False
        formuserloginforgotcredential1 = forms.LOCALUserLoginForgotCredential1
        formuserloginforgotcredential2 = forms.LOCALUserLoginForgotCredential2
    elif request.GET.get('tab_ldapuserlogin_forgot_credential'):
        tab_localuserlogin_forgot_credential = False
        tab_ldapuserlogin_forgot_credential = True
        formuserloginforgotcredential1 = forms.LDAPUserLoginForgotCredential1
        formuserloginforgotcredential2 = forms.LDAPUserLoginForgotCredential2
    else:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    #
    instance = None
    form = formuserloginforgotcredential1(data=request.POST or None, request=request)
    #
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form.is_valid():
            instance = form.save(commit=True)
            # Send mail with the verification code to the user who forgot their credential.
            tasks.task___security_login_forgot_credential_1_send_mail.apply_async(
                args=[],
                kwargs={
                    'string___email': instance.email,
                    'string___code': instance.code,
                },
                serializer='json'
            )
            messages.add_message(request, messages.SUCCESS, _('SECURITY_LOGIN_FORGOT_CREDENTIAL_MESSAGE An email has been sent to %(email)s with a verification code that will be entered in the field called code confirmation.') % {'email': instance.email, })
            messages.add_message(request, messages.INFO, _('SECURITY_LOGIN_FORGOT_CREDENTIAL_MESSAGE This window should not close and only works %(minutes_max)s minutes after sending the confirmation code to your email address.') % {'minutes_max': instance.INT___MAXIMUM_TIME_OF_EXISTENCE, })
            data['BOOLEAN_IS_VALID_FORM'] = True
        else:
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    #
    if data['BOOLEAN_IS_METHOD_POST'] is True:
        if data['BOOLEAN_IS_VALID_FORM'] is True:
            form = formuserloginforgotcredential2(data=None, request=request, instance=instance)
            data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_forgot_credential_2(request=request, security_from_module=security_from_module, tab_localuserlogin_forgot_credential=tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential=tab_ldapuserlogin_forgot_credential, form=form)
            data['HTML_DIV_MODAL_MODAL_MESSAGE'] = html_template_div_modal_modal_message_message(request=request, security_from_module=security_from_module)
        else:
            data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_forgot_credential_1(request=request, security_from_module=security_from_module, tab_localuserlogin_forgot_credential=tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential=tab_ldapuserlogin_forgot_credential, form=form)
    else:
        data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_forgot_credential_1(request=request, security_from_module=security_from_module, tab_localuserlogin_forgot_credential=tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential=tab_ldapuserlogin_forgot_credential, form=form)
    return http.JsonResponse(data)


def jsonresponse_login_forgot_credential_2(request, security_from_module, pk):
    tasks.task___security_login_forgot_credential_delete_instances()
    data = dict()
    data['BOOLEAN_ERROR'] = False
    if (not hasattr(request, 'SECURITY_USER')) or (request.SECURITY_USER is not None):
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    try:
        pk = int(pk)
    except ValueError:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    if request.GET.get('tab_localuserlogin_forgot_credential'):
        tab_localuserlogin_forgot_credential = True
        tab_ldapuserlogin_forgot_credential = False
        model = models.LOCALUserForgotCredential
        model_mirror = models.LOCALUser
        formuserloginforgotcredential2 = forms.LOCALUserLoginForgotCredential2
        formuserloginforgotcredential3 = forms.LOCALUserLoginForgotCredential3
    elif request.GET.get('tab_ldapuserlogin_forgot_credential'):
        tab_localuserlogin_forgot_credential = False
        tab_ldapuserlogin_forgot_credential = True
        model = models.LDAPUserForgotCredential
        model_mirror = models.LDAPUser
        formuserloginforgotcredential2 = forms.LDAPUserLoginForgotCredential2
        formuserloginforgotcredential3 = forms.LDAPUserLoginForgotCredential3
    else:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    #
    instance = model.objects.instance___by_pk(pk=pk)
    if instance is None:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    instance_mirror = model_mirror.objects.instance___by_email(email=instance.email)
    if instance_mirror is None:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    form = formuserloginforgotcredential2(data=request.POST or None, request=request, instance=instance)
    #
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, _('SECURITY_LOGIN_FORGOT_CREDENTIAL_MESSAGE Now you can change your password to access the application.'))
            minutes = instance.int___time_of_existence()
            minutes_max = instance.INT___MAXIMUM_TIME_OF_EXISTENCE
            if minutes_max < minutes:
                minutes = minutes_max
            messages.add_message(request, messages.INFO, _('SECURITY_LOGIN_FORGOT_CREDENTIAL_MESSAGE This window should not close and only works %(minutes_max)s minutes after sending the confirmation code to your email address that was %(minutes)s minutes ago.') % {'minutes_max': minutes_max, 'minutes': minutes, })
            data['BOOLEAN_IS_VALID_FORM'] = True
        else:
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        messages.add_message(request, messages.SUCCESS, _('SECURITY_LOGIN_FORGOT_CREDENTIAL_MESSAGE An email has been sent to %(email)s with a verification code that will be entered in the field called code confirmation.') % {'email': instance.email, })
        minutes = instance.int___time_of_existence()
        minutes_max = instance.INT___MAXIMUM_TIME_OF_EXISTENCE
        if minutes_max < minutes:
            minutes = minutes_max
        messages.add_message(request, messages.INFO, _('SECURITY_LOGIN_FORGOT_CREDENTIAL_MESSAGE This window should not close and only works %(minutes_max)s minutes after sending the confirmation code to your email address that was %(minutes)s minutes ago.') % {'minutes_max': minutes_max, 'minutes': minutes, })
        data['BOOLEAN_IS_METHOD_POST'] = False
    #
    if data['BOOLEAN_IS_METHOD_POST'] is True:
        if data['BOOLEAN_IS_VALID_FORM'] is True:
            form = formuserloginforgotcredential3(data=None, request=request, instance=instance, instance_mirror=instance_mirror)
            data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_forgot_credential_3(request=request, security_from_module=security_from_module, tab_localuserlogin_forgot_credential=tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential=tab_ldapuserlogin_forgot_credential, form=form)
            data['HTML_DIV_MODAL_MODAL_MESSAGE'] = html_template_div_modal_modal_message_message(request=request, security_from_module=security_from_module)
        else:
            data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_forgot_credential_2(request=request, security_from_module=security_from_module, tab_localuserlogin_forgot_credential=tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential=tab_ldapuserlogin_forgot_credential, form=form)
    else:
        data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_forgot_credential_2(request=request, security_from_module=security_from_module, tab_localuserlogin_forgot_credential=tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential=tab_ldapuserlogin_forgot_credential, form=form)
        data['HTML_DIV_MODAL_MODAL_MESSAGE'] = html_template_div_modal_modal_message_message(request=request, security_from_module=security_from_module)
    return http.JsonResponse(data)


def jsonresponse_login_forgot_credential_3(request, security_from_module, pk):
    tasks.task___security_login_forgot_credential_delete_instances()
    data = dict()
    data['BOOLEAN_ERROR'] = False
    if (not hasattr(request, 'SECURITY_USER')) or (request.SECURITY_USER is not None):
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    try:
        pk = int(pk)
    except ValueError:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    if request.GET.get('tab_localuserlogin_forgot_credential'):
        tab_localuserlogin_forgot_credential = True
        tab_ldapuserlogin_forgot_credential = False
        model = models.LOCALUserForgotCredential
        model_mirror = models.LOCALUser
        formuserloginforgotcredential3 = forms.LOCALUserLoginForgotCredential3
    elif request.GET.get('tab_ldapuserlogin_forgot_credential'):
        tab_localuserlogin_forgot_credential = False
        tab_ldapuserlogin_forgot_credential = True
        model = models.LDAPUserForgotCredential
        model_mirror = models.LDAPUser
        formuserloginforgotcredential3 = forms.LDAPUserLoginForgotCredential3
    else:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    #
    instance = model.objects.instance___by_pk(pk=pk)
    if instance is None:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    instance_mirror = model_mirror.objects.instance___by_email(email=instance.email)
    if instance_mirror is None:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    form = formuserloginforgotcredential3(data=request.POST or None, request=request, instance=instance, instance_mirror=instance_mirror)
    #
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form.is_valid():
            instance = form.save(commit=True)
            instance.delete()
            messages.add_message(request, messages.SUCCESS, _('SECURITY_LOGIN_FORGOT_CREDENTIAL_MESSAGE Try to access the application.'))
            data['BOOLEAN_IS_VALID_FORM'] = True
        else:
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        messages.add_message(request, messages.SUCCESS, _('SECURITY_LOGIN_FORGOT_CREDENTIAL_MESSAGE Now you can change your password to access the application.'))
        minutes = instance.int___time_of_existence()
        minutes_max = instance.INT___MAXIMUM_TIME_OF_EXISTENCE
        if minutes_max < minutes:
            minutes = minutes_max
        messages.add_message(request, messages.INFO, _('SECURITY_LOGIN_FORGOT_CREDENTIAL_MESSAGE This window should not close and only works %(minutes_max)s minutes after sending the confirmation code to your email address that was %(minutes)s minutes ago.') % {'minutes_max': minutes_max, 'minutes': minutes, })
        data['BOOLEAN_IS_METHOD_POST'] = False
    #
    if data['BOOLEAN_IS_METHOD_POST'] is True:
        if data['BOOLEAN_IS_VALID_FORM'] is True:
            data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_message(request=request, security_from_module=security_from_module)
            data['HTML_DIV_MODAL_MODAL_MESSAGE'] = html_template_div_modal_modal_message_message(request=request, security_from_module=security_from_module)
        else:
            data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_forgot_credential_3(request=request, security_from_module=security_from_module, tab_localuserlogin_forgot_credential=tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential=tab_ldapuserlogin_forgot_credential, form=form)
    else:
        data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_forgot_credential_3(request=request, security_from_module=security_from_module, tab_localuserlogin_forgot_credential=tab_localuserlogin_forgot_credential, tab_ldapuserlogin_forgot_credential=tab_ldapuserlogin_forgot_credential, form=form)
        data['HTML_DIV_MODAL_MODAL_MESSAGE'] = html_template_div_modal_modal_message_message(request=request, security_from_module=security_from_module)
    return http.JsonResponse(data)


def jsonresponse_login_request(request, security_from_module):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    if (not hasattr(request, 'SECURITY_USER')) or (request.SECURITY_USER is not None):
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    if request.GET.get('tab_localuserlogin_request'):
        tab_localuserlogin_request = True
        tab_ldapuserlogin_request = False
        form = forms.LOCALUserLoginRequest(data=request.POST or None, request=request)
        string___user_model = SECURITY_USER_MODEL_LOCALUSER_TEXT
        string___identifier = ''
    elif request.GET.get('tab_ldapuserlogin_request'):
        tab_localuserlogin_request = False
        tab_ldapuserlogin_request = True
        form = forms.LDAPUserLoginRequest(data=request.POST or None, request=request)
        string___user_model = SECURITY_USER_MODEL_LDAPUSER_TEXT
        string___identifier = ''
    else:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    #
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form.is_valid():
            instance = form.save(commit=True)
            # Send mail to users who approve the request.
            # Send mail to the user who made the request.
            tasks.task___security_login_request_send_mail.apply_async(
                args=[],
                kwargs={
                    'string___user_model': string___user_model,
                    'string___first_name': instance.first_name,
                    'string___last_name': instance.last_name,
                    'string___identifier': '%s%s' % (string___identifier, instance.identifier,),
                    'string___email': instance.email,
                    'string___detail': instance.detail,
                },
                serializer='json'
            )
            messages.add_message(request, messages.SUCCESS, _('SECURITY_LOGIN_REQUEST_MESSAGE The application administrators have received your request, you will receive an email informing you if it was accepted or canceled.'))
            data['BOOLEAN_IS_VALID_FORM'] = True
        else:
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    #
    if data['BOOLEAN_IS_METHOD_POST'] is True:
        if data['BOOLEAN_IS_VALID_FORM'] is True:
            data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_message(request=request, security_from_module=security_from_module)
            data['HTML_DIV_MODAL_MODAL_MESSAGE'] = html_template_div_modal_modal_message_message(request=request, security_from_module=security_from_module)
        else:
            data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_request(request=request, security_from_module=security_from_module, tab_localuserlogin_request=tab_localuserlogin_request, tab_ldapuserlogin_request=tab_ldapuserlogin_request, form=form)
    else:
        data['HTML_DIV_MODAL_MODAL'] = html_template_div_modal_modal_login_request(request=request, security_from_module=security_from_module, tab_localuserlogin_request=tab_localuserlogin_request, tab_ldapuserlogin_request=tab_ldapuserlogin_request, form=form)
    return http.JsonResponse(data)


def jsonresponse_logout(request, security_from_module):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    if (not hasattr(request, 'SECURITY_USER')) or (request.SECURITY_USER is None):
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    instance = request.SECURITY_USER
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if request.session.get('SECURITY_USER_MODEL'):
            del request.session['SECURITY_USER_MODEL']
        if request.session.get('SECURITY_USER_PK'):
            del request.session['SECURITY_USER_PK']
        request.SECURITY_USER = None
        messages.add_message(request, messages.SUCCESS, _('SECURITY_LOGOUT_MESSAGE %(instance)s your session was successfully closed.') % {'instance': instance, })
        data['BOOLEAN_WITHOUT_PERMISSION'] = True
        data['URL_REDIRECT'] = urlresolvers.reverse(SECURITY_USER_URL_REVERSE)
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    #
    if data['BOOLEAN_IS_METHOD_POST']:
        data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request, security_from_module=security_from_module)
        data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request, security_from_module=security_from_module)
    else:
        data['HTML_DIV_MODAL'] = html_template_div_modal_logout(request=request, security_from_module=security_from_module)
        data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request, security_from_module=security_from_module)
    return http.JsonResponse(data)


def jsonresponse_profile(request, security_from_module):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    if (not hasattr(request, 'SECURITY_USER')) or (request.SECURITY_USER is None):
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    instance = request.SECURITY_USER
    instance_current = copy.deepcopy(instance)
    if isinstance(instance, models.LOCALUser):
        form = forms.LOCALUserProfile(data=request.POST or None, files=request.FILES or None, request=request, instance=instance, instance_current=instance_current)
    elif isinstance(instance, models.LDAPUser):
        ldap.messages___action_is_there_connection(request=request)
        form = forms.LDAPUserProfile(data=request.POST or None, files=request.FILES or None, request=request, instance=instance, instance_current=instance_current)
    else:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    if request.method == 'POST':
        data['BOOLEAN_IS_METHOD_POST'] = True
        if form is not None and form.is_valid():
            instance = form.save(commit=True)
            request.SECURITY_USER = instance
            messages.add_message(request, messages.SUCCESS, _('SECURITY_PROFILE_MESSAGE %(instance)s your profile was successfully update.') % {'instance': instance, })
            data['BOOLEAN_IS_VALID_FORM'] = True
        else:
            data['BOOLEAN_IS_VALID_FORM'] = False
    else:
        data['BOOLEAN_IS_METHOD_POST'] = False
    #
    data['HTML_DIV_MODAL'] = html_template_div_modal_profile(request=request, security_from_module=security_from_module, form=form)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request, security_from_module=security_from_module)
    return http.JsonResponse(data)


def jsonresponse_locale(request, security_from_module):
    data = dict()
    data['BOOLEAN_ERROR'] = False
    if hasattr(request, 'SECURITY_USER') and request.GET.get('locale'):
        boolean___is_valid = False
        for language in settings.LANGUAGES:
            if request.GET.get('locale') in language[0]:
                translation.activate(request.GET.get('locale'))
                request.session[translation.LANGUAGE_SESSION_KEY] = request.GET.get('locale')
                if request.SECURITY_USER is not None:
                    request.SECURITY_USER.locale = request.GET.get('locale')
                    request.SECURITY_USER.save()
                    messages.add_message(request, messages.SUCCESS, _('SECURITY_LOCALE_MESSAGE %(instance)s the language of the application was successfully update.') % {'instance': request.SECURITY_USER, })
                else:
                    messages.add_message(request, messages.SUCCESS, _('SECURITY_LOCALE_MESSAGE The language of the application was successfully update.'))
                boolean___is_valid = True
                break
        if boolean___is_valid is False:
            data['BOOLEAN_ERROR'] = True
    else:
        data['BOOLEAN_ERROR'] = True
    if data['BOOLEAN_ERROR'] is True:
        return jsonresponse_error(request=request, security_from_module=security_from_module)
    #
    data['HTML_DIV_MODAL'] = html_template_div_modal_message(request=request, security_from_module=security_from_module)
    data['HTML_DIV_MODAL_MESSAGE'] = html_template_div_modal_message_message(request=request, security_from_module=security_from_module)
    return http.JsonResponse(data)
