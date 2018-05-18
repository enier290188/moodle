# -*- coding: utf-8 -*-
from . import forms
from src.security import models

# The model to administrate
MODEL = models.LOCALUser
# The path of model to administrate.
MODEL_PATH = 'localuser'
# Pagination
INSTANCES_AMOUNT_PER_PAGE = 10
# The forms of model to administrate
FORM_CREATE = forms.LOCALUserCreate
FORM_DETAIL = forms.LOCALUserDetail
FORM_UPDATE = forms.LOCALUserUpdate
FORM_DELETE = forms.LOCALUserDelete
