# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import ldap, models
from celery import shared_task
from django.core import mail
from django.conf import settings


@shared_task()
def task___security_ldap_synchronize():
    ldap.void___action_user_instances_synchronize()


@shared_task()
def task___security_login_forgot_credential_delete_instances():
    instances___localuserforgotcredential = models.LOCALUserForgotCredential.objects.all()
    instances___ldapuserforgotcredential = models.LDAPUserForgotCredential.objects.all()
    for instance___localuserforgotcredential in instances___localuserforgotcredential:
        if instance___localuserforgotcredential.INT___MAXIMUM_TIME_OF_EXISTENCE <= instance___localuserforgotcredential.int___time_of_existence():
            instance___localuserforgotcredential.delete()
    for instance___ldapuserforgotcredential in instances___ldapuserforgotcredential:
        if instance___ldapuserforgotcredential.INT___MAXIMUM_TIME_OF_EXISTENCE <= instance___ldapuserforgotcredential.int___time_of_existence():
            instance___ldapuserforgotcredential.delete()


@shared_task()
def task___security_login_forgot_credential_1_send_mail(string___email, string___code):
    # Send mail with the verification code to the user who forgot their credential.
    try:
        string___subject = '::: MOODLE-%s ::: FORGOT CREDENTIAL :::' % (settings.LDAP_SERVER_GROUPS_GROUP_CN,)
        string___msg_plain = string___subject + '\n\n' \
                                                'CODE: %s' % (string___code,)
        string___msg_html = string___subject + '<br/><br/>' \
                                               'CODE: %s' % (string___code,)
        string___email_from = settings.EMAIL_USER_NOREPLY
        list_string___email_to = [string___email, ]
        mail.send_mail(
            subject=string___subject,
            message=string___msg_plain,
            html_message=string___msg_html,
            from_email=string___email_from,
            recipient_list=list_string___email_to,
            fail_silently=True
        )
    except (Exception,):
        pass


@shared_task()
def task___security_login_request_send_mail(string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail):
    # Send mail to users who approve the request.
    # Send mail to the user who made the request.
    try:
        string___subject = '::: MOODLE-%s ::: REQUEST USER :::' % (settings.LDAP_SERVER_GROUPS_GROUP_CN,)
        string___msg_plain_1 = string___subject + '\n\n' \
                                                  'User model: %s \n' \
                                                  'First name: %s \n' \
                                                  'Last name: %s \n' \
                                                  'Identifier: %s \n' \
                                                  'Email: %s \n' \
                                                  'Detail: %s \n' % (string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail,)
        string___msg_html_1 = string___subject + '<br/><br/>' \
                                                 'User model: %s <br/>' \
                                                 'First name: %s <br/>' \
                                                 'Last name: %s <br/>' \
                                                 'Identifier: %s <br/>' \
                                                 'Email: %s <br/>' \
                                                 'Detail: %s <br/>' % (string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail,)
        string___msg_plain_2 = string___subject + '\n\n' \
                                                  'The application administrators have received your request, you will receive an email informing you if it was accepted or canceled. ' \
                                                  '\n\n' \
                                                  'User model: %s \n' \
                                                  'First name: %s \n' \
                                                  'Last name: %s \n' \
                                                  'Identifier: %s \n' \
                                                  'Email: %s \n' \
                                                  'Detail: %s \n' % (string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail,)
        string___msg_html_2 = string___subject + '<br/><br/>' \
                                                 'The application administrators have received your request, you will receive an email informing you if it was accepted or canceled. <br/>' \
                                                 '<br/><br/>' \
                                                 'User model: %s <br/>' \
                                                 'First name: %s <br/>' \
                                                 'Last name: %s <br/>' \
                                                 'Identifier: %s <br/>' \
                                                 'Email: %s <br/>' \
                                                 'Detail: %s <br/>' % (string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail,)
        string___email_from = settings.EMAIL_USER_NOREPLY
        list_string___email_to_1 = list()
        instances___localuser = models.LOCALUser.objects.all()
        instances___ldapuser = models.LDAPUser.objects.all()
        for instance___localuser in instances___localuser:
            if instance___localuser.is_superuser or instance___localuser.boolean___has_permission(set_identifier___to_verify={'security_requestedlocaluser_approve', 'security_requestedlocaluser_disapprove', }):
                list_string___email_to_1.append(instance___localuser.email)
        for instance___ldapuser in instances___ldapuser:
            if instance___ldapuser.is_superuser or instance___ldapuser.boolean___has_permission(set_identifier___to_verify={'security_requestedldapuser_approve', 'security_requestedldapuser_disapprove', }):
                list_string___email_to_1.append(instance___ldapuser.email)
        list_string___email_to_2 = [string___email, ]
        #
        mail.send_mail(
            subject=string___subject,
            message=string___msg_plain_1,
            from_email=string___email_from,
            recipient_list=list_string___email_to_1,
            html_message=string___msg_html_1,
            fail_silently=True
        )
        mail.send_mail(
            subject=string___subject,
            message=string___msg_plain_2,
            html_message=string___msg_html_2,
            from_email=string___email_from,
            recipient_list=list_string___email_to_2,
            fail_silently=True
        )
    except (Exception,):
        pass


