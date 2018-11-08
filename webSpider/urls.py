# -*- coding: utf-8 -*-
"""web spider URL Configuration
"""
from django.conf.urls import url

from . import views

app_name = 'web_spider'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^top250/$', views.top250, name='top250'),
    url(r'^nba/$', views.nba, name='nba'),
    url(r'^zhihu/$', views.zhihu, name='zhihu'),
]
