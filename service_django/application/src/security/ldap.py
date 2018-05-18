# -*- coding: utf-8 -*-
from . import models
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
import ldap3


def connection___ldap():
    # The server and the connection are created with the default parameters
    # define the server
    # define an unsecure LDAP server, requesting info on DSE and schema
    server = ldap3.Server(
        host=settings.LDAP_SERVER_HOST,
        port=settings.LDAP_SERVER_PORT,
        use_ssl=False,
        get_info=ldap3.ALL
    )
    # define the connection
    connection = ldap3.Connection(
        server=server,
        user=settings.LDAP_SERVER_USER,
        password=settings.LDAP_SERVER_PASSWORD,
        auto_bind='NONE',
        version=3,
        authentication='SIMPLE',
        client_strategy='SYNC',
        auto_referrals=True,
        check_names=True,
        read_only=False,
        lazy=False,
        raise_exceptions=False
    )
    return connection


##########################################################################################
def boolean___ldap_ldapuser_group_instances_search(connection):
    # perform the operation search
    boolean___is_find = connection.search(
        search_base=settings.LDAP_SERVER_GROUPS_SEARCH_BASE,
        search_filter='(&(objectClass=posixGroup))',
        search_scope=ldap3.SUBTREE,
        attributes=['cn', 'gidNumber', ]
    )
    return boolean___is_find


def boolean___ldap_ldapuser_instances_search(connection, string___gidnumber):
    # perform the operation search
    boolean___is_find = connection.search(
        search_base=settings.LDAP_SERVER_GROUPS_SEARCH_BASE,
        search_filter='(&(objectClass=posixGroup)(gidNumber=%s))' % (string___gidnumber,),
        search_scope=ldap3.SUBTREE,
        attributes=['cn', 'gidNumber', ]
    )
    if boolean___is_find:
        boolean___is_find = connection.search(
            search_base='ou=%s,%s' % (str(connection.entries[0].cn), settings.LDAP_SERVER_USERS_SEARCH_BASE,),
            search_filter='(&(objectClass=inetOrgPerson)(objectClass=posixAccount)(objectClass=top)(gidNumber=%s))' % (string___gidnumber,),
            search_scope=ldap3.SUBTREE,
            attributes=['uid', 'uidNumber', 'gidNumber', 'givenName', 'sn', 'mail', 'userPassword', 'description', 'homeDirectory', ]
        )
    return boolean___is_find


def boolean___ldap_ldapuser_instance_search(connection, instance):
    # perform the operation search
    boolean___is_find = connection.search(
        search_base='ou=%s,%s' % (settings.LDAP_SERVER_GROUPS_GROUP_CN, settings.LDAP_SERVER_USERS_SEARCH_BASE,),
        search_filter='(&(objectClass=inetOrgPerson)(objectClass=posixAccount)(objectClass=top)(uidNumber=%s)(gidNumber=%s))' % (100000 + instance.pk, settings.LDAP_SERVER_GROUPS_GROUP_GIDNUMBER,),
        search_scope=ldap3.SUBTREE,
        attributes=['uid', 'uidNumber', 'gidNumber', ]
    )
    return boolean___is_find


def boolean___ldap_ldapuser_instance_create(connection, instance):
    # perform the operation create
    boolean___is_add = connection.add(
        dn='uid=%s,ou=%s,%s' % (instance.identifier, settings.LDAP_SERVER_GROUPS_GROUP_CN, settings.LDAP_SERVER_USERS_SEARCH_BASE,),
        object_class=['inetOrgPerson', 'posixAccount', 'top'],
        attributes={
            'uid': instance.identifier,
            'uidNumber': '%s' % (100000 + instance.pk),
            'gidNumber': settings.LDAP_SERVER_GROUPS_GROUP_GIDNUMBER,
            'cn': instance.__str__(),
            'givenName': (instance.first_name if instance.first_name != '' else '-'),
            'sn': (instance.last_name if instance.last_name != '' else '-'),
            'mail': instance.email,
            'userPassword': instance.password,
            'description': instance.detail,
            'homeDirectory': '%s%s/%s' % (settings.LDAP_SERVER_USERS_HOMEDIRECTORY, settings.LDAP_SERVER_GROUPS_GROUP_CN, instance.identifier,),
            'loginShell': '/bin/bash',
            #
            # 'institute': 'institute',
            # 'researchField': 'researchField',
            # 'researchGroup': 'researchGroup',
            # 'serviceType': 'serviceType',
            # 'userProfile': 'userProfile',
        }
    )
    return boolean___is_add


