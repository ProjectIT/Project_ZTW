from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader, RequestContext
from projects.stubs import create_stub_project, create_stub_user, create_stub_task, create_stub_file

# TODO add 'user_project_list' for all users in public profile

# date format:
#https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date

def __createExampleProject():
	# just for testing
	project_creator = create_stub_user()
	p = create_stub_project(project_creator)
	p.tasks = [create_stub_task(p, project_creator, create_stub_user()) for _ in range(4)]
	p.people = [create_stub_user() for _ in range(4)]
	p.files = [create_stub_file(project_creator,projectId=p) for _ in range(4)]
	return p

def project(request, id):
	# get data
	active_user = create_stub_user()
	p = __createExampleProject()

	# render
	template = loader.get_template('project_read.html')
	context = RequestContext(request, {
		'projectId': id,
		'project': p,
	})
	return HttpResponse(template.render(context))

def project_edit(request, id):
	# get data
	active_user = create_stub_user()
	p = __createExampleProject()

	# render
	template = loader.get_template('project_write.html')
	context = RequestContext(request, {
		'projectId': id,
		'project': p,
	})
	return HttpResponse(template.render(context))

def project_create(request):
	# get data
	active_user = create_stub_user()

	# render
	template = loader.get_template('project_write.html')
	context = RequestContext(request, {
		'new_project': True,
	})
	return HttpResponse(template.render(context))


def project_list(request):
	ps = [__createExampleProject() for _ in range(7)]

	template = loader.get_template('project_list.html')
	context = RequestContext(request, {
		'projects':ps
	})
	return HttpResponse(template.render(context))


def user_project_list(request, id):
	return project_list(request)

#
# tasks
#

def task(request, id):
	template = loader.get_template('task_read.html')
	context = RequestContext(request, {
		'taskId': id,
	})
	return HttpResponse(template.render(context))

def task_edit(request, id, back_url=""):
	# back_url - we need to acknowledge that sometimes we want to go back to the projectWrite, not to taskRead
	template = loader.get_template('task_write.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))

def task_create(request):
	return render(request, 'about.html') # !!! stub, cause emits error otherwise

def user_tasks_list(request, id):
	template = loader.get_template('task_list.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))

