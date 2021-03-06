# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin

from djanban.apps.index import views as index_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as serve_static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    url(r'^$', index_views.index, name="index"),

    url(r'^admin/', admin.site.urls),

    url(r'^base/', include('djanban.apps.base.urls', namespace="base")),
    url(r'^member/', include('djanban.apps.members.urls', namespace="members")),
    url(r'^api/', include('djanban.apps.api.urls', namespace="api")),
    url(r'^boards/', include('djanban.apps.boards.urls', namespace="boards")),
    url(r'^times/', include('djanban.apps.dev_times.urls', namespace="dev_times")),
    url(r'^charts/', include('djanban.apps.charts.urls', namespace="charts")),
    url(r'^hourly_rates/', include('djanban.apps.hourly_rates.urls', namespace="hourly_rates")),
    url(r'^fetch/', include('djanban.apps.fetch.urls', namespace="fetch")),
    url(r'^forecasters/', include('djanban.apps.forecasters.urls', namespace="forecasters")),
    url(r'^environment/', include('djanban.apps.dev_environment.urls', namespace="dev_environment")),
    url(r'^multiboards/', include('djanban.apps.multiboards.urls', namespace="multiboards")),
    url(r'^notifications/', include('djanban.apps.notifications.urls', namespace="notifications")),
    url(r'^reports/', include('djanban.apps.reports.urls', namespace="reports")),
    url(r'^slideshow/', include('djanban.apps.slideshow.urls', namespace="slideshow")),
    url(r'^visitors/', include('djanban.apps.visitors.urls', namespace="visitors")),
    url(r'^niko-niko-calendar/', include('djanban.apps.niko_niko_calendar.urls', namespace="niko_niko_calendar")),
    url(r'^work-hours-packages/', include('djanban.apps.work_hours_packages.urls', namespace="work_hours_packages")),

    url(r'^async_include/', include('async_include.urls', namespace="async_include")),

    url(r'^password-reset/', include('djanban.apps.password_reseter.urls', namespace="password_reseter")),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^captcha/', include('captcha.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve_static, { 'document_root': settings.MEDIA_ROOT, }),
        url(r'^static/(?P<path>.*)$', serve_static, { 'document_root': settings.STATIC_ROOT }),
        #url(settings.ANGULAR_URL_REGEX, serve_static, { 'document_root': settings.ANGULAR_ROOT })
    ]


