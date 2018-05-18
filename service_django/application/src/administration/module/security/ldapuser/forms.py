# -*- coding: utf-8 -*-
from src.security import ldap, models
from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _
import os
import shutil

FIELD_IS_ACTIVE = forms.BooleanField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_IS_ACTIVE'),
    required=False,
    widget=forms.CheckboxInput(
        attrs={
            'id': 'is_active',
            'aria-describedby': 'is_active_icon',
            'icon': 'fa fa-check-square-o',
        },
    ),
)
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
FIELD_AVATAR = forms.ImageField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_AVATAR'),
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
FIELD_FIRST_NAME = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_FIRST_NAME'),
    required=False,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w .\-_]+$', message=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION Only letters, numbers and special characters dot, -, _ and space.')),
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
FIELD_LAST_NAME = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_LAST_NAME'),
    required=False,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w .\-_]+$', message=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION Only letters, numbers and special characters dot, -, _ and space.')),
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
FIELD_IDENTIFIER = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_IDENTIFIER'),
    required=True,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w_]+$', message=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION Only letters, numbers and the special character _.')),
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
FIELD_PASSWORD = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_PASSWORD'),
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
FIELD_PASSWORD_CONFIRMATION = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_PASSWORD_CONFIRMATION'),
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
FIELD_GROUPS = forms.ModelMultipleChoiceField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_GROUPS'),
    required=False,
    widget=forms.CheckboxSelectMultiple(
        attrs={
            'id': 'groups',
            'class': 'form-control',
            'aria-describedby': 'groups_icon',
            'icon': 'fa fa-object-group',
        },
    ),
    queryset=models.Group.objects.all(),
)
FIELD_PERMISSIONS = forms.ModelMultipleChoiceField(
    label=_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_PERMISSIONS'),
    required=False,
    widget=forms.CheckboxSelectMultiple(
        attrs={
            'id': 'permissions',
            'class': 'form-control',
            'aria-describedby': 'permissions_icon',
            'icon': 'fa fa-unlock',
        },
    ),
    queryset=models.Permission.objects.all(),
)


def void___field_attribute_placeholder_locale_reload(field, locale):
    field.widget.attrs['placeholder'] = '- %s -' % (_(locale),)


def void___field_attribute_help_text_locale_reload(field, locale):
    field.help_text = '\"%s\"' % (_(locale),)


