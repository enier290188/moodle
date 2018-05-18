# -*- coding: utf-8 -*-
from src.security import ldap, models, tasks, utils
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

FIELD_CREATED = forms.DateField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_CREATED'),
    required=False,
    widget=forms.DateInput(
        attrs={
            'id': 'created',
            'aria-describedby': 'created_icon',
            'icon': 'fa fa-clock-o',
        },
    ),
)
FIELD_MODIFIED = forms.DateField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_MODIFIED'),
    required=False,
    widget=forms.DateInput(
        attrs={
            'id': 'modified',
            'aria-describedby': 'modified_icon',
            'icon': 'fa fa-clock-o',
        },
    ),
)
FIELD_FIRST_NAME = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_FIRST_NAME'),
    required=False,
    min_length=1,
    max_length=100,
    widget=forms.TextInput(
        attrs={
            'id': 'first_name',
            'class': 'form-control',
            'aria-describedby': 'first_name_icon',
            'icon': 'fa fa-globe',
        },
    ),
)
FIELD_LAST_NAME = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_LAST_NAME'),
    required=False,
    min_length=1,
    max_length=100,
    widget=forms.TextInput(
        attrs={
            'id': 'last_name',
            'class': 'form-control',
            'aria-describedby': 'last_name_icon',
            'icon': 'fa fa-globe',
        },
    ),
)
FIELD_IDENTIFIER = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_IDENTIFIER'),
    required=True,
    min_length=1,
    max_length=100,
    widget=forms.TextInput(
        attrs={
            'id': 'identifier',
            'class': 'form-control',
            'aria-describedby': 'identifier_icon',
            'icon': 'fa fa-user',
        },
    ),
)
FIELD_EMAIL = forms.EmailField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_EMAIL'),
    required=True,
    min_length=1,
    max_length=150,
    widget=forms.EmailInput(
        attrs={
            'id': 'email',
            'class': 'form-control',
            'aria-describedby': 'email_icon',
            'icon': 'fa fa-envelope-o',
        },
    ),
)
FIELD_DETAIL = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_DETAIL'),
    required=True,
    min_length=1,
    max_length=1024,
    widget=forms.Textarea(
        attrs={
            'id': 'detail',
            'class': 'form-control',
            'aria-describedby': 'detail_icon',
            'icon': 'fa fa-globe',
            'rows': 5,
        },
    ),
)


def void___field_attribute_placeholder_locale_reload(field, locale):
    field.widget.attrs['placeholder'] = '- %s -' % (_(locale),)


def void___field_attribute_help_text_locale_reload(field, locale):
    field.help_text = '\"%s\"' % (_(locale),)


class RequestedLDAPUserDetail(forms.ModelForm):
    created = FIELD_CREATED
    modified = FIELD_MODIFIED
    first_name = FIELD_FIRST_NAME
    last_name = FIELD_LAST_NAME
    identifier = FIELD_IDENTIFIER
    email = FIELD_EMAIL
    detail = FIELD_DETAIL

    class Meta:
        model = models.RequestedLDAPUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class RequestedLDAPUserApprove(forms.ModelForm):
    class Meta:
        model = models.RequestedLDAPUser
        fields = ['id', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def approve(self):
        instance_mirror = models.LDAPUser.objects.create(
            first_name=self.instance.first_name,
            last_name=self.instance.last_name,
            identifier=self.instance.identifier,
            email=self.instance.email,
            password=self.instance.password,
            detail=self.instance.detail
        )
        # Send email
        tasks.task___security_login_request_approve_send_mail.apply_async(
            args=[],
            kwargs={
                'string___user_model': utils.SECURITY_USER_MODEL_LDAPUSER_TEXT,
                'string___first_name': instance_mirror.first_name,
                'string___last_name': instance_mirror.last_name,
                'string___identifier': '%s_%s' % (settings.LDAP_SERVER_GROUPS_GROUP_CN.lower(), instance_mirror.identifier,),
                'string___email': instance_mirror.email,
                'string___detail': instance_mirror.detail,
            },
            serializer='json'
        )
        # LDAP
        ldap.void___action_ldapuser_instance_create(instance=instance_mirror)
        return instance_mirror


class RequestedLDAPUserDisapprove(forms.ModelForm):
    class Meta:
        model = models.RequestedLDAPUser
        fields = ['id', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def disapprove(self):
        tasks.task___security_login_request_disapprove_send_mail.apply_async(
            args=[],
            kwargs={
                'string___user_model': utils.SECURITY_USER_MODEL_LDAPUSER_TEXT,
                'string___first_name': self.instance.first_name,
                'string___last_name': self.instance.last_name,
                'string___identifier': '%s_%s' % (settings.LDAP_SERVER_GROUPS_GROUP_CN.lower(), self.instance.identifier,),
                'string___email': self.instance.email,
                'string___detail': self.instance.detail,
            },
            serializer='json'
        )
