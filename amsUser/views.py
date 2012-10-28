# -*- coding: utf-8 -*-
'''
    Attendance Management System. 
    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Ltd.
'''
import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import logout

from amsUser.models import Attendance, UserTime, Time, Holiday
from amsUser.forms import AttendanceDetailForm

def home_page(request):
    '''This is the home page view for attendance management system.
    :param request: is a HttpRequest object.
    :return:if user is logged in then display home page.
            if user is not logged in then redirect to login page
    '''
    if request.user.username:
        return render_to_response('home.html', {'user': request.user})
    else:
        return HttpResponseRedirect('/login')


def logout_page(request):
    '''When user will make logout request then this view will be called.
    :param request: is a HttpRequest object.
    :return: redirect to login page.
    '''
    logout(request)
    return HttpResponseRedirect('/login')


def mark_attendance(request):
    '''When user want to mark attendance, this view will be called.
    :param request: request is a HttpRequest object.
    :return: if user is not logged in then redirect to login page.
            if user do check in or check out then do it.
    '''
    if request.user.username:
        if request.method == "POST":
            if check_in_out(request.user):
                msg = get_info(request.user)
                return render_to_response('mark_attendance.html',
                                    {'msg': msg[0], 'button_text': msg[1]},
                                    context_instance=RequestContext(request))
            else:
                return HttpResponse("There is an error, please try again!")
        else:
            msg = get_info(request.user)
            return render_to_response('mark_attendance.html',
                                    {'msg': msg[0], 'button_text': msg[1]},
                                    context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login')


def attendance_detail(request):
    '''When user want to know attendance details, this view will be called.
    :param request: is a HttpRequest object.
    :return: According to user choice, it will return his attendance detail.
    '''
    if request.user.username:
        if request.method == 'POST':
            form = AttendanceDetailForm(request.POST)
            if form.is_valid():
                build_date = datetime.datetime(year=
                                        int(request.POST['date_year']),
                                        month=
                                        int(request.POST['date_month']),
                                        day=
                                        int(request.POST['date_day']))
                temp = get_checkinout_for_date(build_date, request.user)
                return render_to_response('attendance_detail.html',
                                    {'form': form,
                                    'usertime': temp,
                                    'totaltime': get_total_session_time(temp)},
                                    context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect('.')
        else:
            form = AttendanceDetailForm()
            temp = get_checkinout_for_date(get_date_time, request.user)
            return render_to_response('attendance_detail.html',
                                    {'form': form,
                                    'usertime': temp,
                                    'totaltime': get_total_session_time(temp)},
                                    context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login')


def get_checkinout_for_date(date_time, user_id):
    '''This will give users all check in and check out of a given date.
    :param date_time: datetime of which user want to know details.
    :param user_id: user id
    :return: time list if their is any entry otherwise False.
    '''
    attendance_obj_collection =  Attendance.objects.filter(date=date_time)
    if not attendance_obj_collection:
        return False
    else:
        attendance_obj = attendance_obj_collection[0]
    for usertime in attendance_obj.record:
        if user_id == usertime.user_id:
            return usertime.time
    return False


def get_total_session_time(usertime):
    '''This will give total time spent in a date.
    :param usertime: time list of check in and check out
    :return: return total spent time if any, otherwise false.
    '''
    if usertime:
        total = datetime.timedelta()
        for time in usertime:
            if time.time_out is None:
                continue
            else:
                total += time.time_out-time.time_in
        return total
    else:
        return False


def check_in_out(user_id):
    '''This will allows a user to check in or check out for attendance.
    if user is already check in then he will be check out and vice versa.
    :param user_id: id of user who want to check in.
    :return: return True if sucess else False.
    '''
    attendance_obj_collection =  Attendance.objects.filter(date=
                                                    get_date_time())
    user_in_usertime = False
    if not attendance_obj_collection:
        #if date is not cretated for a day then create it.
        attendance_obj = Attendance.objects.create(
                                                date=get_date_time(),
                                                record=
                                                [UserTime(user_id=user_id,
                                                time=[Time(time_in=
                                                get_date_time())])])
        return True
    else:
        attendance_obj = attendance_obj_collection[0]
    for usertime in attendance_obj.record:
        if user_id == usertime.user_id:
            #that mean user is created for the date. now check whether he is 
            #check in or check out
            user_in_usertime = True
            if usertime.time[-1].time_out is None:
                #that mean user is already checked in. so checkout him.
                usertime.time[-1].time_out = get_date_time()
                attendance_obj.save()
                return True
            else:
                #that mean user is not checked in.
                usertime.time.append(Time(time_in=get_date_time()))
                attendance_obj.save()
                return True
    if user_in_usertime == False:
        #if user check in first time in a day and date entry is already
        #created, then simply add check in entry
        attendance_obj.record.append(UserTime(user_id=user_id,
                                                time=[Time(time_in=
                                                get_date_time())]))
        attendance_obj.save()
        return True
    return False


def get_date_time():
    '''This will give datetime.
    :return: datetime.datetime object
    '''
    return datetime.datetime.now()


def view_table():
    '''This prints all the data from attendance table.
    this function is for test purpose.
    '''
    for row in Attendance.objects.all():
        print "########################"
        print "Record for date:%s" % str(row.date)
        print "########################"
        for usertime in row.record:
            print usertime.user_id.username
            for time in usertime.time:
                print "checked in at:" + str(time.time_in)
                print "checked out at:" + str(time.time_out)
        print "########################"
        print "########################"


def get_info(user_id):
    '''This will fetch information of check in and check out.
    :return: a msg dictionary. In which '0' key msg to user and '1' key
            the button text.
    '''
    msg = {}
    attendance_obj_collection = Attendance.objects.filter(date=get_date_time())
    user_in_usertime = False
    if not attendance_obj_collection:
        #that mean user is coming first time in this day. welcome him
        msg[0] = "Welcome " + user_id.username
        msg[1] = "Check In"
        return msg
    else:
        #that mean someone has already mark his attendance in this date
        attendance_obj = attendance_obj_collection[0]
    for usertime in attendance_obj.record:
        if user_id == usertime.user_id:
            #user has either check in or check out once in this day
            user_in_usertime = True
            if usertime.time[-1].time_out is None:
                #that mean user is already checked in.
                msg[0] = "You have last Checked in at %s" % (
                                            usertime.time[-1].time_in.time())
                msg[1] = "Check Out"
                return msg
            else:
                #that mean user is not checked in.
                msg[0] = "You have last Checked out at %s" % (
                                            usertime.time[-1].time_out.time())
                msg[1] = "Check In"
                return msg
    if user_in_usertime == False:
        #if user check in first time in a day
        msg[0] = "Welcome " + user_id.username
        msg[1] = "Check In"
        return msg
    return msg


def holiday_list(request):
    '''when user want to see holiday list, this view will be called.
    '''
    if request.user.username:
        if request.method == 'POST':
            form = AttendanceDetailForm(request.POST)
            if form.is_valid():
                build_date = datetime.datetime(year=
                                        int(request.POST['date_year']),
                                        month=
                                        int(request.POST['date_month']),
                                        day=
                                        int(request.POST['date_day']))
                temp = get_holidays(build_date)
                return render_to_response('holiday_list.html',
                                    {'form': form,
                                    'holidays': temp,
                                    'totalholidays': len(temp)},
                                    context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect('.')
        else:
            form = AttendanceDetailForm()
            temp = get_holidays(get_date_time())
            return render_to_response('holiday_list.html',
                                    {'form': form,
                                    'holidays': temp,
                                    'totalholidays': len(temp)},
                                    context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login')


def get_holidays(date_time):
    '''This function will give all the holiday list of that month/year.
    :param date_time
    '''
    holiday_dates = {}
    holiday_obj_collection = Holiday.objects.all()
    if holiday_obj_collection:
        for holiday in holiday_obj_collection:
            delta = holiday.to_date - holiday.from_date
            for i in range(delta.days + 1):
                temp = holiday.from_date + datetime.timedelta(days=i)
                if (temp.month == date_time.month) and (
                                temp.year == date_time.year):
                    holiday_dates[temp] = holiday.purpose
        return holiday_dates
    else:
        return False
