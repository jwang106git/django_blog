# -*- coding: utf-8 -*-
"""auth app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('auth/', include('auth.urls'))
"""
from django.conf.urls import url

from . import views

app_name = 'auth'
urlpatterns = [
    url(r'^register$', views.Register.as_view(), name='register'),
    url(r'^login_ajax_check$', views.login_ajax_check, name='login_ajax_check'),
    url(r'^sign_up_ajax_check$', views.sign_up_ajax_check, name='sign_up_ajax_check'),
    url(r'^login$', views.AuthLogin.as_view(), name='login'),
    url(r'^logout$', views.AuthLogout.as_view(), name='logout'),
    url(r'^verify_code/([0-9]+)$', views.verify_code, name='verify_code'),
]