class LDAPUserCreate(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    first_name = FIELD_FIRST_NAME
    last_name = FIELD_LAST_NAME
    identifier = FIELD_IDENTIFIER
    email = FIELD_EMAIL
    password = FIELD_PASSWORD
    password_confirmation = FIELD_PASSWORD_CONFIRMATION
    detail = FIELD_DETAIL
    groups = FIELD_GROUPS
    permissions = FIELD_PERMISSIONS

    class Meta:
        model = models.LDAPUser
        fields = ['is_active', 'first_name', 'last_name', 'identifier', 'email', 'password', 'detail', 'groups', 'permissions', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # is_active
        void___field_attribute_help_text_locale_reload(field=self.fields['is_active'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_IS_ACTIVE_HELP_TEXT')
        self.fields['is_active'].initial = True
        # first_name
        void___field_attribute_placeholder_locale_reload(field=self.fields['first_name'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_FIRST_NAME')
        self.fields['first_name'].widget.attrs['autofocus'] = True
        # last name
        void___field_attribute_placeholder_locale_reload(field=self.fields['last_name'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_LAST_NAME')
        # identifier
        void___field_attribute_placeholder_locale_reload(field=self.fields['identifier'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_IDENTIFIER')
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_EMAIL')
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['password'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_PASSWORD')
        # password_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['password_confirmation'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_PASSWORD_CONFIRMATION')
        # detail
        void___field_attribute_placeholder_locale_reload(field=self.fields['detail'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_DETAIL')
        void___field_attribute_help_text_locale_reload(field=self.fields['detail'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_DETAIL_HELP_TEXT')
        # groups
        self.groups_choices = models.Group.objects.all()
        # permissions
        self.permissions_choices = models.Permission.objects.all()

    def clean_identifier(self):
        identifier = self.cleaned_data.get('identifier')
        try:
            models.LDAPUser.objects.get(identifier=identifier)
        except models.LDAPUser.DoesNotExist:
            try:
                models.RequestedLDAPUser.objects.get(identifier=identifier)
            except models.RequestedLDAPUser.DoesNotExist:
                return identifier
        raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION This identifier has already been chosen.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.LDAPUser.objects.get(email=email)
        except models.LDAPUser.DoesNotExist:
            try:
                models.RequestedLDAPUser.objects.get(email=email)
            except models.RequestedLDAPUser.DoesNotExist:
                return email
        raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION This email has already been chosen.'))

    def clean(self):
        ___clean___ = super(LDAPUserCreate, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password', _('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION The password and your confirmation do not match.'))
            self.add_error('password_confirmation', _('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION The password and your confirmation do not match.'))
        return ___clean___

    def save(self, commit=True):
        instance = super(LDAPUserCreate, self).save(commit=False)
        #
        if commit:
            # password
            password = self.cleaned_data.get('password')
            instance.void___encrypt_password(password=password)
            # save to data base
            instance.save()
            #
            # groups
            # groups seleccionados en el formulario
            groups_selected = self.cleaned_data.get('groups')
            # to add groups
            for group_selected in groups_selected:
                instance___ldapusergroup = models.LDAPUserGroup(ldapuser=instance, group=group_selected)
                instance___ldapusergroup.save()
            # permissions
            # permissions seleccionados en el formulario
            permissions_selected = self.cleaned_data.get('permissions')
            # to add permissions
            for permission_selected in permissions_selected:
                instance___ldapuserpermission = models.LDAPUserPermission(ldapuser=instance, permission=permission_selected)
                instance___ldapuserpermission.save()
            #
            # LDAP
            ldap.void___action_ldapuser_instance_create(instance=instance)
        return instance


class LDAPUserDetail(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    created = FIELD_CREATED
    modified = FIELD_MODIFIED
    avatar = FIELD_AVATAR
    first_name = FIELD_FIRST_NAME
    last_name = FIELD_LAST_NAME
    identifier = FIELD_IDENTIFIER
    email = FIELD_EMAIL
    detail = FIELD_DETAIL
    groups = FIELD_GROUPS
    permissions = FIELD_PERMISSIONS

    class Meta:
        model = models.LDAPUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def detail(self):
        #
        # LDAP
        ldap.void___action_ldapuser_instance_update(instance=self.instance)


class LDAPUserUpdate(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    avatar = FIELD_AVATAR
    first_name = FIELD_FIRST_NAME
    last_name = FIELD_LAST_NAME
    identifier = FIELD_IDENTIFIER
    email = FIELD_EMAIL
    password = FIELD_PASSWORD
    password_confirmation = FIELD_PASSWORD_CONFIRMATION
    detail = FIELD_DETAIL
    groups = FIELD_GROUPS
    permissions = FIELD_PERMISSIONS

    class Meta:
        model = models.LDAPUser
        fields = ['is_active', 'avatar', 'first_name', 'last_name', 'identifier', 'email', 'password', 'detail', 'groups', 'permissions', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.instance_current = kwargs.pop('instance_current')
        super().__init__(*args, **kwargs)
        #
        # is_active
        void___field_attribute_help_text_locale_reload(field=self.fields['is_active'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_IS_ACTIVE_HELP_TEXT')
        # first_name
        void___field_attribute_placeholder_locale_reload(field=self.fields['first_name'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_FIRST_NAME')
        self.fields['first_name'].widget.attrs['autofocus'] = True
        # last name
        void___field_attribute_placeholder_locale_reload(field=self.fields['last_name'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_LAST_NAME')
        # identifier
        void___field_attribute_placeholder_locale_reload(field=self.fields['identifier'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_IDENTIFIER')
        # email
        void___field_attribute_placeholder_locale_reload(field=self.fields['email'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_EMAIL')
        # password
        void___field_attribute_placeholder_locale_reload(field=self.fields['password'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_PASSWORD')
        # password_confirmation
        void___field_attribute_placeholder_locale_reload(field=self.fields['password_confirmation'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_PASSWORD_CONFIRMATION')
        # detail
        void___field_attribute_placeholder_locale_reload(field=self.fields['detail'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_DETAIL')
        void___field_attribute_help_text_locale_reload(field=self.fields['detail'], locale='ADMINISTRATION_MODULE_SECURITY_LDAPUSER_DETAIL_HELP_TEXT')
        # groups
        self.groups_choices = models.Group.objects.all()
        # permissions
        self.permissions_choices = models.Permission.objects.all()

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if self.files.get('avatar'):
            if len(self.files.get('avatar')) > 1 * 1024 * 1024:  # 1MB
                raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION The avatar should not be beggear than %(weight)s.') % {'weight': '1mb', })
        return avatar

    def clean_identifier(self):
        identifier = self.cleaned_data.get('identifier')
        try:
            instance = models.LDAPUser.objects.get(identifier=identifier)
        except models.LDAPUser.DoesNotExist:
            try:
                instance = models.RequestedLDAPUser.objects.get(identifier=identifier)
            except models.RequestedLDAPUser.DoesNotExist:
                return identifier
        if instance.identifier == self.instance_current.identifier:
            return identifier
        raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION This identifier has already been chosen.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            instance = models.LDAPUser.objects.get(email=email)
        except models.LDAPUser.DoesNotExist:
            try:
                instance = models.RequestedLDAPUser.objects.get(email=email)
            except models.RequestedLDAPUser.DoesNotExist:
                return email
        if instance.email == self.instance_current.email:
            return email
        raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION This email has already been chosen.'))

    def clean(self):
        ___clean___ = super(LDAPUserUpdate, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password', _('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION The password and your confirmation do not match.'))
            self.add_error('password_confirmation', _('ADMINISTRATION_MODULE_SECURITY_LDAPUSER_VALIDATION The password and your confirmation do not match.'))
        return ___clean___

    def save(self, commit=True):
        instance = super(LDAPUserUpdate, self).save(commit=False)
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
            # groups
            # groups a los que pertenece
            instances___group = instance.groups.all()
            # groups seleccionados en el formulario
            groups_selected = self.cleaned_data.get('groups')
            # groups que tenian que no se seleccionaron ahora
            instances___group_to_delete = [x for x in instances___group if x not in groups_selected]
            # groups que se seleccionaron ahora que no tenia
            instances___group_to_add = [x for x in groups_selected if x not in instances___group]
            # to delete groups
            for instance___group_to_delete in instances___group_to_delete:
                instance___ldapusergroup = models.LDAPUserGroup.objects.get(ldapuser=instance, group=instance___group_to_delete)
                instance___ldapusergroup.delete()
            # to add groups
            for instance___group_to_add in instances___group_to_add:
                instance___ldapusergroup = models.LDAPUserGroup(ldapuser=instance, group=instance___group_to_add)
                instance___ldapusergroup.save()
            # permissions
            # permissions a los que pertenece
            instances___permission = instance.permissions.all()
            # permissions seleccionados en el formulario
            permissions_selected = self.cleaned_data.get('permissions')
            # permissions que tenian que no se seleccionaron ahora
            instances___permission_to_delete = [x for x in instances___permission if x not in permissions_selected]
            # permissions que se seleccionaron ahora que no tenia
            instances___permission_to_add = [x for x in permissions_selected if x not in instances___permission]
            # to delete permissions
            for instance___permission_to_delete in instances___permission_to_delete:
                instance___ldapuserpermission = models.LDAPUserPermission.objects.get(ldapuser=instance, permission=instance___permission_to_delete)
                instance___ldapuserpermission.delete()
            # to add permissions
            for instance___permission_to_add in instances___permission_to_add:
                instance___ldapuserpermission = models.LDAPUserPermission(ldapuser=instance, permission=instance___permission_to_add)
                instance___ldapuserpermission.save()
            # save to data base
            instance.save()
            #
            # LDAP
            ldap.void___action_ldapuser_instance_update(instance=instance)
        return instance


class LDAPUserDelete(forms.ModelForm):
    class Meta:
        model = models.LDAPUser
        fields = ['id', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def delete(self):
        # avatar
        if self.instance.avatar is not None and self.instance.avatar != '':
            if os.path.exists(self.instance.string___folder_path()):
                shutil.rmtree(self.instance.string___folder_path())
        # instance delete
        self.instance.delete()
        #
        # LDAP
        ldap.void___action_ldapuser_instance_delete(instance=self.instance)
