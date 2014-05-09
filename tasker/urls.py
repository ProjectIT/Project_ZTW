from django.conf.urls import patterns, include, url

from django.contrib import admin
from tasker import views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls))
)
