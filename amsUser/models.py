# -*- coding: utf-8 -*-
'''
    Attendance Management System Model.

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Ltd.
'''
from djangotoolbox.fields import EmbeddedModelField
from djangotoolbox.fields import ListField
from django.db import models
from django.contrib.auth.models import User


class Time(models.Model):
    '''This model will store the time_in(time when user check in) and
    time_out(time when user check out).
    '''
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()


class UserTime(models.Model):
    '''This model will store time_in, time_out combination for
    a user.
    '''
    user_id = models.ForeignKey(User)
    time = ListField(EmbeddedModelField('Time'))


class Attendance(models.Model):
    '''This model will store the user's time_in, time_out combination for a
    particular date.
    '''
    date = models.DateField(primary_key=True)
    record = ListField(EmbeddedModelField('UserTime'))


class Holiday(models.Model):
    '''This model will store holidays with their purpose.
    '''
    from_date = models.DateField()
    to_date = models.DateField()
    purpose = models.CharField(max_length=200)
