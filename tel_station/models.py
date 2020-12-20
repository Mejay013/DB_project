# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Atc(models.Model):
    district = models.ForeignKey('District', models.DO_NOTHING)
    num_val = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'atc'

class Block(models.Model):
    atc = models.ForeignKey(Atc, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'block'


class District(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'district'



class SubInfo(models.Model):
    sub = models.ForeignKey('Subscriber', models.DO_NOTHING)
    district = models.ForeignKey(District, models.DO_NOTHING)
    note = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sub_info'


class Subscriber(models.Model):
    second_name = models.CharField(max_length=40)
    check_block = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'subscriber'



class TelNumber(models.Model):
    sub = models.ForeignKey(Subscriber, models.DO_NOTHING)
    block = models.ForeignKey(Block, models.DO_NOTHING)
    debt = models.IntegerField()
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tel_number'


class UniqueBlock(models.Model):
    block = models.ForeignKey(Block, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'unique_block'

