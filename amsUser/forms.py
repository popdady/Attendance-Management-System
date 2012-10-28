# -*- coding: utf-8 -*-
"""
    forms for userAms
    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from django import forms
from django.forms.fields import DateField, CharField
from django.forms.extras.widgets import SelectDateWidget

YEAR_CHOICE = ('2010', '2011', '2012')

class AttendanceDetailForm(forms.Form):
    '''This is a form with having datefield. Initial value for datefield will
    be current date.
    '''
    date = DateField(widget=SelectDateWidget(years=YEAR_CHOICE),
                    initial=datetime.now())


class AddHolidayForm(forms.Form):
    '''A form having from_date, to_date and purpose field. This will be used
    to ass holiday
    '''
    from_date = DateField(widget=SelectDateWidget(years=YEAR_CHOICE),
                    initial=datetime.now())
    to_date = DateField(widget=SelectDateWidget(years=YEAR_CHOICE),
                    initial=datetime.now())
    purpose = CharField(max_length=200, required=True,
                widget=forms.Textarea, help_text="Maximum 200 character")
