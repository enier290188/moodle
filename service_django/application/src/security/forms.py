# -*- coding: utf-8 -*-
from . import ldap, models
from django import forms
from django.conf import settings
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import os
import random
import shutil
import string

FIELD_LOGIN_IDENTIFIER = forms.CharField(
    label=_('SECURITY_LOGIN_IDENTIFIER'),
    required=True,
    min_length=1,
    max_length=100,
    widget=forms.TextInput(
        attrs={
            'id': 'identifier',
            'class': 'form-control',
            'aria-describedby': 'identifier_icon',
            'icon': 'fa fa-user',
            'autofocus': True,
        },
    ),
)
FIELD_LOGIN_PASSWORD = forms.CharField(
    label=_('SECURITY_LOGIN_PASSWORD'),
    required=False,
    max_length=32,
    widget=forms.PasswordInput(
        attrs={
            'id': 'password',
            'class': 'form-control',
            'aria-describedby': 'password_icon',
            'icon': 'fa fa-lock',
        },
        render_value=False,
    ),
)
FIELD_LOGIN_FORGOT_CREDENTIAL_EMAIL = forms.EmailField(
    label=_('SECURITY_LOGIN_FORGOT_CREDENTIAL_EMAIL'),
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
FIELD_LOGIN_FORGOT_CREDENTIAL_CODE_CONFIRMATION = forms.CharField(
    label=_('SECURITY_LOGIN_FORGOT_CREDENTIAL_CODE_CONFIRMATION'),
    required=True,
    min_length=1,
    max_length=100,
    widget=forms.TextInput(
        attrs={
            'id': 'code_confirmation',
            'class': 'form-control',
            'aria-describedby': 'code_confirmation_icon',
            'icon': 'fa fa-globe',
        },
    ),
)
FIELD_LOGIN_FORGOT_CREDENTIAL_PASSWORD = forms.CharField(
    label=_('SECURITY_LOGIN_FORGOT_CREDENTIAL_PASSWORD'),
    required=False,
    max_length=32,
    widget=forms.PasswordInput(
        attrs={
            'id': 'password',
            'class': 'form-control',
            'aria-describedby': 'password_icon',
            'icon': 'fa fa-lock',
        },
        render_value=False,
    ),
)
FIELD_LOGIN_FORGOT_CREDENTIAL_PASSWORD_CONFIRMATION = forms.CharField(
    label=_('SECURITY_LOGIN_FORGOT_CREDENTIAL_PASSWORD_CONFIRMATION'),
    required=False,
    max_length=32,
    widget=forms.PasswordInput(
        attrs={
            'id': 'password_confirmation',
            'class': 'form-control',
            'aria-describedby': 'password_confirmation_icon',
            'icon': 'fa fa-lock',
        },
        render_value=False,
    ),
)
FIELD_LOGIN_REQUEST_FIRST_NAME = forms.CharField(
    label=_('SECURITY_LOGIN_REQUEST_FIRST_NAME'),
    required=True,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w .\-_]+$', message=_('SECURITY_LOGIN_REQUEST_VALIDATION Only letters, numbers and special characters dot, -, _ and space.')),
    ],
    widget=forms.TextInput(
        attrs={
            'id': 'first_name',
            'class': 'form-control',
            'aria-describedby': 'first_name_icon',
            'icon': 'fa fa-globe',
        },
    ),
)
FIELD_LOGIN_REQUEST_LAST_NAME = forms.CharField(
    label=_('SECURITY_LOGIN_REQUEST_LAST_NAME'),
    required=True,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w .\-_]+$', message=_('SECURITY_LOGIN_REQUEST_VALIDATION Only letters, numbers and special characters dot, -, _ and space.')),
    ],
    widget=forms.TextInput(
        attrs={
            'id': 'last_name',
            'class': 'form-control',
            'aria-describedby': 'last_name_icon',
            'icon': 'fa fa-globe',
        },
    ),
)
FIELD_LOGIN_REQUEST_IDENTIFIER = forms.CharField(
    label=_('SECURITY_LOGIN_REQUEST_IDENTIFIER'),
    required=True,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w_]+$', message=_('SECURITY_LOGIN_REQUEST_VALIDATION Only letters, numbers and the special character _.')),
    ],
    widget=forms.TextInput(
        attrs={
            'id': 'identifier',
            'class': 'form-control',
            'aria-describedby': 'identifier_icon',
            'icon': 'fa fa-user',
        },
    ),
)
FIELD_LOGIN_REQUEST_EMAIL = forms.EmailField(
    label=_('SECURITY_LOGIN_REQUEST_EMAIL'),
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
FIELD_LOGIN_REQUEST_PASSWORD = forms.CharField(
    label=_('SECURITY_LOGIN_REQUEST_PASSWORD'),
    required=False,
    max_length=32,
    widget=forms.PasswordInput(
        attrs={
            'id': 'password',
            'class': 'form-control',
            'aria-describedby': 'password_icon',
            'icon': 'fa fa-lock',
        },
        render_value=False,
    ),
)
FIELD_LOGIN_REQUEST_PASSWORD_CONFIRMATION = forms.CharField(
    label=_('SECURITY_LOGIN_REQUEST_PASSWORD_CONFIRMATION'),
    required=False,
    max_length=32,
    widget=forms.PasswordInput(
        attrs={
            'id': 'password_confirmation',
            'class': 'form-control',
            'aria-describedby': 'password_confirmation_icon',
            'icon': 'fa fa-lock',
        },
        render_value=False,
    ),
)
FIELD_LOGIN_REQUEST_DETAIL = forms.CharField(
    label=_('SECURITY_LOGIN_REQUEST_DETAIL'),
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
FIELD_PROFILE_AVATAR = forms.ImageField(
    label=_('SECURITY_PROFILE_AVATAR'),
    required=False,
    widget=forms.FileInput(
        attrs={
            'id': 'avatar',
            'icon': 'fa fa-picture-o',
            'id_button_upload': 'avatar-button-upload',
            'id_image_upload': 'avatar-image-upload',
            'style': 'display: none;',
        },
    ),
)
FIELD_PROFILE_FIRST_NAME = forms.CharField(
    label=_('SECURITY_PROFILE_FIRST_NAME'),
    required=False,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w .\-_]+$', message=_('SECURITY_PROFILE_VALIDATION Only letters, numbers and special characters dot, -, _ and space.')),
    ],
    widget=forms.TextInput(
        attrs={
            'id': 'first_name',
            'class': 'form-control',
            'aria-describedby': 'first_name_icon',
            'icon': 'fa fa-globe',
        },
    ),
)
FIELD_PROFILE_LAST_NAME = forms.CharField(
    label=_('SECURITY_PROFILE_LAST_NAME'),
    required=False,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w .\-_]+$', message=_('SECURITY_PROFILE_VALIDATION Only letters, numbers and special characters dot, -, _ and space.')),
    ],
    widget=forms.TextInput(
        attrs={
            'id': 'last_name',
            'class': 'form-control',
            'aria-describedby': 'last_name_icon',
            'icon': 'fa fa-globe',
        },
    ),
)
FIELD_PROFILE_IDENTIFIER = forms.CharField(
    label=_('SECURITY_PROFILE_IDENTIFIER'),
    required=True,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w_]+$', message=_('SECURITY_PROFILE_VALIDATION Only letters, numbers and the special character _.')),
    ],
    widget=forms.TextInput(
        attrs={
            'id': 'identifier',
            'class': 'form-control',
            'aria-describedby': 'identifier_icon',
            'icon': 'fa fa-user',
        },
    ),
)
FIELD_PROFILE_EMAIL = forms.EmailField(
    label=_('SECURITY_PROFILE_EMAIL'),
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
FIELD_PROFILE_PASSWORD = forms.CharField(
    label=_('SECURITY_PROFILE_PASSWORD'),
    required=False,
    max_length=32,
    widget=forms.PasswordInput(
        attrs={
            'id': 'password',
            'class': 'form-control',
            'aria-describedby': 'password_icon',
            'icon': 'fa fa-lock',
        },
        render_value=False,
    ),
)
FIELD_PROFILE_PASSWORD_CONFIRMATION = forms.CharField(
    label=_('SECURITY_PROFILE_PASSWORD_CONFIRMATION'),
    required=False,
    max_length=32,
    widget=forms.PasswordInput(
        attrs={
            'id': 'password_confirmation',
            'class': 'form-control',
            'aria-describedby': 'password_confirmation_icon',
            'icon': 'fa fa-lock',
        },
        render_value=False,
    ),
)


def void___field_attribute_placeholder_locale_reload(field, locale):
    field.widget.attrs['placeholder'] = '- %s -' % (_(locale),)


def void___field_attribute_help_text_locale_reload(field, locale):
    field.help_text = '\"%s\"' % (_(locale),)


class LOCALUserLogin(forms.Form):
    local_identifier = FIELD_LOGIN_IDENTIFIER
    local_password = FIELD_LOGIN_PASSWORD

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # identifier
        void___field_attribute_placeholder_locale_reload(field=self.fields['local_identifier'], locale='SECURITY_LOGIN_IDENTIFIER')
        self.fields['local_identifier'].widget.attrs['id'] = 'local_identifier'
        self.fields['local_identifier'].widget.attrs['aria-describedby'] = 'local_identifier_icon'
        self.fields['local_identifier'].widget.attrs['autofocus'] = True
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['local_password'], locale='SECURITY_LOGIN_PASSWORD')
        self.fields['local_password'].widget.attrs['id'] = 'local_password'
        self.fields['local_password'].widget.attrs['aria-describedby'] = 'local_password_icon'


