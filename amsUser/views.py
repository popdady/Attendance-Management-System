# -*- coding: utf-8 -*-
'''
    Attendance Management System. 
    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Ltd.
'''
import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout

from amsUser.models import Attendance, UserTime, Time

def home_page(request):
    '''This is the home page view. When user open the system this 
    view will be displayed. request is a HttpRequest object.
    '''
    return render_to_response('home.html', {'user': request.user})


def logout_page(request):
    '''When user will make logout request then this view will be 
    called. request is a HttpRequest object.
    '''
    logout(request)
    return HttpResponseRedirect('/')


def mark_attendance(request):
    '''This describes how user will mark his/her attendance.
     :param request: request is a HttpRequest object.
    ''' 
    view_table()
    msg = ""
    button_text = get_info(request.user)
    if request.user.is_authenticated:
        if request.method == "POST":
            msg = check_in_out(request.user)
            view_table()
        return render_to_response('mark_attendance.html',{'button_text': button_text,'msg': msg},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login')


def check_in_out(user_id):
    '''This will allows a user to check in or check out for attendance.
    if user is already checke in then he will be checke out and vice versa.
    :param user_id: id of user who want to check in.
    :return : This will return message(whether user is checked in or checked out)
    '''
    msg = "No message for you."
    attendance_obj =  Attendance.objects.get(date=get_time_or_date("date"))
    user_in_usertime = False
    user_already_checkin = False
    if not attendance_obj:
        #if date is not cretated for a day then create it.
        attendance_obj = Attendance.objects.create(date=get_time_or_date("date"),
                                                    record=[UserTime(user_id=user_id, 
                                                    time=[Time(time_in= get_time_or_date("time"))])])
        msg = "%s has checked in"%(user_id.username)
    for usertime in attendance_obj.record:
        if user_id == usertime.user_id:
            #that mean user is created for the date. now check whether he is check in or check out
            user_in_usertime = True
            for time in usertime.time:
                if not time.time_out:
                    #that mean user is already checked in. so checkout him.
                    user_already_checkin = True
                    time.time_out = get_time_or_date("time")
                    attendance_obj.save()
                    msg = "%s has checked out at %s"%(usertime.user_id.username,str(time.time_out))
                    break
            if user_already_checkin == False:
                #that mean user is not checked in.
                usertime.time.append(Time(time_in=get_time_or_date("time")))
                attendance_obj.save()
                msg = "%s has checked in"%(usertime.user_id.username)
            break
    if user_in_usertime == False:
        #if user check in first time in a day then simply add check in entry
        attendance_obj.record.append(UserTime(user_id=user_id,time=[Time(time_in=get_time_or_date(time))]))
        attendance_obj.save()
        msg = "%s has checked in"%(user_id.username)
    return msg


def get_time_or_date(option):
    '''
    :param option:  if option=="time" then it will return time
                    if option=="date"  then it will return date
    :return : It will return time or date, depending upon option 
    '''
    if option == "time":
        time_or_date = datetime.datetime.now()
    elif option == "date":
        time_or_date = datetime.date.today()
    return time_or_date


def view_table():
    '''This prints all the data from attendance table.
    '''
    for row in Attendance.objects.all():
        print "########################"
        print "Record for date:%s"%str(row.date)
        print "########################"
        for usertime in row.record:
            print usertime.user_id.username
            for time in usertime.time:
                print "checked in at:"+str(time.time_in)
                print "checked out at:"+str(time.time_out)
        print "########################"
        print "########################"

def get_info(user_id):
    '''This will return button text.
    '''
    msg = ""
    attendance_obj = Attendance.objects.get(date=get_time_or_date("date"))
    user_in_usertime = False
    user_already_checkin = False
    if not attendance_obj:
        #that mean user is coming first time in this day. welcome him
        msg = "Check In"
    for usertime in attendance_obj.record:
        if user_id == usertime.user_id:
            #user has either check in or check out once in this day
            user_in_usertime = True
            for time in usertime.time:
                if not time.time_out:
                    #that mean user is already checked in.
                    user_already_checkin = True
                    msg = "Check Out"
                    break
            if user_already_checkin == False:
                #that mean user is not checked in.
                msg = "Check In"
            break
    if user_in_usertime == False:
        #if user check in first time in a day
        msg = "Check In"
    return msg
