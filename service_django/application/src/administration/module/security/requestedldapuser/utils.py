# -*- coding: utf-8 -*-
from . import forms
from src.security import ldap, models

# The model to administrate
MODEL = models.RequestedLDAPUser
# The path of model to administrate.
MODEL_PATH = 'requestedldapuser'
# Pagination
INSTANCES_AMOUNT_PER_PAGE = 10
# The forms of model to administrate
FORM_DETAIL = forms.RequestedLDAPUserDetail
FORM_APPROVE = forms.RequestedLDAPUserApprove
FORM_DISAPPROVE = forms.RequestedLDAPUserDisapprove


def boolean___initial_approve(request, data):
    # LDAP
    ldap.messages___action_is_there_connection(request=request)
    return True