class LOCALUserLoginForgotCredential1(forms.ModelForm):
    email = FIELD_LOGIN_FORGOT_CREDENTIAL_EMAIL

    class Meta:
        model = models.LOCALUserForgotCredential
        fields = ['email', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_EMAIL')
        void___field_attribute_help_text_locale_reload(field=self.fields['email'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_EMAIL_HELP_TEXT')
        self.fields['email'].widget.attrs['autofocus'] = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.LOCALUser.objects.get(email=email)
        except models.LOCALUser.DoesNotExist:
            raise forms.ValidationError(_('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION This email address is not subscribed to any account.'))
        try:
            instance = models.LOCALUserForgotCredential.objects.get(email=email)
        except models.LOCALUserForgotCredential.DoesNotExist:
            return email
        minutes = instance.int___time_of_existence()
        minutes_max = instance.INT___MAXIMUM_TIME_OF_EXISTENCE
        if minutes_max <= minutes + 1:
            raise forms.ValidationError(_('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION In a few seconds you can try to recover your account.'))
        else:
            raise forms.ValidationError(_('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION It is been %(minutes)s minutes since you tried to recover your account, you should wait about %(minutes_max)s minutes.') % {'minutes': minutes, 'minutes_max': minutes_max, })

    def save(self, commit=True):
        instance = super(LOCALUserLoginForgotCredential1, self).save(commit=False)
        #
        if commit:
            # code
            string___timezone = timezone.now().strftime('%Y%m%d%H%M%S')
            string___letters_digits = string.ascii_letters + string.digits
            string___code = string___timezone + ''.join([random.choice(string___letters_digits) for x in range(86)])  # 100 characteres = 14 + 86
            instance.code = string___code
            # save to data base
            instance.save()
        return instance


class LOCALUserLoginForgotCredential2(forms.ModelForm):
    email = FIELD_LOGIN_FORGOT_CREDENTIAL_EMAIL
    code_confirmation = FIELD_LOGIN_FORGOT_CREDENTIAL_CODE_CONFIRMATION

    class Meta:
        model = models.LOCALUserForgotCredential
        fields = ['email', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_EMAIL')
        self.fields['email'].widget.attrs['readonly'] = True
        # code_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['code_confirmation'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_CODE_CONFIRMATION')
        void___field_attribute_help_text_locale_reload(field=self.fields['code_confirmation'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_CODE_CONFIRMATION_HELP_TEXT')
        self.fields['code_confirmation'].widget.attrs['autofocus'] = True

    def clean_email(self):
        return self.instance.email

    def clean_code_confirmation(self):
        code_confirmation = self.cleaned_data.get('code_confirmation')
        try:
            models.LOCALUserForgotCredential.objects.get(email=self.instance.email, code=code_confirmation)
        except models.LOCALUserForgotCredential.DoesNotExist:
            raise forms.ValidationError(_('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION This code is not correct.'))
        return code_confirmation

    def save(self, commit=True):
        instance = super(LOCALUserLoginForgotCredential2, self).save(commit=False)
        #
        if commit:
            # save to data base
            instance.save()
        return instance


class LOCALUserLoginForgotCredential3(forms.ModelForm):
    password = FIELD_LOGIN_FORGOT_CREDENTIAL_PASSWORD
    password_confirmation = FIELD_LOGIN_FORGOT_CREDENTIAL_PASSWORD_CONFIRMATION

    class Meta:
        model = models.LOCALUserForgotCredential
        fields = ['password', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.instance_mirror = kwargs.pop('instance_mirror')
        super().__init__(*args, **kwargs)
        #
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['password'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_PASSWORD')
        self.fields['password'].widget.attrs['autofocus'] = True
        # password_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['password_confirmation'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_PASSWORD_CONFIRMATION')

    def clean(self):
        ___clean___ = super(LOCALUserLoginForgotCredential3, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password', _('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION The password and your confirmation do not match.'))
            self.add_error('password_confirmation', _('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION The password and your confirmation do not match.'))
        return ___clean___

    def save(self, commit=True):
        instance = super(LOCALUserLoginForgotCredential3, self).save(commit=False)
        #
        if commit:
            # password
            password = self.cleaned_data.get('password')
            instance.void___encrypt_password(password=password)
            self.instance_mirror.void___encrypt_password(password=password)
            # save to data base
            instance.save()
            self.instance_mirror.save()
        return instance


class LOCALUserLoginRequest(forms.ModelForm):
    first_name = FIELD_LOGIN_REQUEST_FIRST_NAME
    last_name = FIELD_LOGIN_REQUEST_LAST_NAME
    identifier = FIELD_LOGIN_REQUEST_IDENTIFIER
    email = FIELD_LOGIN_REQUEST_EMAIL
    password = FIELD_LOGIN_REQUEST_PASSWORD
    password_confirmation = FIELD_LOGIN_REQUEST_PASSWORD_CONFIRMATION
    detail = FIELD_LOGIN_REQUEST_DETAIL

    class Meta:
        model = models.RequestedLOCALUser
        fields = ['first_name', 'last_name', 'identifier', 'email', 'password', 'detail', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # first_name
        void___field_attribute_placeholder_locale_reload(field=self.fields['first_name'], locale='SECURITY_LOGIN_REQUEST_FIRST_NAME')
        self.fields['first_name'].widget.attrs['autofocus'] = True
        # last name
        void___field_attribute_placeholder_locale_reload(field=self.fields['last_name'], locale='SECURITY_LOGIN_REQUEST_LAST_NAME')
        # identifier
        void___field_attribute_placeholder_locale_reload(field=self.fields['identifier'], locale='SECURITY_LOGIN_REQUEST_IDENTIFIER')
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='SECURITY_LOGIN_REQUEST_EMAIL')
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['password'], locale='SECURITY_LOGIN_REQUEST_PASSWORD')
        # password_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['password_confirmation'], locale='SECURITY_LOGIN_REQUEST_PASSWORD_CONFIRMATION')
        # detail
        void___field_attribute_placeholder_locale_reload(field=self.fields['detail'], locale='SECURITY_LOGIN_REQUEST_DETAIL')
        void___field_attribute_help_text_locale_reload(field=self.fields['detail'], locale='SECURITY_LOGIN_REQUEST_DETAIL_HELP_TEXT')

    def clean_identifier(self):
        identifier = self.cleaned_data.get('identifier')
        try:
            models.LOCALUser.objects.get(identifier=identifier)
        except models.LOCALUser.DoesNotExist:
            try:
                models.RequestedLOCALUser.objects.get(identifier=identifier)
            except models.RequestedLOCALUser.DoesNotExist:
                return identifier
        raise forms.ValidationError(_('SECURITY_LOGIN_REQUEST_VALIDATION This identifier has already been chosen.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.LOCALUser.objects.get(email=email)
        except models.LOCALUser.DoesNotExist:
            try:
                models.RequestedLOCALUser.objects.get(email=email)
            except models.RequestedLOCALUser.DoesNotExist:
                return email
        raise forms.ValidationError(_('SECURITY_LOGIN_REQUEST_VALIDATION This email has already been chosen.'))

    def clean(self):
        ___clean___ = super(LOCALUserLoginRequest, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password', _('SECURITY_LOGIN_REQUEST_VALIDATION The password and your confirmation do not match.'))
            self.add_error('password_confirmation', _('SECURITY_LOGIN_REQUEST_VALIDATION The password and your confirmation do not match.'))
        return ___clean___

    def save(self, commit=True):
        instance = super(LOCALUserLoginRequest, self).save(commit=False)
        #
        if commit:
            # password
            password = self.cleaned_data.get('password')
            if password is not '':
                instance.void___encrypt_password(password=password)
            # save to data base
            instance.save()
        return instance


class LOCALUserProfile(forms.ModelForm):
    avatar = FIELD_PROFILE_AVATAR
    first_name = FIELD_PROFILE_FIRST_NAME
    last_name = FIELD_PROFILE_LAST_NAME
    identifier = FIELD_PROFILE_IDENTIFIER
    email = FIELD_PROFILE_EMAIL
    password = FIELD_PROFILE_PASSWORD
    password_confirmation = FIELD_PROFILE_PASSWORD_CONFIRMATION

    class Meta:
        model = models.LOCALUser
        fields = ['avatar', 'first_name', 'last_name', 'identifier', 'email', 'password', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.instance_current = kwargs.pop('instance_current')
        super().__init__(*args, **kwargs)
        #
        # first_name
        void___field_attribute_placeholder_locale_reload(field=self.fields['first_name'], locale='SECURITY_PROFILE_FIRST_NAME')
        self.fields['first_name'].widget.attrs['autofocus'] = True
        # last name
        void___field_attribute_placeholder_locale_reload(field=self.fields['last_name'], locale='SECURITY_PROFILE_LAST_NAME')
        # identifier
        void___field_attribute_placeholder_locale_reload(field=self.fields['identifier'], locale='SECURITY_PROFILE_IDENTIFIER')
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='SECURITY_PROFILE_EMAIL')
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['password'], locale='SECURITY_PROFILE_PASSWORD')
        # password_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['password_confirmation'], locale='SECURITY_PROFILE_PASSWORD_CONFIRMATION')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if self.files.get('avatar'):
            if len(self.files.get('avatar')) > 1 * 1024 * 1024:  # 1MB
                raise forms.ValidationError(_('SECURITY_PROFILE_VALIDATION The avatar should not be beggear than %(weight)s.') % {'weight': '1mb', })
        return avatar

    def clean_identifier(self):
        identifier = self.cleaned_data.get('identifier')
        try:
            instance = models.LOCALUser.objects.get(identifier=identifier)
        except models.LOCALUser.DoesNotExist:
            return identifier
        if instance.identifier == self.instance_current.identifier:
            return identifier
        raise forms.ValidationError(_('SECURITY_PROFILE_VALIDATION This identifier has already been chosen.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            instance = models.LOCALUser.objects.get(email=email)
        except models.LOCALUser.DoesNotExist:
            return email
        if instance.email == self.instance_current.email:
            return email
        raise forms.ValidationError(_('SECURITY_PROFILE_VALIDATION This email has already been chosen.'))

    def clean(self):
        ___clean___ = super(LOCALUserProfile, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password', _('SECURITY_PROFILE_VALIDATION The password and your confirmation do not match.'))
            self.add_error('password_confirmation', _('SECURITY_PROFILE_VALIDATION The password and your confirmation do not match.'))
        return ___clean___

    def save(self, commit=True):
        instance = super(LOCALUserProfile, self).save(commit=False)
        #
        if commit:
            # avatar
            if self.instance_current.avatar is not None and self.instance_current.avatar != '' and instance.avatar is not None and instance.avatar != '':
                if self.instance_current.avatar != instance.avatar:
                    if os.path.exists(self.instance_current.avatar.path):
                        os.remove(self.instance_current.avatar.path)
                if self.instance_current.identifier != instance.identifier:
                    if self.instance_current.avatar != instance.avatar:
                        if os.path.exists(self.instance_current.string___folder_path()):
                            shutil.rmtree(self.instance_current.string___folder_path())
                    else:
                        instance.avatar = '%s/%s/%s.jpg' % (models.FOLDER_LOCALUSER_PATH, instance.identifier, instance.identifier,)
                        if os.path.exists(self.instance_current.avatar.path) and os.path.exists(self.instance_current.string___folder_path()):
                            os.rename(self.instance_current.avatar.path, '%s/%s.jpg' % (self.instance_current.string___folder_path(), instance.identifier,))
                            os.rename(self.instance_current.string___folder_path(), self.instance.string___folder_path())
            # password
            password = self.cleaned_data.get('password')
            if password is not '':
                instance.void___encrypt_password(password=password)
            else:
                instance.password = self.instance_current.password
            # save to data base
            instance.save()
        return instance


class LDAPUserLogin(forms.Form):
    ldap_identifier = FIELD_LOGIN_IDENTIFIER
    ldap_password = FIELD_LOGIN_PASSWORD

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # identifier
        void___field_attribute_placeholder_locale_reload(field=self.fields['ldap_identifier'], locale='SECURITY_LOGIN_IDENTIFIER')
        self.fields['ldap_identifier'].widget.attrs['id'] = 'ldap_identifier'
        self.fields['ldap_identifier'].widget.attrs['aria-describedby'] = 'ldap_identifier_icon'
        self.fields['ldap_identifier'].widget.attrs['autofocus'] = True
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['ldap_password'], locale='SECURITY_LOGIN_PASSWORD')
        self.fields['ldap_password'].widget.attrs['id'] = 'ldap_password'
        self.fields['ldap_password'].widget.attrs['aria-describedby'] = 'ldap_password_icon'


class LDAPUserLoginForgotCredential1(forms.ModelForm):
    email = FIELD_LOGIN_FORGOT_CREDENTIAL_EMAIL

    class Meta:
        model = models.LDAPUserForgotCredential
        fields = ['email', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_EMAIL')
        void___field_attribute_help_text_locale_reload(field=self.fields['email'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_EMAIL_HELP_TEXT')
        self.fields['email'].widget.attrs['autofocus'] = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.LDAPUser.objects.get(email=email)
        except models.LDAPUser.DoesNotExist:
            raise forms.ValidationError(_('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION This email address is not subscribed to any account.'))
        try:
            instance = models.LDAPUserForgotCredential.objects.get(email=email)
        except models.LDAPUserForgotCredential.DoesNotExist:
            return email
        minutes = instance.int___time_of_existence()
        minutes_max = instance.INT___MAXIMUM_TIME_OF_EXISTENCE
        if minutes_max <= minutes + 1:
            raise forms.ValidationError(_('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION In a few seconds you can try to recover your account.'))
        else:
            raise forms.ValidationError(_('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION It is been %(minutes)s minutes since you tried to recover your account, you should wait about %(minutes_max)s minutes.') % {'minutes': minutes, 'minutes_max': minutes_max, })

    def save(self, commit=True):
        instance = super(LDAPUserLoginForgotCredential1, self).save(commit=False)
        #
        if commit:
            # code
            string___timezone = timezone.now().strftime('%Y%m%d%H%M%S')
            string___letters_digits = string.ascii_letters + string.digits
            string___code = string___timezone + ''.join([random.choice(string___letters_digits) for x in range(86)])  # 100 characteres = 14 + 86
            instance.code = string___code
            # save to data base
            instance.save()
        return instance


class LDAPUserLoginForgotCredential2(forms.ModelForm):
    email = FIELD_LOGIN_FORGOT_CREDENTIAL_EMAIL
    code_confirmation = FIELD_LOGIN_FORGOT_CREDENTIAL_CODE_CONFIRMATION

    class Meta:
        model = models.LDAPUserForgotCredential
        fields = ['email', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_EMAIL')
        self.fields['email'].widget.attrs['readonly'] = True
        # code_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['code_confirmation'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_CODE_CONFIRMATION')
        void___field_attribute_help_text_locale_reload(field=self.fields['code_confirmation'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_CODE_CONFIRMATION_HELP_TEXT')
        self.fields['code_confirmation'].widget.attrs['autofocus'] = True

    def clean_email(self):
        return self.instance.email

    def clean_code_confirmation(self):
        code_confirmation = self.cleaned_data.get('code_confirmation')
        try:
            models.LDAPUserForgotCredential.objects.get(email=self.instance.email, code=code_confirmation)
        except models.LDAPUserForgotCredential.DoesNotExist:
            raise forms.ValidationError(_('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION This code is not correct.'))
        return code_confirmation

    def save(self, commit=True):
        instance = super(LDAPUserLoginForgotCredential2, self).save(commit=False)
        #
        if commit:
            # save to data base
            instance.save()
        return instance


class LDAPUserLoginForgotCredential3(forms.ModelForm):
    password = FIELD_LOGIN_FORGOT_CREDENTIAL_PASSWORD
    password_confirmation = FIELD_LOGIN_FORGOT_CREDENTIAL_PASSWORD_CONFIRMATION

    class Meta:
        model = models.LDAPUserForgotCredential
        fields = ['password', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.instance_mirror = kwargs.pop('instance_mirror')
        super().__init__(*args, **kwargs)
        #
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['password'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_PASSWORD')
        self.fields['password'].widget.attrs['autofocus'] = True
        # password_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['password_confirmation'], locale='SECURITY_LOGIN_FORGOT_CREDENTIAL_PASSWORD_CONFIRMATION')

    def clean(self):
        ___clean___ = super(LDAPUserLoginForgotCredential3, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password', _('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION The password and your confirmation do not match.'))
            self.add_error('password_confirmation', _('SECURITY_LOGIN_FORGOT_CREDENTIAL_VALIDATION The password and your confirmation do not match.'))
        return ___clean___

    def save(self, commit=True):
        instance = super(LDAPUserLoginForgotCredential3, self).save(commit=False)
        #
        if commit:
            # password
            password = self.cleaned_data.get('password')
            instance.void___encrypt_password(password=password)
            self.instance_mirror.void___encrypt_password(password=password)
            # save to data base
            instance.save()
            self.instance_mirror.save()
            #
            # LDAP
            ldap.void___action_ldapuser_instance_update(instance=self.instance_mirror)
        return instance


class LDAPUserLoginRequest(forms.ModelForm):
    first_name = FIELD_LOGIN_REQUEST_FIRST_NAME
    last_name = FIELD_LOGIN_REQUEST_LAST_NAME
    identifier = FIELD_LOGIN_REQUEST_IDENTIFIER
    email = FIELD_LOGIN_REQUEST_EMAIL
    password = FIELD_LOGIN_REQUEST_PASSWORD
    password_confirmation = FIELD_LOGIN_REQUEST_PASSWORD_CONFIRMATION
    detail = FIELD_LOGIN_REQUEST_DETAIL

    class Meta:
        model = models.RequestedLDAPUser
        fields = ['first_name', 'last_name', 'identifier', 'email', 'password', 'detail', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # first_name
        void___field_attribute_placeholder_locale_reload(field=self.fields['first_name'], locale='SECURITY_LOGIN_REQUEST_FIRST_NAME')
        self.fields['first_name'].widget.attrs['autofocus'] = True
        # last name
        void___field_attribute_placeholder_locale_reload(field=self.fields['last_name'], locale='SECURITY_LOGIN_REQUEST_LAST_NAME')
        # identifier
        void___field_attribute_placeholder_locale_reload(field=self.fields['identifier'], locale='SECURITY_LOGIN_REQUEST_IDENTIFIER')
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='SECURITY_LOGIN_REQUEST_EMAIL')
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['password'], locale='SECURITY_LOGIN_REQUEST_PASSWORD')
        # password_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['password_confirmation'], locale='SECURITY_LOGIN_REQUEST_PASSWORD_CONFIRMATION')
        # detail
        void___field_attribute_placeholder_locale_reload(field=self.fields['detail'], locale='SECURITY_LOGIN_REQUEST_DETAIL')
        void___field_attribute_help_text_locale_reload(field=self.fields['detail'], locale='SECURITY_LOGIN_REQUEST_DETAIL_HELP_TEXT')

    def clean_identifier(self):
        identifier = self.cleaned_data.get('identifier')
        try:
            models.LDAPUser.objects.get(identifier=identifier)
        except models.LDAPUser.DoesNotExist:
            try:
                models.RequestedLDAPUser.objects.get(identifier=identifier)
            except models.RequestedLDAPUser.DoesNotExist:
                return identifier
        raise forms.ValidationError(_('SECURITY_LOGIN_REQUEST_VALIDATION This identifier has already been chosen.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.LDAPUser.objects.get(email=email)
        except models.LDAPUser.DoesNotExist:
            try:
                models.RequestedLDAPUser.objects.get(email=email)
            except models.RequestedLDAPUser.DoesNotExist:
                return email
        raise forms.ValidationError(_('SECURITY_LOGIN_REQUEST_VALIDATION This email has already been chosen.'))

    def clean(self):
        ___clean___ = super(LDAPUserLoginRequest, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password', _('SECURITY_LOGIN_REQUEST_VALIDATION The password and your confirmation do not match.'))
            self.add_error('password_confirmation', _('SECURITY_LOGIN_REQUEST_VALIDATION The password and your confirmation do not match.'))
        return ___clean___

    def save(self, commit=True):
        instance = super(LDAPUserLoginRequest, self).save(commit=False)
        #
        if commit:
            # password
            password = self.cleaned_data.get('password')
            if password is not '':
                instance.void___encrypt_password(password=password)
            # save to data base
            instance.save()
        return instance


class LDAPUserProfile(forms.ModelForm):
    avatar = FIELD_PROFILE_AVATAR
    first_name = FIELD_PROFILE_FIRST_NAME
    last_name = FIELD_PROFILE_LAST_NAME
    identifier = FIELD_PROFILE_IDENTIFIER
    email = FIELD_PROFILE_EMAIL
    password = FIELD_PROFILE_PASSWORD
    password_confirmation = FIELD_PROFILE_PASSWORD_CONFIRMATION

    class Meta:
        model = models.LDAPUser
        fields = ['avatar', 'first_name', 'last_name', 'identifier', 'email', 'password', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.instance_current = kwargs.pop('instance_current')
        super().__init__(*args, **kwargs)
        #
        # first_name
        void___field_attribute_placeholder_locale_reload(field=self.fields['first_name'], locale='SECURITY_PROFILE_FIRST_NAME')
        self.fields['first_name'].widget.attrs['autofocus'] = True
        # last name
        void___field_attribute_placeholder_locale_reload(field=self.fields['last_name'], locale='SECURITY_PROFILE_LAST_NAME')
        # identifier
        void___field_attribute_placeholder_locale_reload(field=self.fields['identifier'], locale='SECURITY_PROFILE_IDENTIFIER')
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='SECURITY_PROFILE_EMAIL')
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['password'], locale='SECURITY_PROFILE_PASSWORD')
        # password_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['password_confirmation'], locale='SECURITY_PROFILE_PASSWORD_CONFIRMATION')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if self.files.get('avatar'):
            if len(self.files.get('avatar')) > 1 * 1024 * 1024:  # 1MB
                raise forms.ValidationError(_('SECURITY_PROFILE_VALIDATION The avatar should not be beggear than %(weight)s.') % {'weight': '1mb', })
        return avatar

    def clean_identifier(self):
        identifier = self.cleaned_data.get('identifier')
        try:
            instance = models.LDAPUser.objects.get(identifier=identifier)
        except models.LDAPUser.DoesNotExist:
            return identifier
        if instance.identifier == self.instance_current.identifier:
            return identifier
        raise forms.ValidationError(_('SECURITY_PROFILE_VALIDATION This identifier has already been chosen.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            instance = models.LDAPUser.objects.get(email=email)
        except models.LDAPUser.DoesNotExist:
            return email
        if instance.email == self.instance_current.email:
            return email
        raise forms.ValidationError(_('SECURITY_PROFILE_VALIDATION This email has already been chosen.'))

    def clean(self):
        ___clean___ = super(LDAPUserProfile, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password', _('SECURITY_PROFILE_VALIDATION The password and your confirmation do not match.'))
            self.add_error('password_confirmation', _('SECURITY_PROFILE_VALIDATION The password and your confirmation do not match.'))
        return ___clean___

    def save(self, commit=True):
        instance = super(LDAPUserProfile, self).save(commit=False)
        #
        if commit:
            # avatar
            if self.instance_current.avatar is not None and self.instance_current.avatar != '' and instance.avatar is not None and instance.avatar != '':
                if self.instance_current.avatar != instance.avatar:
                    if os.path.exists(self.instance_current.avatar.path):
                        os.remove(self.instance_current.avatar.path)
                if self.instance_current.identifier != instance.identifier:
                    if self.instance_current.avatar != instance.avatar:
                        if os.path.exists(self.instance_current.string___folder_path()):
                            shutil.rmtree(self.instance_current.string___folder_path())
                    else:
                        instance.avatar = '%s/%s/%s.jpg' % (models.FOLDER_LDAPUSER_PATH, instance.identifier, instance.identifier,)
                        if os.path.exists(self.instance_current.avatar.path) and os.path.exists(self.instance_current.string___folder_path()):
                            os.rename(self.instance_current.avatar.path, '%s/%s.jpg' % (self.instance_current.string___folder_path(), instance.identifier,))
                            os.rename(self.instance_current.string___folder_path(), self.instance.string___folder_path())
            # password
            password = self.cleaned_data.get('password')
            if password is not '':
                instance.void___encrypt_password(password=password)
            else:
                instance.password = self.instance_current.password
            # save to data base
            instance.save()
            #
            # LDAP
            ldap.void___action_ldapuser_instance_update(instance=instance)
        return instance
