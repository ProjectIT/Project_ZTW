from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader, RequestContext


def project(request, id):
	template = loader.get_template('project_read.html')
	context = RequestContext(request, {
		'projectId': id,
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

