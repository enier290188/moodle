# -*- coding: utf-8 -*-
from . import forms
from src.security import models

# The model to administrate
MODEL = models.RequestedLOCALUser
# The path of model to administrate.
MODEL_PATH = 'requestedlocaluser'
# Pagination
INSTANCES_AMOUNT_PER_PAGE = 10
# The forms of model to administrate
FORM_DETAIL = forms.RequestedLOCALUserDetail
FORM_APPROVE = forms.RequestedLOCALUserApprove
FORM_DISAPPROVE = forms.RequestedLOCALUserDisapprove
