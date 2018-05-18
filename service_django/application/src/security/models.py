# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils import timezone
from passlib.handlers import django as passlib_django
from passlib.hash import ldap_salted_sha1 as passlib_ldap_salted_sha1

FOLDER_LOCALUSER_PATH = 'application/security/localuser'
FOLDER_LDAPUSER_PATH = 'application/security/ldapuser'


class RequestedLOCALUserManager(models.Manager):
    def instances(self, request):
        instances = self.all()
        return instances

    def instance(self, request, pk):
        try:
            instance = self.get(pk=pk)
        except RequestedLOCALUser.DoesNotExist:
            return None
        return instance

    def instance___by_pk(self, pk):
        try:
            instance = self.get(pk=pk)
        except RequestedLOCALUser.DoesNotExist:
            return None
        return instance


class RequestedLOCALUser(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    first_name = models.CharField(
        default='',
        max_length=100,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        default='',
        max_length=100,
        null=True,
        blank=True,
    )
    identifier = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
    )
    email = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
    )
    password = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
    )
    detail = models.TextField(
        default='',
        max_length=1024,
        null=True,
        blank=True,
    )
    objects = RequestedLOCALUserManager()

    class Meta:
        db_table = 'application_security_requestedlocaluser'
        ordering = ['id', ]

    def __str__(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name,)
        if self.first_name:
            return '%s' % (self.first_name,)
        return self.identifier

    def save(self, *args, **kwargs):
        if self.password == '':
            self.void___encrypt_password(password='')
        return super(RequestedLOCALUser, self).save(*args, **kwargs)

    def void___encrypt_password(self, password):
        self.password = passlib_django.django_pbkdf2_sha256.encrypt(password)


class LOCALUserManager(models.Manager):
    def instances(self, request):
        if isinstance(request.SECURITY_USER, LOCALUser):
            instances = self.all().filter(is_superuser=False).exclude(pk=request.SECURITY_USER.pk)
        else:
            instances = self.all().filter(is_superuser=False)
        instances = instances.order_by('first_name', 'identifier')
        return instances

    def instance(self, request, pk):
        try:
            instance = self.get(pk=pk)
            if instance.is_superuser or (isinstance(request.SECURITY_USER, LOCALUser) and request.SECURITY_USER.pk == instance.pk):
                return None
        except LOCALUser.DoesNotExist:
            return None
        return instance

    def instance___by_pk(self, pk):
        try:
            instance = self.get(pk=pk)
        except LOCALUser.DoesNotExist:
            return None
        return instance

    def instance___by_identifier(self, identifier):
        try:
            instance = self.get(identifier=identifier)
        except LOCALUser.DoesNotExist:
            return None
        return instance

    def instance___by_email(self, email):
        try:
            instance = self.get(email=email)
        except LOCALUser.DoesNotExist:
            return None
        return instance


class LOCALUser(models.Model):
    def avatar_upload_to(instance, filename):
        return '%s/%s/%s.jpg' % (FOLDER_LOCALUSER_PATH, instance.identifier, instance.identifier,)

    id = models.AutoField(
        primary_key=True,
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=avatar_upload_to,
    )
    first_name = models.CharField(
        default='',
        max_length=100,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        default='',
        max_length=100,
        null=True,
        blank=True,
    )
    identifier = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
    )
    email = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
    )
    password = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
    )
    detail = models.TextField(
        default='',
        max_length=1024,
        null=True,
        blank=True,
    )
    groups = models.ManyToManyField(
        'Group',
        related_name='localuser_groups_set',
        through='LOCALUserGroup',
        through_fields=('localuser', 'group')
    )
    permissions = models.ManyToManyField(
        'Permission',
        related_name='localuser_permissions_set',
        through='LOCALUserPermission',
        through_fields=('localuser', 'permission')
    )
    locale = models.CharField(
        default='',
        max_length=10,
        null=True,
        blank=True,
    )
    is_superuser = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    objects = LOCALUserManager()

    class Meta:
        db_table = 'application_security_localuser'
        ordering = ['id', ]

    def __str__(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name,)
        if self.first_name:
            return '%s' % (self.first_name,)
        return self.identifier

    def save(self, *args, **kwargs):
        if self.password == '':
            self.void___encrypt_password(password='')
        return super(LOCALUser, self).save(*args, **kwargs)

    def string___folder_path(self):
        return '%s/%s/%s' % (settings.MEDIA_ROOT, FOLDER_LOCALUSER_PATH, self.identifier,)

    def void___encrypt_password(self, password):
        self.password = passlib_django.django_pbkdf2_sha256.encrypt(password)

    def boolean___verify_password(self, password):
        return passlib_django.django_pbkdf2_sha256.verify(password, self.password)

    def boolean___has_permission(self, set_identifier___to_verify=set()):
        if self.is_superuser:
            return True
        if set_identifier___to_verify and self.groups and self.permissions:
            set_identifier = set()
            # groups
            instances___group = self.groups.filter(is_active=True)
            for instance___group in instances___group:
                instances___permission = instance___group.permissions.filter(is_active=True)
                for instance___permission in instances___permission:
                    set_identifier.add(instance___permission.identifier)
            # permissions
            instances___permission = self.permissions.all().filter(is_active=True)
            for instance___permission in instances___permission:
                set_identifier.add(instance___permission.identifier)
            #
            for identifier in set_identifier___to_verify:
                if identifier not in set_identifier:
                    return False
            return True
        else:
            return False