def boolean_ldap_ldapuser_instance_update(connection, instance):
    boolean___is_update = True
    # perform the operation search
    boolean___is_find = boolean___ldap_ldapuser_instance_search(
        connection=connection,
        instance=instance
    )
    if boolean___is_find:
        if instance.identifier != str(connection.entries[0].uid):
            # perform the operation update dn
            boolean___is_update = connection.modify_dn(
                dn='uid=%s,ou=%s,%s' % (str(connection.entries[0].uid), settings.LDAP_SERVER_GROUPS_GROUP_CN, settings.LDAP_SERVER_USERS_SEARCH_BASE,),
                relative_dn='uid=%s' % (instance.identifier,)
            )
        if boolean___is_update:
            # perform the operation update
            boolean___is_update = connection.modify(
                dn='uid=%s,ou=%s,%s' % (instance.identifier, settings.LDAP_SERVER_GROUPS_GROUP_CN, settings.LDAP_SERVER_USERS_SEARCH_BASE,),
                changes={
                    'uidNumber': [(ldap3.MODIFY_REPLACE, [100000 + instance.pk])],
                    'gidNumber': [(ldap3.MODIFY_REPLACE, [settings.LDAP_SERVER_GROUPS_GROUP_GIDNUMBER])],
                    'cn': [(ldap3.MODIFY_REPLACE, [instance.__str__()])],
                    'givenName': [(ldap3.MODIFY_REPLACE, [(instance.first_name if instance.first_name != '' else '-')])],
                    'sn': [(ldap3.MODIFY_REPLACE, [(instance.last_name if instance.last_name != '' else '-')])],
                    'mail': [(ldap3.MODIFY_REPLACE, [instance.email])],
                    'userPassword': [(ldap3.MODIFY_REPLACE, [instance.password])],
                    'description': [(ldap3.MODIFY_REPLACE, [instance.detail])],
                    'homeDirectory': [(ldap3.MODIFY_REPLACE, ['%s%s/%s' % (settings.LDAP_SERVER_USERS_HOMEDIRECTORY, settings.LDAP_SERVER_GROUPS_GROUP_CN, instance.identifier,)])],
                    'loginShell': [(ldap3.MODIFY_REPLACE, ['/bin/bash'])],
                    #
                    # 'institute': [(ldap3.MODIFY_REPLACE, ['institute'])],
                    # 'researchField': [(ldap3.MODIFY_REPLACE, ['researchField'])],
                    # 'researchGroup': [(ldap3.MODIFY_REPLACE, ['researchGroup'])],
                    # 'serviceType': [(ldap3.MODIFY_REPLACE, ['serviceType'])],
                    # 'userProfile': [(ldap3.MODIFY_REPLACE, ['userProfile'])],
                }
            )
    return boolean___is_update


def boolean___ldap_ldapuser_instance_delete(connection, instance):
    # perform the operation delete
    boolean___is_delete = connection.delete(
        dn='uid=%s,ou=%s,%s' % (instance.identifier, settings.LDAP_SERVER_GROUPS_GROUP_CN, settings.LDAP_SERVER_USERS_SEARCH_BASE,)
    )
    return boolean___is_delete


