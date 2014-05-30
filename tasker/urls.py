from django.conf.urls import patterns, include, url

from django.contrib import admin
from tasker import views


admin.autodiscover()

# https://docs.djangoproject.com/en/dev/intro/tutorial03/
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
	url(r'^project/', include('projects.urls')),
	url(r'^task/', include('projects.task_urls')),

	url(r'^$', views.mainpage, name="home"),
	url(r'^about$', views.about, name="about"),
	url(r'^login$', views.loginSite, name="loginSite"),

	url(r'^settings$', views.settings, name="settings"),

	# friends
	url(r'^profile/(?P<id>\d+)$', views.public_profile, name="public_profile"),
	url(r'^friends/user/(?P<id>\d+)$', views.friends_list, name="friends_list"),
)
