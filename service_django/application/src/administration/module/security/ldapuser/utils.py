# -*- coding: utf-8 -*-
from . import forms
from src.security import ldap, models

# The model to administrate
MODEL = models.LDAPUser
# The path of model to administrate.
MODEL_PATH = 'ldapuser'
# Pagination
INSTANCES_AMOUNT_PER_PAGE = 10
# The forms of model to administrate
FORM_CREATE = forms.LDAPUserCreate
FORM_DETAIL = forms.LDAPUserDetail
FORM_UPDATE = forms.LDAPUserUpdate
FORM_DELETE = forms.LDAPUserDelete


def boolean___initial_create(request, data):
    # LDAP
    ldap.messages___action_is_there_connection(request=request)
    return True


def boolean___initial_detail(request, data):
    # LDAP
    ldap.messages___action_is_there_connection(request=request)
    return True


def boolean___initial_update(request, data):
    # LDAP
    ldap.messages___action_is_there_connection(request=request)
    return True


def boolean___initial_delete(request, data):
    # LDAP
    ldap.messages___action_is_there_connection(request=request)
    return True
