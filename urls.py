# -*- coding: utf-8 -*-
'''
    Attendance Management System Model.
    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Ltd.
'''
from django.conf.urls.defaults import patterns, include,url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    (r'^$', 'amsUser.views.home_page'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'amsUser.views.logout_page'),
    (r'^mark_attendance/$', 'amsUser.views.mark_attendance'),
    url(r'^admin/',include(admin.site.urls)),
)
