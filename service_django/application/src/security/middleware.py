from . import models, utils
from django.utils import translation


class SecurityMiddleware(object):
    def process_request(self, request):
        instance = None
        if request.session.get('SECURITY_USER_MODEL') and (request.session.get('SECURITY_USER_PK')):
            if request.session.get('SECURITY_USER_MODEL') == utils.SECURITY_USER_MODEL_LOCALUSER:
                instance = models.LOCALUser.objects.instance___by_pk(pk=request.session.get('SECURITY_USER_PK'))
            if request.session.get('SECURITY_USER_MODEL') == utils.SECURITY_USER_MODEL_LDAPUSER:
                instance = models.LDAPUser.objects.instance___by_pk(pk=request.session.get('SECURITY_USER_PK'))
            if instance is not None:
                translation.activate(instance.locale)
                request.session[translation.LANGUAGE_SESSION_KEY] = instance.locale
        request.SECURITY_USER = instance
        #
        list_string___url = (
            '/home/',
            '/home/module/home/website/',
            '/home/module/documentation/documentation/',
            '/screening/',
            '/screening/module/screening/module01/',
            '/screening/module/screening/module02/',
            '/screening/module/screening/module03/',
            '/administration/',
            '/administration/module/security/requestedlocaluser/',
            '/administration/module/security/localuser/',
            '/administration/module/security/requestedldapuser/',
            '/administration/module/security/ldapuser/',
            '/administration/module/security/importedldapuser/',
            '/administration/module/security/group/',
            '/administration/module/security/permission/',
            '/administration/module/documentation/document/',
        )
        if request.path in list_string___url:
            if request.path == '/home/':
                request.session['SECURITY_USER_URL_CURRENT'] = '/home/module/home/website/'
            else:
                request.session['SECURITY_USER_URL_CURRENT'] = request.path

    def process_response(self, request, response):
        return response
