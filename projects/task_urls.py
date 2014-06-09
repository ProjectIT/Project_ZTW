from django.conf.urls import url

from projects import views_tasks

urlpatterns = [
	url(r'^(?P<id>\d+)/edit$', views_tasks.task_edit, name='task_edit'),
	url(r'^create/(?P<project_id>\d+)$', views_tasks.task_create, name='task_create'),
    url(r'^(?P<id>\d+)$', views_tasks.task, name='task'),
	url(r'^comment/(?P<task_id>\d+)$', views_tasks.task_comment, name='task_comment'),

	url(r'^user/(?P<id>\d+)$', views_tasks.user_tasks_list, name='user_tasks_list') # tasks for user
]