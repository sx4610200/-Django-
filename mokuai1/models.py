from django.db import models


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=60)
    pwd = models.CharField(max_length=60)
    nicheng = models.CharField(unique=True, max_length=60)
    createtime = models.DateTimeField()
    role = models.IntegerField(default=1)
    msgnum = models.IntegerField(default=0)
    updtime = models.DateTimeField()
    office = models.CharField(max_length=60, blank=True, null=True)
    sicker = models.BigIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'users'


class Messages(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField()
    name = models.CharField(unique=True, max_length=60)
    email = models.CharField(unique=True, max_length=60)
    idperson1 = models.CharField(max_length=60)
    idperson2 = models.CharField(max_length=60)
    createtime = models.DateTimeField()
    role = models.IntegerField(default=2)
    msgnum = models.IntegerField(default=0)
    updtime = models.DateTimeField()
    office = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'messages'


class News(models.Model):
    id = models.BigAutoField(primary_key=True)
    sendid = models.BigIntegerField()
    sendname = models.CharField(max_length=60)
    recid = models.BigIntegerField()
    contents = models.CharField(max_length=60)
    createtime = models.DateTimeField()
    pdtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'news'


class Office(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField(unique=True)
    dename = models.CharField(unique=True,max_length=60)
    officename = models.CharField(max_length=60)
    docid = models.BigIntegerField(blank=True, null=True)
    docname = models.CharField(max_length=60, blank=True, null=True)
    msgnum = models.IntegerField(default=0)
    createtime = models.DateTimeField()
    updtime = models.DateTimeField()
    content = models.CharField(max_length=60, blank=True, null=True)
    money = models.BigIntegerField(blank=True, null=True,default=0)

    class Meta:
        managed = False
        db_table = 'office'

# Create your models here.
