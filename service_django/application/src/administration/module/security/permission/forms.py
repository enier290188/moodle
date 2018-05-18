from src.security import models
from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _

FIELD_IS_ACTIVE = forms.BooleanField(
    label=_('ADMINISTRATION_MODULE_SECURITY_PERMISSION_IS_ACTIVE'),
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
    label=_('ADMINISTRATION_MODULE_SECURITY_PERMISSION_CREATED'),
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
    label=_('ADMINISTRATION_MODULE_SECURITY_PERMISSION_MODIFIED'),
    required=False,
    widget=forms.DateInput(
        attrs={
            'id': 'modified',
            'aria-describedby': 'modified_icon',
            'icon': 'fa fa-clock-o',
        },
    ),
)
FIELD_NAME = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_PERMISSION_NAME'),
    required=True,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w .\-_]+$', message=_('ADMINISTRATION_MODULE_SECURITY_PERMISSION_VALIDATION Only letters, numbers and special characters dot, -, _ and space.')),
    ],
    widget=forms.TextInput(
        attrs={
            'id': 'name',
            'class': 'form-control',
            'aria-describedby': 'name_icon',
            'icon': 'fa fa-globe',
        },
    ),
)
FIELD_IDENTIFIER = forms.CharField(
    label=_('ADMINISTRATION_MODULE_SECURITY_PERMISSION_IDENTIFIER'),
    required=True,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w.]+$', message=_('ADMINISTRATION_MODULE_SECURITY_PERMISSION_VALIDATION Only letters, numbers and the special character dot.')),
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


def void___field_attribute_placeholder_locale_reload(field, locale):
    field.widget.attrs['placeholder'] = '- %s -' % (_(locale),)


def void___field_attribute_help_text_locale_reload(field, locale):
    field.help_text = '\"%s\"' % (_(locale),)


class PermissionDetail(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    created = FIELD_CREATED
    modified = FIELD_MODIFIED
    name = FIELD_NAME
    identifier = FIELD_IDENTIFIER

    class Meta:
        model = models.Permission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class PermissionUpdate(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    name = FIELD_NAME
    identifier = FIELD_IDENTIFIER

    class Meta:
        model = models.Permission
        fields = ['is_active', 'name', 'identifier', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.instance_current = kwargs.pop('instance_current')
        super().__init__(*args, **kwargs)
        #
        # is_active
        void___field_attribute_help_text_locale_reload(field=self.fields['is_active'], locale='ADMINISTRATION_MODULE_SECURITY_PERMISSION_IS_ACTIVE_HELP_TEXT')
        # name
        void___field_attribute_placeholder_locale_reload(field=self.fields['name'], locale='ADMINISTRATION_MODULE_SECURITY_PERMISSION_NAME')
        self.fields['name'].widget.attrs['autofocus'] = True
        # identifier
        void___field_attribute_placeholder_locale_reload(field=self.fields['identifier'], locale='ADMINISTRATION_MODULE_SECURITY_PERMISSION_IDENTIFIER')
        self.fields['identifier'].widget.attrs['readonly'] = 'readonly'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = ' '.join(name.split())
        try:
            instance = models.Permission.objects.get(name=name)
        except models.Permission.DoesNotExist:
            return name
        if instance.name == self.instance_current.name:
            return name
        raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_PERMISSION_VALIDATION This name has already been chosen.'))

    def clean_identifier(self):
        identifier = self.instance_current.identifier
        return identifier

    def save(self, commit=True):
        instance = super(PermissionUpdate, self).save(commit=False)
        #
        if commit:
            # save to data base
            instance.save()
        return instance
