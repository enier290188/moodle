# -*- coding: utf-8 -*-
from . import forms
from src.security import models

# The model to administrate
MODEL = models.Permission
# The path of model to administrate.
MODEL_PATH = 'permission'
# Pagination
INSTANCES_AMOUNT_PER_PAGE = 1000000
# The forms of model to administrate
FORM_DETAIL = forms.PermissionDetail
FORM_UPDATE = forms.PermissionUpdate
