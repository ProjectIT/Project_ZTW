from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader, RequestContext
from projects.stubs import create_stub_project, create_stub_user, create_stub_task, create_stub_file

# date format:
#https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date

def project(request, id):
	# get data
	active_user = create_stub_user()
	project_creator = create_stub_user()
	p = create_stub_project(project_creator)
	p.tasks = [create_stub_task(p,project_creator,active_user) for i in range(4)]
	p.people = [create_stub_user() for i in range(4)]
	p.files = [create_stub_file(project_creator,projectId=p) for i in range(4)]

	# for f in p.files:
	# 	f.short_name = str(f.path[f.path.rfind("/")+1:])

	# render
	template = loader.get_template('project_read.html')
	context = RequestContext(request, {
		'projectId': id,
		'project': p,
	})
	return HttpResponse(template.render(context))

def project_edit(request, id):
	template = loader.get_template('project_write.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))

def project_list(request):
	template = loader.get_template('project_list.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))


def user_project_list(request, id):
	template = loader.get_template('project_list.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))

#
# tasks
#

def task(request, id):
	template = loader.get_template('task_read.html')
	context = RequestContext(request, {
		'taskId': id,
	})
	return HttpResponse(template.render(context))

def task_edit(request, id):
	template = loader.get_template('task_write.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))

def user_tasks_list(request, id):
	template = loader.get_template('task_list.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))

