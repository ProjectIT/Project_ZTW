from django.conf.urls import url

from projects import views

urlpatterns = [
	url(r'^(?P<id>\d+)/edit$', views.task_edit, name='task_edit'),
	url(r'^create$', views.task_edit, name='task_create'),
    url(r'^(?P<id>\d+)$', views.task, name='task'),

	url(r'^user/(?P<id>\d+)$', views.user_tasks_list, name='user_tasks_list') # tasks for user
]