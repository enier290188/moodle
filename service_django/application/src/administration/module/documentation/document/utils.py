# -*- coding: utf-8 -*-
from . import forms
from src.documentation import models

# The model to administrate
MODEL = models.Document
# The path of model to administrate.
MODEL_PATH = 'document'
# Pagination
INSTANCES_AMOUNT_PER_PAGE = 1000000
# The forms of model to administrate
FORM_CREATE = forms.DocumentCreate
FORM_DETAIL = forms.DocumentDetail
FORM_UPDATE = forms.DocumentUpdate
FORM_DELETE = forms.DocumentDelete