class LOCALUserForgotCredentialManager(models.Manager):
    def instances(self, request):
        instances = self.all()
        return instances

    def instance(self, request, pk):
        try:
            instance = self.get(pk=pk)
        except LOCALUserForgotCredential.DoesNotExist:
            return None
        return instance

    def instance___by_pk(self, pk):
        try:
            instance = self.get(pk=pk)
        except LOCALUserForgotCredential.DoesNotExist:
            return None
        return instance


class LOCALUserForgotCredential(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    email = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
    )
    code = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
    )
    password = models.CharField(
        default='',
        max_length=1024,
        null=True,
        blank=True,
    )
    objects = LOCALUserForgotCredentialManager()
    #
    INT___MAXIMUM_TIME_OF_EXISTENCE = 15

    class Meta:
        db_table = 'application_security_localuserforgotcredential'
        ordering = ['id', ]

    def __str__(self):
        return '%s-%s' % (self.email, self.code,)

    def void___encrypt_password(self, password):
        self.password = passlib_django.django_pbkdf2_sha256.encrypt(password)

    def int___time_of_existence(self):  # in minutes
        time___created = timezone.datetime.time(self.created)
        time___now = timezone.now()
        hour___created = time___created.hour
        hour___now = time___now.hour
        minute___created = time___created.minute
        minute___now = time___now.minute
        #
        if hour___created == hour___now:
            minutes = minute___now - minute___created
        else:
            minutes = 60 - minute___created + minute___now
        return minutes


class RequestedLDAPUserManager(models.Manager):
    def instances(self, request):
        instances = self.all()
        return instances

    def instance(self, request, pk):
        try:
            instance = self.get(pk=pk)
        except RequestedLDAPUser.DoesNotExist:
            return None
        return instance

    def instance___by_pk(self, pk):
        try:
            instance = self.get(pk=pk)
        except RequestedLDAPUser.DoesNotExist:
            return None
        return instance


class RequestedLDAPUser(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    first_name = models.CharField(
        default='',
        max_length=100,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        default='',
        max_length=100,
        null=True,
        blank=True,
    )
    identifier = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
    )
    email = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
    )
    password = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
    )
    detail = models.TextField(
        default='',
        max_length=1024,
        null=True,
        blank=True,
    )
    objects = RequestedLDAPUserManager()

    class Meta:
        db_table = 'application_security_requestedldapuser'
        ordering = ['id', ]

    def __str__(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name,)
        if self.first_name:
            return '%s' % (self.first_name,)
        return self.identifier

    def save(self, *args, **kwargs):
        if self.password == '':
            self.void___encrypt_password(password='')
        return super(RequestedLDAPUser, self).save(*args, **kwargs)

    def void___encrypt_password(self, password):
        self.password = passlib_ldap_salted_sha1.encrypt(password)


class LDAPUserManager(models.Manager):
    def instances(self, request):
        if isinstance(request.SECURITY_USER, LDAPUser):
            instances = self.all().filter(is_superuser=False).exclude(pk=request.SECURITY_USER.pk)
        else:
            instances = self.all().filter(is_superuser=False)
        instances = instances.order_by('first_name', 'identifier')
        return instances

    def instance(self, request, pk):
        try:
            instance = self.get(pk=pk)
            if instance.is_superuser or (isinstance(request.SECURITY_USER, LDAPUser) and request.SECURITY_USER.pk == instance.pk):
                return None
        except LDAPUser.DoesNotExist:
            return None
        return instance

    def instance___by_pk(self, pk):
        try:
            instance = self.get(pk=pk)
        except LDAPUser.DoesNotExist:
            return None
        return instance

    def instance___by_identifier(self, identifier):
        try:
            instance = self.get(identifier=identifier)
        except LDAPUser.DoesNotExist:
            return None
        return instance

    def instance___by_email(self, email):
        try:
            instance = self.get(email=email)
        except LDAPUser.DoesNotExist:
            return None
        return instance


