# -*- coding: utf-8 -*-
"""
    Admin views in Attendance Management System.
    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User

from amsUser.views import get_info, check_in_out, get_holidays, get_date_time
from amsUser.forms import AttendanceDetailForm, AddHolidayForm
from amsUser.models import Holiday

def ams_admin(request):
    '''This view will be called when admin view of ams will be called.
    :param request: is a HttpRequest object.
    '''
    if request.user.username:
        if request.user.is_superuser:
            return render_to_response('ams_admin.html', {'user': request.user})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login')


def mark_all_attendance(request):
    '''This view mark attendance of all user available.
    '''
    if request.user.username:
        if request.user.is_superuser:
            alluser = {}
            if request.method == 'POST':
                for user in get_all_user():
                    if user.username in request.POST.keys():
                        if not check_in_out(user):
                            return HttpResponse(
                                     "There is an error, please try again!")
                    alluser[user] = get_info(user)[1]
                return render_to_response('mark_all_attendance.html', {
                                    'alluser': alluser},
                                    context_instance=RequestContext(request))
            else:
                for user in get_all_user():
                    alluser[user] = get_info(user)[1]
                return render_to_response('mark_all_attendance.html',
                                    {'alluser': alluser},
                                    context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login')


def edit_view_holidays(request):
    '''This function will allow to view and edit holiday list
    '''
    if request.user.username:
        if request.user.is_superuser:
            if request.method == 'POST':
                if 'add' in request.POST.keys():
                    addform = AddHolidayForm(request.POST)
                    if addform.is_valid():
                        build_date_from = datetime.datetime(year=
                                        int(request.POST['from_date_year']),
                                        month=
                                        int(request.POST['from_date_month']),
                                        day=
                                        int(request.POST['from_date_day']))
                        build_date_to = datetime.datetime(year=
                                        int(request.POST['to_date_year']),
                                        month=
                                        int(request.POST['to_date_month']),
                                        day=
                                        int(request.POST['to_date_day']))
                        add_holiday(build_date_from, build_date_to,
                                     request.POST['purpose'])
                        return HttpResponseRedirect('.')
                    else:
                        return HttpResponseRedirect('.')
                else:
                    form = AttendanceDetailForm(request.POST)
                    addform = AddHolidayForm()
                    if form.is_valid():
                        build_date = datetime.datetime(year=
                                        int(request.POST['date_year']),
                                        month=
                                        int(request.POST['date_month']),
                                        day=
                                        int(request.POST['date_day']))
                        temp = get_holidays(build_date)
                        return render_to_response('edit_view_holidays.html',
                                    {'form': form,
                                    'holidays': temp,
                                    'addform': addform,
                                    'totalholidays': len(temp)},
                                    context_instance=RequestContext(request))
                    else:
                        return HttpResponseRedirect('.')
            else:
                form = AttendanceDetailForm()
                addform = AddHolidayForm()
                temp = get_holidays(get_date_time())
                return render_to_response('edit_view_holidays.html',
                                    {'form': form,
                                    'addform': addform,
                                    'holidays': temp,
                                    'totalholidays': len(temp)},
                                    context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login')


def get_all_user():
    '''This will fetch all users.
    :return: list of user objects.
    '''
    return User.objects.all()


def add_holiday(from_date, to_date, purpose):
    '''This will add holiday.
    :param from_date: from date the holiday start.
    :param to_date: till date you holidy.
    '''
    from_date = datetime.datetime.date(from_date)
    to_date = datetime.datetime.date(to_date)
    Holiday.objects.create(from_date=from_date, to_date=to_date,
                            purpose=purpose)
