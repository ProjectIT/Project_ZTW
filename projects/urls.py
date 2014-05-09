from django.conf.urls import url

from projects import views

urlpatterns = [
	url(r'^(?P<id>\d+)/edit$', views.project_edit, name='project_edit'),
    url(r'^(?P<id>\d+)$', views.project, name='project'),

	#TODO lists
	url(r'^list$', views.project_list, name='project_list'), # all projects
	url(r'^list/user/(?P<id>\d+)$', views.user_project_list, name='user_project_list') # projects for user

]