@shared_task()
def task___security_login_request_approve_send_mail(string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail):
    try:
        string___subject = '::: MOODLE-%s ::: REQUEST USER ::: APPROVE :::' % (settings.LDAP_SERVER_GROUPS_GROUP_CN,)
        string___msg_plain = string___subject + '\n\n' \
                                                'Your request was approved. \n\n' \
                                                'User model: %s \n' \
                                                'First name: %s \n' \
                                                'Last name: %s \n' \
                                                'Identifier: %s \n' \
                                                'Email: %s \n' \
                                                'Detail: %s \n' % (string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail,)
        string___msg_html = string___subject + '<br/><br/>' \
                                               'Your request was approved. <br/><br/>' \
                                               'User model: %s <br/>' \
                                               'First name: %s <br/>' \
                                               'Last name: %s <br/>' \
                                               'Identifier: %s <br/>' \
                                               'Email: %s <br/>' \
                                               'Detail: %s <br/>' % (string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail,)
        string___email_from = settings.EMAIL_USER_NOREPLY
        list_string___email_to = [string___email, ]
        # Send mail.
        mail.send_mail(
            subject=string___subject,
            message=string___msg_plain,
            from_email=string___email_from,
            recipient_list=list_string___email_to,
            html_message=string___msg_html,
            fail_silently=True
        )
    except (Exception,):
        pass


@shared_task()
def task___security_login_request_disapprove_send_mail(string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail):
    try:
        string___subject = '::: MOODLE-%s ::: REQUEST USER ::: DISAPPROVE :::' % (settings.LDAP_SERVER_GROUPS_GROUP_CN,)
        string___msg_plain = string___subject + '\n\n' \
                                                'Your request was disapproved. \n\n' \
                                                'User model: %s \n' \
                                                'First name: %s \n' \
                                                'Last name: %s \n' \
                                                'Identifier: %s \n' \
                                                'Email: %s \n' \
                                                'Detail: %s \n' % (string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail,)
        string___msg_html = string___subject + '<br/><br/>' \
                                               'Your request was disapproved. <br/><br/>' \
                                               'User model: %s <br/>' \
                                               'First name: %s <br/>' \
                                               'Last name: %s <br/>' \
                                               'Identifier: %s <br/>' \
                                               'Email: %s <br/>' \
                                               'Detail: %s <br/>' % (string___user_model, string___first_name, string___last_name, string___identifier, string___email, string___detail,)
        string___email_from = settings.EMAIL_USER_NOREPLY
        list_string___email_to = [string___email, ]
        # Send mail.
        mail.send_mail(
            subject=string___subject,
            message=string___msg_plain,
            from_email=string___email_from,
            recipient_list=list_string___email_to,
            html_message=string___msg_html,
            fail_silently=True
        )
    except (Exception,):
        pass
