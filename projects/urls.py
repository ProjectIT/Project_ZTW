from django.conf.urls import url

from projects import views

urlpatterns = [
	url(r'^(?P<id>\d+)/edit$', views.project_edit, name='project_edit'),
	url(r'^create$', views.project_create, name='project_create'),
    url(r'^(?P<id>\d+)$', views.project, name='project'),

	# all projects
	url(r'^list$', views.project_list, name='project_list'),
	# projects for user
	url(r'^user/(?P<id>\d+)$', views.user_project_list, name='user_project_list')

]