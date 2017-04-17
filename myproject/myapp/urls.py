# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin
from django.shortcuts import render
from django.conf import settings


urlpatterns = patterns('myproject.myapp.views',
    url(r'^main/$', 'mainPage', name='mainpage'),
    url(r'^register/$', 'UserRegistration'),
    url(r'^login/$', 'LoginRequest'),
    url(r'^logout/$', 'LogoutRequest'),
    url(r'^direct/$', render, {'template': 'direct.html', 'extra_context': {'showDirect':True}}),
    url(r'^profile/$', 'Profile'),
    url(r'^browse/$', 'Browse', name='browse'),
    url(r'^browseAll/$', 'BrowseAll', name='browseAll'),    
    url(r'^applyFX/$', 'ApplyFX', name='applyFX'),
    url(r'^deleteImage/$', 'DeleteImage', name='deleteImage'),
    url(r'^editImage/$', 'EditImage', name='editImage'),
    url(r'^chooseFX/$', 'ChooseFX', name='chooseFX'),

)

urlpatterns += patterns('',
    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(
    r'^static/(?P<path>.*)$',
    'django.views.static.serve',
    {'document_root': settings.STATIC_URL}
    ),
    

)