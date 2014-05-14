from django.http import HttpResponse
from django.template import loader, RequestContext

from projects.models import Task
from projects.stubs import create_stub_user, __createExampleProject, __createExampleTask

# TODO add 'user_project_list' for all users in public profile

# NOTE: 'user' in templates is a reserved keyword

# date format:
#https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date


def get_context( tmplContext):
	user=create_stub_user()
	context = {
		'currentUser':user,
		'user_id':user.id,
		'task_count':2,
	}
	# concat
	return dict(list(context.items()) + list(tmplContext.items()))


#
# projects
#
def project(request, id):
	p = __createExampleProject()

	template = loader.get_template('project_read.html')
	context = RequestContext(request,  get_context({
		'projectId': id,
		'project': p,
		'data_page_type':'projects'
	}))
	return HttpResponse(template.render(context))

def project_edit(request, id):
	p = __createExampleProject()

	template = loader.get_template('project_write.html')
	context = RequestContext(request,  get_context({
		'projectId': id,
		'project': p,
		'data_page_type':'projects'
	}))
	return HttpResponse(template.render(context))

def project_create(request):
	template = loader.get_template('project_write.html')
	context = RequestContext(request,  get_context({
		'new_project': True,
		'data_page_type':'projects'
	}))
	return HttpResponse(template.render(context))


def project_list(request):
	ps = [__createExampleProject() for _ in range(7)]

	template = loader.get_template('project_list.html')
	context = RequestContext(request, get_context({
		'projects':ps,
		'data_page_type':'projects'
	}))
	return HttpResponse(template.render(context))


def user_project_list(request, id):
	return project_list(request)

#
# tasks
#
# TODO utilize task status

def task(request, id):
	template = loader.get_template('task_read.html')
	task = __createExampleTask()

	context = RequestContext(request,  get_context({
		'taskId': id,
		'task': task,
		'canAddComment':False,
		'data_page_type':'tasks',
		'taskTypes': Task.TASK_TYPES,
	}))
	return HttpResponse(template.render(context))

def task_edit(request, id, back_url=""):
	# TODO back_url - we need to acknowledge that sometimes we want to go back to the projectWrite, not to taskRead
	template = loader.get_template('task_write.html')
	task = __createExampleTask()

	context = RequestContext(request,  get_context({
		'taskId': id,
		'task': task,
		'taskTypes': Task.TASK_TYPES,
		'data_page_type':'tasks'
	}))
	return HttpResponse(template.render(context))

def task_create(request):
	template = loader.get_template('task_write.html')
	context = RequestContext(request,  get_context({
		'new_project': True,
		'taskTypes': Task.TASK_TYPES,
		'data_page_type':'tasks'
	}))
	return HttpResponse(template.render(context))

def user_tasks_list(request, id):
	ts = [__createExampleTask() for _ in range(7)]

	template = loader.get_template('task_list.html')
	context = RequestContext(request,  get_context({
		'tasks':ts,
		'data_page_type':'tasks'
	}))
	return HttpResponse(template.render(context))

