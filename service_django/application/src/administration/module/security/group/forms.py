# -*- coding: utf-8 -*-
from src.security import models
from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _

FIELD_IS_ACTIVE = forms.BooleanField(
    label=_('ADMINISTRATION_MODULE_SECURITY_GROUP_IS_ACTIVE'),
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
    label=_('ADMINISTRATION_MODULE_SECURITY_GROUP_CREATED'),
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
    label=_('ADMINISTRATION_MODULE_SECURITY_GROUP_MODIFIED'),
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
    label=_('ADMINISTRATION_MODULE_SECURITY_GROUP_NAME'),
    required=True,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[\w .\-_]+$', message=_('ADMINISTRATION_MODULE_SECURITY_GROUP_VALIDATION Only letters, numbers and special characters dot, -, _ and space.')),
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
FIELD_PERMISSIONS = forms.ModelMultipleChoiceField(
    label=_('ADMINISTRATION_MODULE_SECURITY_GROUP_PERMISSIONS'),
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


class GroupCreate(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    name = FIELD_NAME
    permissions = FIELD_PERMISSIONS

    class Meta:
        model = models.Group
        fields = ['is_active', 'name', 'permissions', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # is_active
        void___field_attribute_help_text_locale_reload(field=self.fields['is_active'], locale='ADMINISTRATION_MODULE_SECURITY_GROUP_IS_ACTIVE_HELP_TEXT')
        self.fields['is_active'].initial = True
        # name
        void___field_attribute_placeholder_locale_reload(field=self.fields['name'], locale='ADMINISTRATION_MODULE_SECURITY_GROUP_NAME')
        self.fields['name'].widget.attrs['autofocus'] = True
        # permissions
        self.permissions_choices = models.Permission.objects.all()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = ' '.join(name.split())
        try:
            models.Group.objects.get(name=name)
        except models.Group.DoesNotExist:
            return name
        raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_GROUP_VALIDATION This name has already been chosen.'))

    def save(self, commit=True):
        instance = super(GroupCreate, self).save(commit=False)
        #
        if commit:
            # save to data base
            instance.save()
            #
            # permissions
            # permissions seleccionados en el formulario
            permissions_selected = self.cleaned_data.get('permissions')
            # to add permissions
            for permission_selected in permissions_selected:
                instance___grouppermission = models.GroupPermission(group=instance, permission=permission_selected)
                instance___grouppermission.save()
        return instance


class GroupDetail(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    created = FIELD_CREATED
    modified = FIELD_MODIFIED
    name = FIELD_NAME
    permissions = FIELD_PERMISSIONS

    class Meta:
        model = models.Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class GroupUpdate(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    name = FIELD_NAME
    permissions = FIELD_PERMISSIONS

    class Meta:
        model = models.Group
        fields = ['is_active', 'name', 'permissions', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.instance_current = kwargs.pop('instance_current')
        super().__init__(*args, **kwargs)
        #
        # is_active
        void___field_attribute_help_text_locale_reload(field=self.fields['is_active'], locale='ADMINISTRATION_MODULE_SECURITY_GROUP_IS_ACTIVE_HELP_TEXT')
        # name
        void___field_attribute_placeholder_locale_reload(field=self.fields['name'], locale='ADMINISTRATION_MODULE_SECURITY_GROUP_NAME')
        self.fields['name'].widget.attrs['autofocus'] = True
        # permissions
        self.permissions_choices = models.Permission.objects.all()

    def clean_is_active(self):
        is_active = self.cleaned_data.get('is_active')
        if is_active is True:
            if self.instance_current.parent != 0:
                instance_parent = models.Group.objects.get(pk=self.instance.parent)
                if instance_parent is not None and instance_parent.is_active is False:
                    raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_GROUP_VALIDATION This instance is a branch of a non-active instance, so it can not be activated.'))
        return is_active

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = ' '.join(name.split())
        try:
            instance = models.Group.objects.get(name=name)
        except models.Group.DoesNotExist:
            return name
        if instance.name == self.instance_current.name:
            return name
        raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_GROUP_VALIDATION This name has already been chosen.'))

    def save(self, commit=True):
        instance = super(GroupUpdate, self).save(commit=False)
        #
        if commit:
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
                instance___grouppermission = models.GroupPermission.objects.get(group=instance, permission=instance___permission_to_delete)
                instance___grouppermission.delete()
            # to add permissions
            for instance___permission_to_add in instances___permission_to_add:
                instance___grouppermission = models.GroupPermission(group=instance, permission=instance___permission_to_add)
                instance___grouppermission.save()
            # save to data base
            instance.save()
            #
            # is_active
            if instance.is_active is False:
                instances = models.Group.objects.all()
                # get parents of instance
                list_int___parent = []
                temporal_int___parent = instance.parent
                while temporal_int___parent != 0:
                    list_int___parent.append(temporal_int___parent)
                    temporal_instance = models.Group.objects.get(pk=temporal_int___parent)
                    temporal_int___parent = temporal_instance.parent
                list_int___parent.append(0)
                # count children of instance
                int___children_amount = 0
                for temporal_instance in instances[instance.position:]:
                    if temporal_instance.parent in list_int___parent:
                        break
                    int___children_amount += 1
                # change is_active to False
                for temporal_instance in instances[instance.position - 1:instance.position + int___children_amount]:
                    temporal_instance.is_active = False
                    temporal_instance.save()
        return instance


class GroupDelete(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ['id', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        ___clean___ = super(GroupDelete, self).clean()
        instances = models.Group.objects.all()
        for temporal_instance in instances:
            if temporal_instance.parent == self.instance.pk:
                raise forms.ValidationError(_('ADMINISTRATION_MODULE_SECURITY_GROUP_VALIDATION There are instances that are branches of this instance, so it can not be deleted.'))
        return ___clean___
