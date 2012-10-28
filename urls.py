# -*- coding: utf-8 -*-
'''
    Attendance Management System Model.
    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Ltd.
'''
import os.path

from django.conf.urls.defaults import patterns, include,url
from django.contrib import admin

site_media = os.path.join(os.path.dirname(__file__), 'site_media')
admin.autodiscover()
urlpatterns = patterns('',
    (r'^$', 'amsUser.views.home_page'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'amsUser.views.logout_page'),
    (r'^mark_attendance/$', 'amsUser.views.mark_attendance'),
    (r'^attendance_detail/$', 'amsUser.views.attendance_detail'),
    (r'^holiday_list/$', 'amsUser.views.holiday_list'),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': site_media }),
    url(r'^admin/',include(admin.site.urls)),
)
