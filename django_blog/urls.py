"""django_blog URL Configuration

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
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

handler404 = 'blog.views.page_not_found_view'
handler500 = 'blog.views.server_error_view'

# ... the rest of your URLconf goes here ...

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('auth.urls')),
    url(r'^web-spider/', include('webSpider.urls')),
    url(r'', include('blog.urls')),
]
urlpatterns += staticfiles_urlpatterns()