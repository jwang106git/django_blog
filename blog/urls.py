# -*- coding: utf-8 -*-
"""blog app URL Configuration

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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views
from django.views.decorators.cache import cache_page

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.Detail.as_view(), name='detail'),
    url(r'view_post/(?P<post_id>[0-9]+)/$', views.PostDetailView.as_view(), name='detailbyid'),
    # 测试一下使用detail view
    url(r'^get_time/$', views.get_time, name='get_time'),
    url(r'^submit_comment/$', views.submit_comment, name='submit_commit'),
    url(r'^search/$', views.Search.as_view(), name='search'),
    url(r'^404$', views.page_not_found, name='404'),
    url(r'^500$', views.page_error),
]