##########################################################################################
def void___ldap_ldapuser_instances_synchronize(connection):
    # synchronize ldapuser instances
    instances = models.LDAPUser.objects.all()
    for instance in instances:
        # perform the operation search
        boolean___is_find = boolean___ldap_ldapuser_instance_search(
            connection=connection,
            instance=instance
        )
        if boolean___is_find:
            # perform the operation update
            boolean_ldap_ldapuser_instance_update(
                connection=connection,
                instance=instance
            )
        else:
            # perform the operation create
            boolean___ldap_ldapuser_instance_create(
                connection=connection,
                instance=instance
            )
    # perform the operation search
    boolean___is_find = boolean___ldap_ldapuser_instances_search(
        connection=connection,
        string___gidnumber=settings.LDAP_SERVER_GROUPS_GROUP_GIDNUMBER
    )
    if boolean___is_find:
        list_entry___to_delete = list()
        for entry in connection.entries:
            string___uid = str(entry.uid)
            string___uidnumber = str(entry.uidNumber)
            string___homedirectory = str(entry.homeDirectory)
            boolean___delete = True
            for instance in instances:
                uid = instance.identifier
                uidnumber = '%s' % (100000 + instance.pk)
                homedirectory = '%s%s/%s' % (settings.LDAP_SERVER_USERS_HOMEDIRECTORY, settings.LDAP_SERVER_GROUPS_GROUP_CN, instance.identifier,)
                if uid == string___uid and uidnumber == string___uidnumber and homedirectory == string___homedirectory:
                    boolean___delete = False
                    break
            if boolean___delete is True:
                list_entry___to_delete.append(entry)
        for entry in list_entry___to_delete:
            # perform the operation update
            connection.delete(
                dn='uid=%s,ou=%s,%s' % (str(entry.uid), settings.LDAP_SERVER_GROUPS_GROUP_CN, settings.LDAP_SERVER_USERS_SEARCH_BASE,)
            )


##########################################################################################
def messages___action_is_there_connection(request):
    boolean___is_there_connection = False
    connection = connection___ldap()
    try:
        # start the connection
        if connection.bind():
            boolean___is_there_connection = True
    except (Exception,):
        pass
    finally:
        # close the connection
        connection.unbind()
    if boolean___is_there_connection is False:
        messages.add_message(request, messages.WARNING, _('SECURITY_MESSAGE Connection to the LDAP could not be established. When the connection will be place, the action will be perform in the LDAP.'))


def void___action_ldapuser_instance_create(instance):
    connection = connection___ldap()
    try:
        # start the connection
        if connection.bind():
            # perform the operation search
            boolean___is_find = boolean___ldap_ldapuser_instance_search(
                connection=connection,
                instance=instance
            )
            if boolean___is_find:
                # perform the operation delete
                boolean___ldap_ldapuser_instance_delete(
                    connection=connection,
                    instance=instance
                )
            # perform the operation create
            boolean___ldap_ldapuser_instance_create(
                connection=connection,
                instance=instance
            )
    except (Exception,):
        pass
    finally:
        # close the connection
        connection.unbind()


def void___action_ldapuser_instance_update(instance):
    connection = connection___ldap()
    try:
        # start the connection
        if connection.bind():
            # perform the operation search
            boolean___is_find = boolean___ldap_ldapuser_instance_search(
                connection=connection,
                instance=instance
            )
            if boolean___is_find:
                # perform the operation update
                boolean_ldap_ldapuser_instance_update(
                    connection=connection,
                    instance=instance
                )
            else:
                # perform the operation create
                boolean___ldap_ldapuser_instance_create(
                    connection=connection,
                    instance=instance
                )
    except (Exception,):
        pass
    finally:
        # close the connection
        connection.unbind()


def void___action_ldapuser_instance_delete(instance):
    connection = connection___ldap()
    try:
        # start the connection
        if connection.bind():
            # perform the operation delete
            boolean___ldap_ldapuser_instance_delete(
                connection=connection,
                instance=instance
            )
    except (Exception,):
        pass
    finally:
        # close the connection
        connection.unbind()


def void___action_user_instances_synchronize():
    connection = connection___ldap()
    try:
        # start the connection
        if connection.bind():
            void___ldap_ldapuser_instances_synchronize(connection=connection)
    except (Exception,):
        pass
    finally:
        # close the connection
        connection.unbind()
