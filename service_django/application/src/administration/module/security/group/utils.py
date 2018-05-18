# -*- coding: utf-8 -*-
from . import forms
from src.security import models

# The model to administrate
MODEL = models.Group
# The path of model to administrate.
MODEL_PATH = 'group'
# Pagination
INSTANCES_AMOUNT_PER_PAGE = 1000000
# The forms of model to administrate
FORM_CREATE = forms.GroupCreate
FORM_DETAIL = forms.GroupDetail
FORM_UPDATE = forms.GroupUpdate
FORM_DELETE = forms.GroupDelete


def void___table_tbody_and_pagination_tree_reload(request, data, instance):
    # get parents of instance
    list_int___group_parent = []
    temporal_int___group_parent = instance.parent
    if temporal_int___group_parent != 0:
        while temporal_int___group_parent != 0:
            list_int___group_parent.append(temporal_int___group_parent)
            temporal_instance___group_parent = models.Group.objects.instance___by_pk(pk=temporal_int___group_parent)
            temporal_int___group_parent = temporal_instance___group_parent.parent
        #
        instances___localusergroup = models.LOCALUserGroup.objects.filter(group=instance.pk)
        for instance___localusergroup in instances___localusergroup:
            # parents que tiene ahora que no tiene incluidos
            list_int___group_parent_selected = [x.pk for x in instance___localusergroup.localuser.groups.all()]
            list_int___group_parent_to_add = [x for x in list_int___group_parent if x not in list_int___group_parent_selected]
            for int___group_parent_to_add in list_int___group_parent_to_add:
                temporal_instance___group_parent_to_add = models.Group.objects.instance___by_pk(pk=int___group_parent_to_add)
                temporal_instance___localusergroup_to_save = models.LOCALUserGroup(localuser=instance___localusergroup.localuser, group=temporal_instance___group_parent_to_add)
                temporal_instance___localusergroup_to_save.save()
        #
        instances___ldapusergroup = models.LDAPUserGroup.objects.filter(group=instance.pk)
        for instance___ldapusergroup in instances___ldapusergroup:
            # parents que tiene ahora que no tiene incluidos
            list_int___group_parent_selected = [x.pk for x in instance___ldapusergroup.ldapuser.groups.all()]
            list_int___group_parent_to_add = [x for x in list_int___group_parent if x not in list_int___group_parent_selected]
            for int___group_parent_to_add in list_int___group_parent_to_add:
                temporal_instance___group_parent_to_add = models.Group.objects.instance___by_pk(pk=int___group_parent_to_add)
                temporal_instance___ldapusergroup_to_save = models.LDAPUserGroup(ldapuser=instance___ldapusergroup.ldapuser, group=temporal_instance___group_parent_to_add)
                temporal_instance___ldapusergroup_to_save.save()
