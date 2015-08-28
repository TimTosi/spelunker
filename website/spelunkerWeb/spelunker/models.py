# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Addresses(models.Model):
    id = models.CharField(primary_key=True, max_length=34)
    cluster = models.ForeignKey('Clusters', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class Blocks(models.Model):
    id = models.BigIntegerField(primary_key=True)
    magic_id = models.CharField(max_length=8)
    length = models.IntegerField()
    version = models.IntegerField()
    previous_block_hash = models.CharField(max_length=64)
    merkle_root = models.CharField(max_length=64)
    target_difficulty = models.IntegerField()
    nonce = models.BigIntegerField()
    block_hash = models.CharField(max_length=64)
    file_name = models.CharField(max_length=50)
    real_size = models.BigIntegerField()
    block_timestamp = models.DateTimeField()
    real_number = models.BigIntegerField(blank=True, null=True)
    orphan = models.NullBooleanField()
    next_block_hash = models.CharField(max_length=64, blank=True)

    class Meta:
        managed = True
        db_table = 'blocks'


class Clusters(models.Model):
    id = models.BigIntegerField(primary_key=True)
    currency_amount = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clusters'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Inputs(models.Model):
    id = models.BigIntegerField(primary_key=True)
    transaction = models.ForeignKey('Transactions', blank=True, null=True)
    transaction_hash = models.CharField(max_length=64)
    transaction_index = models.BigIntegerField()
    coinbase = models.BooleanField()
    sequence_number = models.BigIntegerField()
    script = models.TextField()
    orphan = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'inputs'


class Ledger(models.Model):
    id = models.BigIntegerField(primary_key=True)
    address = models.CharField(max_length=34)
    operation = models.BooleanField()
    value = models.BigIntegerField()
    block_timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ledger'


class Outputs(models.Model):
    id = models.BigIntegerField(primary_key=True)
    transaction = models.ForeignKey('Transactions', blank=True, null=True)
    value = models.BigIntegerField()
    address = models.CharField(max_length=34)
    script = models.TextField()
    index = models.BigIntegerField()
    orphan = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'outputs'


class Transactions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    block = models.ForeignKey(Blocks, blank=True, null=True)
    version = models.BigIntegerField()
    input_count = models.BigIntegerField()
    output_count = models.BigIntegerField()
    locktime = models.BigIntegerField()
    transaction_hash = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'transactions'