class LDAPUser(models.Model):
    def avatar_upload_to(instance, filename):
        return '%s/%s/%s.jpg' % (FOLDER_LDAPUSER_PATH, instance.identifier, instance.identifier,)

    id = models.AutoField(
        primary_key=True,
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=avatar_upload_to,
    )
    first_name = models.CharField(
        default='',
        max_length=100,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        default='',
        max_length=100,
        null=True,
        blank=True,
    )
    identifier = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
    )
    email = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
    )
    password = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
    )
    detail = models.TextField(
        default='',
        max_length=1024,
        null=True,
        blank=True,
    )
    groups = models.ManyToManyField(
        'Group',
        related_name='ldapuser_groups_set',
        through='LDAPUserGroup',
        through_fields=('ldapuser', 'group')
    )
    permissions = models.ManyToManyField(
        'Permission',
        related_name='ldapuser_permissions_set',
        through='LDAPUserPermission',
        through_fields=('ldapuser', 'permission')
    )
    locale = models.CharField(
        default='',
        max_length=10,
        null=True,
        blank=True,
    )
    is_superuser = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    objects = LDAPUserManager()

    class Meta:
        db_table = 'application_security_ldapuser'
        ordering = ['id', ]

    def __str__(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name,)
        if self.first_name:
            return '%s' % (self.first_name,)
        return '%s_%s' % (settings.LDAP_SERVER_GROUPS_GROUP_CN.lower(), self.identifier,)

    def save(self, *args, **kwargs):
        if self.password == '':
            self.void___encrypt_password(password='')
        return super(LDAPUser, self).save(*args, **kwargs)

    def string___folder_path(self):
        return '%s/%s/%s' % (settings.MEDIA_ROOT, FOLDER_LDAPUSER_PATH, self.identifier,)

    def void___encrypt_password(self, password):
        self.password = passlib_ldap_salted_sha1.encrypt(password)

    def boolean___verify_password(self, password):
        return passlib_ldap_salted_sha1.verify(password, self.password)

    def boolean___has_permission(self, set_identifier___to_verify=set()):
        if self.is_superuser:
            return True
        if set_identifier___to_verify and self.groups and self.permissions:
            set_identifier = set()
            # groups
            instances___group = self.groups.filter(is_active=True)
            for instance___group in instances___group:
                instances___permission = instance___group.permissions.filter(is_active=True)
                for instance___permission in instances___permission:
                    set_identifier.add(instance___permission.identifier)
            # permissions
            instances___permission = self.permissions.all().filter(is_active=True)
            for instance___permission in instances___permission:
                set_identifier.add(instance___permission.identifier)
            #
            for identifier in set_identifier___to_verify:
                if identifier not in set_identifier:
                    return False
            return True
        else:
            return False


class LDAPUserForgotCredentialManager(models.Manager):
    def instances(self, request):
        instances = self.all()
        return instances

    def instance(self, request, pk):
        try:
            instance = self.get(pk=pk)
        except LDAPUserForgotCredential.DoesNotExist:
            return None
        return instance

    def instance___by_pk(self, pk):
        try:
            instance = self.get(pk=pk)
        except LDAPUserForgotCredential.DoesNotExist:
            return None
        return instance


class LDAPUserForgotCredential(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    email = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
    )
    code = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
    )
    password = models.CharField(
        default='',
        max_length=1024,
        null=True,
        blank=True,
    )
    objects = LDAPUserForgotCredentialManager()
    #
    INT___MAXIMUM_TIME_OF_EXISTENCE = 15

    class Meta:
        db_table = 'application_security_ldapuserforgotcredential'
        ordering = ['id', ]

    def __str__(self):
        return '%s-%s' % (self.email, self.code,)

    def void___encrypt_password(self, password):
        self.password = passlib_ldap_salted_sha1.encrypt(password)

    def int___time_of_existence(self):  # in minutes
        time___created = timezone.datetime.time(self.created)
        time___now = timezone.now()
        hour___created = time___created.hour
        hour___now = time___now.hour
        minute___created = time___created.minute
        minute___now = time___now.minute
        #
        if hour___created == hour___now:
            minutes = minute___now - minute___created
        else:
            minutes = 60 - minute___created + minute___now
        return minutes


