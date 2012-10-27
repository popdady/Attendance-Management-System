# -*- coding: utf-8 -*-
"""
    forms for userAms

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from django import forms
from django.forms.fields import DateField
from django.forms.extras.widgets import SelectDateWidget

YEAR_CHOICE = ('2010', '2011', '2012')

class AttendanceDetailForm(forms.Form):
    '''This is a form with having datefield. Initial value for datefield will
    be current date.
    '''
    date = DateField(widget=SelectDateWidget(years=YEAR_CHOICE),
                    initial=datetime.now())
