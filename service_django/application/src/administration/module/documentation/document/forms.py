# -*- coding: utf-8 -*-
from src.documentation import models
from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _
import copy

FIELD_IS_ACTIVE = forms.BooleanField(
    label=_('ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_IS_ACTIVE'),
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
    label=_('ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_CREATED'),
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
    label=_('ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_MODIFIED'),
    required=False,
    widget=forms.DateInput(
        attrs={
            'id': 'modified',
            'aria-describedby': 'modified_icon',
            'icon': 'fa fa-clock-o',
        },
    ),
)
FIELD_TITLE = forms.CharField(
    label=_('ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_TITLE'),
    required=False,
    min_length=1,
    max_length=1024,
    validators=[
        validators.RegexValidator('^[\w .\-_]+$', message=_('ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_VALIDATION Only letters, numbers and special characters dot, -, _ and space.')),
    ],
    widget=forms.TextInput(
        attrs={
            'id': 'title',
            'class': 'form-control',
            'aria-describedby': 'title_icon',
            'icon': 'fa fa-globe',
        },
    ),
)
FIELD_CONTENT = forms.CharField(
    label=_('ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_CONTENT'),
    required=False,
    widget=forms.Textarea(
        attrs={
            'id': 'content',
            'class': 'form-control',
            'icon': 'fa fa-globe',
            'rows': 5,
        },
    ),
)


def void___field_attribute_placeholder_locale_reload(field, locale):
    field.widget.attrs['placeholder'] = '- %s -' % (_(locale),)


def void___field_attribute_help_text_locale_reload(field, locale):
    field.help_text = '\"%s\"' % (_(locale),)


class DocumentCreate(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    title_en = copy.deepcopy(FIELD_TITLE)
    title_es = copy.deepcopy(FIELD_TITLE)
    content_en = copy.deepcopy(FIELD_CONTENT)
    content_es = copy.deepcopy(FIELD_CONTENT)

    class Meta:
        model = models.Document
        fields = ['is_active', 'title_en', 'title_es', 'content_en', 'content_es', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        #
        # is_active
        void___field_attribute_help_text_locale_reload(field=self.fields['is_active'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_IS_ACTIVE_HELP_TEXT')
        self.fields['is_active'].initial = True
        # title_en
        void___field_attribute_placeholder_locale_reload(field=self.fields['title_en'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_TITLE')
        self.fields['title_en'].widget.attrs['id'] = 'title_en'
        self.fields['title_en'].widget.attrs['aria-describedby'] = 'title_en_icon'
        # title_es
        void___field_attribute_placeholder_locale_reload(field=self.fields['title_es'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_TITLE')
        self.fields['title_es'].widget.attrs['id'] = 'title_es'
        self.fields['title_es'].widget.attrs['aria-describedby'] = 'title_es_icon'
        # content_en
        void___field_attribute_placeholder_locale_reload(field=self.fields['content_en'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_CONTENT')
        self.fields['content_en'].widget.attrs['id'] = 'content_en'
        # content_es
        void___field_attribute_placeholder_locale_reload(field=self.fields['content_es'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_CONTENT')
        self.fields['content_es'].widget.attrs['id'] = 'content_es'

    def save(self, commit=True):
        instance = super(DocumentCreate, self).save(commit=False)
        #
        if commit:
            # save to data base
            instance.save()
        return instance


class DocumentDetail(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    created = FIELD_CREATED
    modified = FIELD_MODIFIED
    title = FIELD_TITLE

    class Meta:
        model = models.Document
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class DocumentUpdate(forms.ModelForm):
    is_active = FIELD_IS_ACTIVE
    title_en = copy.deepcopy(FIELD_TITLE)
    title_es = copy.deepcopy(FIELD_TITLE)
    content_en = copy.deepcopy(FIELD_CONTENT)
    content_es = copy.deepcopy(FIELD_CONTENT)

    class Meta:
        model = models.Document
        fields = ['is_active', 'title_en', 'title_es', 'content_en', 'content_es', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.instance_current = kwargs.pop('instance_current')
        super().__init__(*args, **kwargs)
        #
        # is_active
        void___field_attribute_help_text_locale_reload(field=self.fields['is_active'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_IS_ACTIVE_HELP_TEXT')
        # title_en
        void___field_attribute_placeholder_locale_reload(field=self.fields['title_en'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_TITLE')
        self.fields['title_en'].widget.attrs['id'] = 'title_en'
        self.fields['title_en'].widget.attrs['aria-describedby'] = 'title_en_icon'
        # title_es
        void___field_attribute_placeholder_locale_reload(field=self.fields['title_es'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_TITLE')
        self.fields['title_es'].widget.attrs['id'] = 'title_es'
        self.fields['title_es'].widget.attrs['aria-describedby'] = 'title_es_icon'
        # content_en
        void___field_attribute_placeholder_locale_reload(field=self.fields['content_en'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_CONTENT')
        self.fields['content_en'].widget.attrs['id'] = 'content_en'
        # content_es
        void___field_attribute_placeholder_locale_reload(field=self.fields['content_es'], locale='ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_CONTENT')
        self.fields['content_es'].widget.attrs['id'] = 'content_es'

    def clean_is_active(self):
        is_active = self.cleaned_data.get('is_active')
        if is_active is True:
            if self.instance_current.parent != 0:
                instance_parent = models.Document.objects.get(pk=self.instance.parent)
                if instance_parent is not None and instance_parent.is_active is False:
                    raise forms.ValidationError(_('ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_VALIDATION This instance is a branch of a non-active instance, so it can not be activated.'))
        return is_active

    def save(self, commit=True):
        instance = super(DocumentUpdate, self).save(commit=False)
        #
        if commit:
            # save to data base
            instance.save()
            #
            # is_active
            if instance.is_active is False:
                instances = models.Document.objects.all()
                # get parents of instance
                list_int___parent = []
                temporal_int___parent = instance.parent
                while temporal_int___parent != 0:
                    list_int___parent.append(temporal_int___parent)
                    temporal_instance = models.Document.objects.get(pk=temporal_int___parent)
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


class DocumentDelete(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ['id', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        ___clean___ = super(DocumentDelete, self).clean()
        instances = models.Document.objects.all()
        for temporal_instance in instances:
            if temporal_instance.parent == self.instance.pk:
                raise forms.ValidationError(_('ADMINISTRATION_MODULE_DOCUMENTATION_DOCUMENT_VALIDATION There are instances that are branches of this instance, so it can not be deleted.'))
        return ___clean___