class GroupManager(models.Manager):
    def instances(self, request):
        instances = self.all()
        instances___position_not_equal_0 = instances.exclude(position__lte=0)
        instances___position_equal_0 = instances.exclude(position__gt=0)
        int___position = 1
        if instances___position_not_equal_0.count() > 0:
            for instance in instances___position_not_equal_0:
                instance.position = int___position
                instance.save()
                int___position += 1
        if instances___position_equal_0.count() > 0:
            for instance in instances___position_equal_0:
                instance.position = int___position
                instance.save()
                int___position += 1
        instances = self.all()
        return instances

    def instance(self, request, pk):
        try:
            instance = self.get(pk=pk)
        except Group.DoesNotExist:
            return None
        return instance

    def instance___by_pk(self, pk):
        try:
            instance = self.get(pk=pk)
        except Group.DoesNotExist:
            return None
        return instance


class Group(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    name = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
    )
    permissions = models.ManyToManyField(
        'Permission',
        related_name='group_permissions_set',
        through='GroupPermission',
        through_fields=('group', 'permission')
    )
    parent = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )
    position = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )
    objects = GroupManager()

    class Meta:
        db_table = 'application_security_group'
        ordering = ['position', 'id', ]

    def __str__(self):
        return self.name


class PermissionManager(models.Manager):
    def instances(self, request):
        instances = self.all()
        return instances

    def instance(self, request, pk):
        try:
            instance = self.get(pk=pk)
        except Permission.DoesNotExist:
            return None
        return instance

    def instance___by_pk(self, pk):
        try:
            instance = self.get(pk=pk)
        except Permission.DoesNotExist:
            return None
        return instance


class Permission(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    name = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
    )
    identifier = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
    )
    objects = PermissionManager()

    class Meta:
        db_table = 'application_security_permission'
        ordering = ['id', ]

    def __str__(self):
        return self.name


class LOCALUserGroupManager(models.Manager):
    pass


class LOCALUserGroup(models.Model):
    localuser = models.ForeignKey(
        'LOCALUser',
    )
    group = models.ForeignKey(
        'Group',
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    objects = LOCALUserGroupManager()

    class Meta:
        db_table = 'application_security_localusergroup'
        ordering = ['localuser', 'group']

    def __str__(self):
        return '<%s> <%s>' % (self.localuser, self.group,)


class LOCALUserPermissionManager(models.Manager):
    pass


class LOCALUserPermission(models.Model):
    localuser = models.ForeignKey(
        'LOCALUser',
    )
    permission = models.ForeignKey(
        'Permission',
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    objects = LOCALUserPermissionManager()

    class Meta:
        db_table = 'application_security_localuserpermission'
        ordering = ['localuser', 'permission']

    def __str__(self):
        return '<%s> <%s>' % (self.localuser, self.permission,)


class LDAPUserGroupManager(models.Manager):
    pass


class LDAPUserGroup(models.Model):
    ldapuser = models.ForeignKey(
        'LDAPUser',
    )
    group = models.ForeignKey(
        'Group',
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    objects = LDAPUserGroupManager()

    class Meta:
        db_table = 'application_security_ldapusergroup'
        ordering = ['ldapuser', 'group']

    def __str__(self):
        return '<%s> <%s>' % (self.ldapuser, self.group,)


class LDAPUserPermissionManager(models.Manager):
    pass


class LDAPUserPermission(models.Model):
    ldapuser = models.ForeignKey(
        'LDAPUser',
    )
    permission = models.ForeignKey(
        'Permission',
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    objects = LDAPUserPermissionManager()

    class Meta:
        db_table = 'application_security_ldapuserpermission'
        ordering = ['ldapuser', 'permission']

    def __str__(self):
        return '<%s> <%s>' % (self.ldapuser, self.permission,)


class GroupPermissionManager(models.Manager):
    pass


class GroupPermission(models.Model):
    group = models.ForeignKey(
        'Group',
    )
    permission = models.ForeignKey(
        'Permission',
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
    )
    objects = GroupPermissionManager()

    class Meta:
        db_table = 'application_security_grouppermission'
        ordering = ['group', 'permission']

    def __str__(self):
        return '<%s> <%s>' % (self.group, self.permission,)
